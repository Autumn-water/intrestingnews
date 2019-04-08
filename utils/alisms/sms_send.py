# -*- coding: utf-8 -*-
import json
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from django.conf import settings

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


# telephone  captcha
def send_sms(phone_numbers, captcha):
    business_id = uuid.uuid1()
    sign_name = settings.SING_NAME
    template_code = settings.TEMPLATE_CODE
    template_param = json.dumps({"code": captcha})

    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)
	
    # 数据提交方式
	# smsRequest.set_method(MT.POST)
	
	# 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
	
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    return smsResponse



# if __name__ == '__main__':
   #  __business_id = uuid.uuid1()
    #print(__business_id)
    # 只能是一个标准 JSON 字符串 {"": ""}
    # params = "{\"code\":\"12345\"}"
	#params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'  前段时间  1分钟一条 同一个手机号 现在 1分钟两条
    # send_sms(__business_id, "17767095149", "付帅帅", "SMS_142947701", params)
    # import json
    # print(json.loads(send_sms("17767095149", params)))
   # 代码一周发一次
   # json.loads
    # b'{\uxxx\xx\}'  转换编码
   # str(send_sms(__business_id, "17767095149", "付帅帅", "SMS_142947701", params), encoding='utf-8')
