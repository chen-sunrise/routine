# -*- coding:utf-8 -*-
# 图片验证码和短信验证码
from rent_house.utils.response_code import RET
from . import api
from flask import request, jsonify, abort, make_response
from rent_house.utils.captcha.captcha import captcha
from rent_house import redis_store
from rent_house import constants


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

    # 3.使用uuid存储图片验证码内容到redis
    try:
        if last_uuid:
            # 上次的uuid还存在，删除上次的uuid对应的记录
            redis_store.delete('ImageCode'+last_uuid)

        # 保存本次需要记录的验证码数据
        redis_store.set('ImageCode'+last_uuid, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg=u'保存验证码失败')

    # 4.返回图片验证码
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    return response


