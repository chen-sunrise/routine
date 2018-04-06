# -*- coding:utf-8 -*-
# 图片验证码和短信验证码
from flask import current_app

from rent_house.utils.response_code import RET
from rent_house.utils.sms import CCP
from . import api
from flask import request, jsonify, abort, make_response
from rent_house.utils.captcha.captcha import captcha
from rent_house import redis_store
from rent_house import constants
import json
import re
import random


@api.route('/sms_code', methods = ['POST'])
def send_sms_code():
    '''
    1.接受参数：手机号，uuid，图片验证码
    2.判断参数是否有缺失，并且对手机号进行校验
    3.获取图片验证码，以uuid作为key
    4.与客户端的验证码做比较，如果相同
    5.生成短信验证码
    6.使用云通讯发送短信验证码
    7.存储短信验证码
    8.返回响应结果
    :return:
    '''

    # 1.接受参数
    json_str = request.data
    json_dict = json.loads(json_str)

    mobile = json_dict.get('mobile')
    imageCode_client = json_dict.get('imagecode')
    uuid = json_dict.get('uuid')

    # 2.判读参数是否缺失，并对手机号进验证
    if not all([mobile, imageCode_client, uuid]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    if not re.match(r'^1[345678][0-9]{9}$', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 3.获取图片验证码，uuid作为key
    try:
        imageCode_server = redis_store.get('ImageCode:' + uuid)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询服务器验证码失败')

    # 判断是否为空或者过期
    # if not imageCode_server:
    #     return jsonify(errno=RET.NODATA, errmsg='验证码不存在')

    # 4.与客户端验证对比
    if imageCode_server.lower() != imageCode_client.lower():
        return jsonify(errno=RET.DATAERR, errmsg='验证码输入错误')

    # 5.生成短信信息
    sms_code = '%06d' % random.randint(0,999999)
    current_app.logger.error(sms_code)

    # 6.用云通讯发送短信到用户手机中
    # result = CCP().send_template_sms(mobile,[sms_code, constants.SMS_CODE_REDIS_EXPIRES/60], '1')
    # if result != 1:
    #     return jsonify(errno = RET.THIRDERR, errmsg = '发送短信验证码失败')

    # 7.存储短信验证码到redis中:短信验证码在redis中的有效期一定要和短信验证码的提示信息一致
    # 参数3有效时间
    try:
        redis_store.set('Mobile:'+mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR, errmsg = '存储验证码失败')

    # 8.返回响应结果
    return jsonify(errno=RET.OK, errmsg='短信发送成功')




@api.route('/image_code')
def get_image_code():
    '''
    提供图片验证码
    1.接受请求，获取uuid
    2.生成图片验证码
    3.使用uuid存储图片验证码内容到redis
    4.返回图片验证码
    :return:
    '''

    # 1.接受请求，获取uuid
    uuid = request.args.get('uuid')
    last_uuid = request.args.get('last_uuid')
    if not uuid:
        abort(403)
        # return jsoify(error=RET.PARAMERR, errmsg=u'缺少参数')


    # 2.生成验证码：text是验证码的文字信息，image验证码的图片信息
    name, text, image = captcha.generate_captcha()
    current_app.logger.debug('图片验证码文字信息：' + text)


    # 3.使用uuid存储图片验证码内容到redis
    try:
        if last_uuid:
            # 上次的uuid还存在，删除上次的uuid对应的记录
            redis_store.delete('ImageCode:'+last_uuid)

        # 保存本次需要记录的验证码数据
        redis_store.set('ImageCode:'+uuid, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'保存验证码失败')

    # 4.返回图片验证码
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    return response



