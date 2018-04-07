# -*- coding:utf-8 -*-
# 实现注册和登录
from rent_house import redis_store, db
from rent_house.utils.common import login_required
from rent_house.utils.response_code import RET
from . import api
from rent_house.models import User
from flask import request, jsonify, current_app, session
import json
import re


@api.route('/sessions')
def check_login():
    """判断用户是否登录
    0.提示:该接口是用于前端在渲染界面时判断使用的根据不同的登录状态，展示不同的界面
    """

    user_id = session.get('user_id')
    name = session.get('name')

    return jsonify(errno=RET.OK, errmsg='OK', data={'user_id':user_id, 'name':name})



@api.route('/sessions', methods=['DELETE'])
@login_required
def logout():
    '''实现退出登录
    '''

    session.pop('user_id')
    session.pop('name')
    session.pop('mobile')

    return jsonify(errno=RET.OK, errmsg='退出登录成功')


@api.route('/sessions', methods=['POST'])
def login():
    '''
    实现登录
    1.接受请求参数：手机号，明文密码
    2.判断是否缺少参数，并做手机号格式校验
    3.使用手机号查询该要登录的用户数据是否登录
    4.对密码进行校验
    5.将用户的状态保持信息写入session
    6.响应登录结果
    :return:
    '''

    # 1.接受请求参数：手机号，明文密码
    json_dict = request.json
    mobile = json_dict.get('mobile')
    password = json_dict.get('password')

    # 2.判断是否缺少参数，并做手机号格式校验
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    # 做手机号格式校验
    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 3.使用手机号查询该要登录的用户数据是否存在
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.USERERR, errmsg='用户名或密码错误')

    # 4.对密码进行校验
    print password,mobile,json_dict
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='用户名或密码错误')

    # 5.将用户的状态保持信息写入到session
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile

    # 6.响应登录结果
    return jsonify(errno=RET.OK, errmsg='登录成功')

    # # 1.接受请求参数：手机号，明文密码
    # json_dict = request.json
    # mobile = json_dict.get('mobile')
    # password = json_dict.get('password')
    # # print password
    #
    # # 判断是否缺少参数，并做手机号的验证
    # if not all([mobile, password]):
    #     return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    # # 做手机号格式校验
    # if not re.match(r'^1[345678][0-9]{9}$', mobile):
    #     return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    #
    # # 3.使用手机号查询该要登录的用户数据是否登录
    # try:
    #     user = User.query.filter(User.mobile == mobile).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR,errmsg='查询用户失败')
    #
    # if not user:
    #     return jsonify(errno=RET.USERERR, errmsg='用户或密码错误')
    # # 4.对密码进行校验
    # if not user.check_password(password):
    #     return jsonify(errno=RET.PWDERR, errmsg='用户名或密码错误')
    #
    # # 5.将用户的状态保持信息写入session
    # session['user_id'] = user.id
    # session['name'] = user.name
    # session['mobile'] = user.mobile
    #
    # # 6.响应登录结果
    # return jsonify(errno=RET.OK, errmsg='登录成功')


@api.route('/users', methods=['POST'])
def register():
    '''
    实现注册
    1.获取请求参数：手机号，短信验证码，密码
    2.判断参数是否缺失
    3.获取服务器的短信验证码
    4.并和客户端的短信验证码比较，如果一致
    5.创建User模型类对象
    6.保存数据到数据库
    7.响应结果
    :return:
    '''

    # 1.获取请求参数：手机号，短信验证码，密码
    # 第一种办法
    # json_str = request.data
    # json_dict = json.loads(json_str)
    # 2.第二中办法
    # json_dict = request.get_json()
    # 第三种办法
    json_dict = request.json

    mobile= json_dict.get('mobile')
    sms_code_client = json_dict.get('sms_code')
    password = json_dict.get('password')


    # 2.判断参数是否缺失
    if not all([mobile,sms_code_client,password]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # 3.获取服务器的短信验证码
    try:
        sms_code_server = redis_store.get('Mobile:' + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询短信验证码失败')
    if not sms_code_server:
        return jsonify(errno=RET.NODATA,errmsg='短信验证码不存在')

    # 4.并和客户端的短信验证码比较，如果一致
    if sms_code_client != sms_code_server:
        return jsonify(errno=RET.DATAERR, errmsg='输入验证码有误')

    # 判断该用户是否已经注册
    if User.query.filter(User.mobile == mobile).first():
        return jsonify(errno=RET.DATAEXIST, errmsg='用户已经注册')

    # 5.创建User模型类对象
    user = User()
    user.name = mobile
    user.mobile = mobile
    # 密码需要加密后才能存储
    # user.password_hash = '加密后的密码'
    user.password = password

    # 6.保存数据到数据库中
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存注册信息失败')

    # 实现注册成功即登录：记住状态保持信息即可
    session['user_id'] = user.id
    session['name'] = user.name
    session['mobile'] = user.mobile


    # 7.做出响应
    return jsonify(errno=RET.OK, errmsg='注册成功')
