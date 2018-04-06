# -*- coding:utf-8 -*-
# 实现注册和登录
from rent_house import redis_store, db
from rent_house.utils.response_code import RET
from . import api
from rent_house.models import User
from flask import request, jsonify, current_app
import json



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

    # 7.做出响应
    return jsonify(errno=RET.OK, errmsg='注册成功')
