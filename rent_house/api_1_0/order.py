# -*- coding:utf-8 -*-
# 处理订单逻辑
from rent_house import db
from rent_house.models import House, Order
from rent_house.utils.common import login_required
from rent_house.utils.response_code import RET
from . import api
from flask import g, request, jsonify, current_app
import datetime


@api.route('/orders', methods=['POST'])
@login_required
def create_order():
    '''创建、提交订单
    1.接受参数，house_id,入住时间和离开时间
    2.校验参数，判断入住时间和离开时间是否符合逻辑，校验房屋是否存在
    3.判断当前房屋有没有被预定
    4.创建订单模型对象，并存储订单数据
    5.保存到数据库
    6.响应结果'''


    # 1.接受参数，house_id,入住时间和离开时间
    json_dict = request.json
    house_id = json_dict.get('house_id')
    start_date_str = json_dict.get('start_date')
    end_date_str = json_dict.get('end_date')

    # 判断是否缺少参数
    if not all([house_id, start_date_str, end_date_str]):
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')

    # print start_date_str
    # print '-----'
    # print end_date_str

    # 2.校验参数，判断入住时间和离开时间是否符合逻辑，校验房屋是否存在
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
        # print start_date
        # print '----'
        # print end_date
        if start_date and end_date:
            assert start_date < end_date, Exception('入住时间有误1')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='入住时间有误2')

    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询房屋信息失败')
    if not house:
        return jsonify(errno= RET.NODATA, errmsg='该房屋不存在')

    # 3.判断当前房屋有没有被预定
    try:
        Order.query.filter(Order.house_id == house_id, end_date > Order.begin_date, start_date < Order.end_date)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='该房屋已被预定')

    # 4.创建订单模型对象，并存储订单数据
    days = (end_date - start_date).days # 计算时间段之间的天数
    order = Order()
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = house.price * days

    # 5.保存订单到数据库
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存订单数据失败')

    # 响应结果
    return jsonify(errno=RET.OK, errmsg='OK')


