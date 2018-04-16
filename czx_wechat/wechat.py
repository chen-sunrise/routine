# -*- coding:utf-8 -*-
import xmltodict
import time
from flask import Flask, request
import hashlib


WECHAT_TOKEN = 'python'


app = Flask(__name__)


@app.route('/wechat8006', methods=['POST', 'GET'])
def index():
    # signature: 微信加密签名
    signature = request.args.get('signature')
    # timestamp: 时间戳
    timestamp = request.args.get('timestamp')
    # nonce: 随机数
    nonce = request.args.get('nonce')
    # echostr: 随机字符串
    echostr = request.args.get('echostr')

    '''
    开发者通过检验signature对请求进行校验。若确认此次GET请求来自微信服务器，
    请原样返回echostr参数内容，则接入生效，成为开发者成功，否则接入失败。

    xmltodict.parse()方法可以将xml数据转为python中的dict字典数据
    xmltodict.unparse()方法可以将字典转换为xml字符串
    '''
    # 校验流程：

    # 将token、timestamp、nonce三个参数进行字典序排序(就是以a到z排序)
    tmp_list = [WECHAT_TOKEN, timestamp, nonce]
    tmp_list.sort()
    # 将三个参数字符串拼接成一个字符串进行sha1加密
    tmp_list = ''.join(tmp_list)
    sin_str = hashlib.sha1(tmp_list).hexdigest()

    # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if sin_str == signature:
        if request.method == 'POST':
        # 处理消息
        # 接受用户发送微信服务器转发的xml字符串
            xml_str = request.data
        # 转成易于操作的字典
            xml_dict = xmltodict.parse(xml_str)
            request_dict = xml_dict.get('xml')
        # 获取类型
            msg_type = request_dict.get('MsgType')

            if msg_type == 'text':
                new_dict = {
                    'ToUserName': request_dict.get('FromUserName'),
                    'FromUserName': request_dict.get('ToUserName'),
                    'CreateTime': time.time(),
                    'MsgType':'text',
                    'Content': u'你真的感兴趣么'
                }
                # 封装响应的字典
                response_dict = {'xml': new_dict}
                # 将响应的字典转为xml字符串
                response_xml_str= xmltodict.unparse(response_dict)
                # 发送xml字符串给微信服务器，然后服务器转到到粉丝
                return response_xml_str
            elif msg_type == 'voice':
                # 此时的需求： 接受到语音后，转成文字，再回给粉丝
                # 收到语音消息
                recognition_str = request_dict.get('Recognition')
                new_dict = {
                    'ToUserName': request_dict.get('FromUserName'),
                    'FromUserName': request_dict.get('ToUserName'),
                    'CreateTime': time.time(),
                    'MsgType': 'text',
                    'Content': recognition_str
                }
                response_dict = {'xml':new_dict}
                response_xml_str = xmltodict.unparse(response_dict)
                return response_xml_str
            elif msg_type == 'event':
                # 获取是关注还是取消关注
                event =  request_dict.get('Event')
                # 判断是关注的话
                if event == 'subscribe':
                    new_dict = {
                        'ToUserName': request_dict.get('FromUserName'),
                        'FromUserName': request_dict.get('ToUserName'),
                        'CreateTime': time.time(),
                        'MsgType': 'text',
                        'Content': u'感谢您的关注'
                    }
                    # 地址后跟的数据
                    event_key = request_dict.get('EventKey')
                    print event_key
                    if event_key:
                        print u'你扫描的是我们的%s号工作人员' % event_key
                    response_dict = {'xml': new_dict}
                    response_xml_str = xmltodict.unparse(response_dict)
                    return response_xml_str
        else:
            return echostr # 告诉微信服务器，我给你的ip是ok的



    return '' # 告诉微信服务不可用


if __name__ == '__main__':
    app.run(debug=True, port=8006)