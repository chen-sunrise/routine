#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-

from rent_house.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '8a216da86276486901629a048d1d0e06';

#���ʺ�Token
accountToken= '74c3d4fc131749bb95d341ccc6e06ac2';

#Ӧ��Id
appId='8a216da86276486901629a048d6e0e0c';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
  # @param $tempId ģ��Id


class CCP(object):
    '''�Զ��嵥���࣬���ڷ��Ͷ���'''

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)


            # ��ʼ��REST SDK
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)

        return cls._instance


    def send_template_sms(self, to, datas, tempId):
        '''�������Ͷ��ŵķ���
        ����ֵ�������1����ʾ��ͨѶ�����Ƿ��Ͷ����ǳɹ��ģ������0����ʾʧ��'''

        # result: ����ͨѶ���߿����ߵĽ����Ϣ
        result = self.rest.sendTemplateSMS(to, datas, tempId)

        # return�Ľ��ֵ���ǿ����߸����û������Ƿ��ͳɹ�
        if result.get('statusCode') == '000000':
            return 1
        else:
            return 0

# def sendTemplateSMS(to,datas,tempId):
#
#
#     #��ʼ��REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
    

# ����1��Ŀ���ֻ�
# ����2����һ��Ԫ�أ�������֤�� �ڶ���Ԫ�أ�������֤�����Ч�� ��λΪ����
# ����3�����ŵ�ģ�壬Ĭ���ṩ��ģ���idΪ1
# sendTemplateSMS('13113842566',['666666', '5'],1)