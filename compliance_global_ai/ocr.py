"""
ocr 阿里云文字识别
"""

import json
import os
import sys

from typing import List

from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_credentials.client import Client as CredentialClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class OCRClient:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> ocr_api20210707Client:
        """
        使用凭据初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码建议使用更安全的无AK方式，凭据配置方式请参见：https://help.aliyun.com/document_detail/378659.html。
        credential = CredentialClient()
        config = open_api_models.Config(
            access_key_id=os.environ["OCR_ACCESS_KEY_ID"],
            access_key_secret=os.environ["OCR_ACCESS_KEY_SECRET"],
        )
        # Endpoint 请参考 https://api.aliyun.com/product/ocr-api
        config.endpoint = f"ocr-api.cn-hangzhou.aliyuncs.com"
        return ocr_api20210707Client(config)

    @staticmethod
    def main(url: str) -> None:
        client = OCRClient.create_client()
        # 营业执照识别
        # recognize_request = ocr_api_20210707_models.RecognizeBusinessLicenseRequest(url=url)
        # 通用识别
        recognize_request = ocr_api_20210707_models.RecognizeBusinessLicenseRequest(
            url=url
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 营业执照识别
            # resp = client.recognize_business_license_with_options(recognize_request, runtime)
            # 通用识别
            # resp = client.recognize_general_with_options(recognize_request, runtime)
            # content = json.loads(resp.body.data)['content']
            # print("ocr content:", content)
            # return content
            # return '{ "algo_version": "", "angle": 0, "codes": [ { "data": "", "points": [ { "x": 97, "y": 502 }, { "x": 169, "y": 502 }, { "x": 169, "y": 578 }, { "x": 97, "y": 578 } ], "type": "QRcode" } ], "data": { "title": "营业执照", "creditCode": "510302000014926", "companyName": "自贡市一品堂商贸有限责任公司", "companyType": "有限责任公司(自然人投资或控股)", "businessAddress": "自贡市自流井区五星街西巷12组10号附9号", "legalPerson": "曹文军", "businessScope": "销售预:包装食品兼散装食品(食品流通许可证有效期至2016年2月29日)。销售;蔬菜、水果、工艺品、化妆品、", "registeredCapital": "叁万元人民币", "RegistrationDate": "2013年03月15日", "validPeriod": "2013年03月15日至2033年03月14日", "validFromDate": "20130315", "validToDate": "20330314", "issueDate": "2014年10月28日", "companyForm": "" }, "figure": [ { "type": "round_stamp", "x": 348, "y": 522, "w": 89, "h": 92, "box": { "x": 391, "y": 567, "w": 88, "h": 84, "angle": 89 }, "points": [ { "x": 349, "y": 524 }, { "x": 433, "y": 523 }, { "x": 435, "y": 611 }, { "x": 350, "y": 611 } ] }, { "type": "qrcode", "x": 97, "y": 502, "w": 72, "h": 76, "box": { "x": 132, "y": 539, "w": 69, "h": 73, "angle": 0 }, "points": [ { "x": 98, "y": 504 }, { "x": 168, "y": 503 }, { "x": 167, "y": 576 }, { "x": 97, "y": 576 } ] }, { "type": "blicense_title", "x": 115, "y": 81, "w": 281, "h": 66, "box": { "x": 254, "y": 113, "w": 58, "h": 277, "angle": 88 }, "points": [ { "x": 118, "y": 87 }, { "x": 392, "y": 82 }, { "x": 394, "y": 140 }, { "x": 117, "y": 146 } ] }, { "type": "national_emblem", "x": 206, "y": 14, "w": 95, "h": 51, "box": { "x": 253, "y": 39, "w": 45, "h": 93, "angle": 88 }, "points": [ { "x": 207, "y": 18 }, { "x": 299, "y": 15 }, { "x": 299, "y": 61 }, { "x": 207, "y": 63 } ] } ], "ftype": 0, "height": 667, "orgHeight": 667, "orgWidth": 500, "prism_keyValueInfo": [ { "key": "title", "keyProb": 100, "value": "营业执照", "valuePos": [ { "x": 113, "y": 84 }, { "x": 396, "y": 75 }, { "x": 397, "y": 143 }, { "x": 112, "y": 151 } ], "valueProb": 100 }, { "key": "creditCode", "keyProb": 100, "value": "510302000014926", "valuePos": [ { "x": 322, "y": 166 }, { "x": 434, "y": 164 }, { "x": 434, "y": 176 }, { "x": 322, "y": 178 } ], "valueProb": 100 }, { "key": "companyName", "keyProb": 100, "value": "自贡市一品堂商贸有限责任公司", "valuePos": [ { "x": 197, "y": 206 }, { "x": 378, "y": 202 }, { "x": 378, "y": 216 }, { "x": 197, "y": 220 } ], "valueProb": 100 }, { "key": "companyType", "keyProb": 97, "value": "有限责任公司(自然人投资或控股)", "valuePos": [ { "x": 196, "y": 234 }, { "x": 391, "y": 231 }, { "x": 392, "y": 245 }, { "x": 196, "y": 248 } ], "valueProb": 97 }, { "key": "businessAddress", "keyProb": 100, "value": "自贡市自流井区五星街西巷12组10号附9号", "valuePos": [ { "x": 195, "y": 259 }, { "x": 462, "y": 254 }, { "x": 463, "y": 268 }, { "x": 195, "y": 273 } ], "valueProb": 100 }, { "key": "legalPerson", "keyProb": 100, "value": "曹文军", "valuePos": [ { "x": 196, "y": 292 }, { "x": 237, "y": 291 }, { "x": 237, "y": 305 }, { "x": 196, "y": 306 } ], "valueProb": 100 }, { "key": "businessScope", "keyProb": 100, "value": "销售预:包装食品兼散装食品(食品流通许可证有效期至2016年2月29日)。销售;蔬菜、水果、工艺品、化妆品、", "valuePos": [ { "x": 191, "y": 409 }, { "x": 469, "y": 405 }, { "x": 470, "y": 425 }, { "x": 191, "y": 428 } ], "valueProb": 99 }, { "key": "registeredCapital", "keyProb": 100, "value": "叁万元人民币", "valuePos": [ { "x": 195, "y": 322 }, { "x": 276, "y": 320 }, { "x": 276, "y": 335 }, { "x": 195, "y": 337 } ], "valueProb": 100 }, { "key": "RegistrationDate", "keyProb": 100, "value": "2013年03月15日", "valuePos": [ { "x": 196, "y": 354 }, { "x": 306, "y": 352 }, { "x": 306, "y": 366 }, { "x": 196, "y": 368 } ], "valueProb": 100 }, { "key": "validPeriod", "keyProb": 100, "value": "2013年03月15日至2033年03月14日", "valuePos": [ { "x": 195, "y": 382 }, { "x": 436, "y": 378 }, { "x": 436, "y": 394 }, { "x": 195, "y": 397 } ], "valueProb": 100 }, { "key": "validFromDate", "keyProb": 100, "value": "20130315", "valuePos": [ { "x": 195, "y": 382 }, { "x": 436, "y": 378 }, { "x": 436, "y": 394 }, { "x": 195, "y": 397 } ], "valueProb": 100 }, { "key": "validToDate", "keyProb": 100, "value": "20330314", "valuePos": [ { "x": 195, "y": 382 }, { "x": 436, "y": 378 }, { "x": 436, "y": 394 }, { "x": 195, "y": 397 } ], "valueProb": 100 }, { "key": "issueDate", "keyProb": 100, "value": "2014年10月28日", "valuePos": [ { "x": 335, "y": 617 }, { "x": 448, "y": 617 }, { "x": 449, "y": 627 }, { "x": 335, "y": 628 } ], "valueProb": 100 }, { "key": "companyForm", "keyProb": 100, "value": "", "valueProb": 100 } ], "sliceRect": { "x0": 25, "y0": 22, "x1": 486, "y1": 9, "x2": 500, "y2": 665, "x3": 12, "y3": 667 }, "width": 500 }'
            return "营! 业执照 注册号510302000014926 名 称 自贡市一品堂商贸有限责任公司 类 型 有限责任公司(自然人投资或控股) 住 所 自贡市自流井区五星街西巷12组10号附9号 法定代表人 曹文军 注册资本 叁万元人民币 成立日 期 2013年03月15日 营业期 限 2013年03月15日至2033年03月14日 经营范围 销售预：包装食品栽散装食品(食品流通许可证有效期至2016年2 月29日)。销售；蔬菜、水果、工艺品、化妆品、 登记机关 2014 年10月 28日"
        except Exception as error:
            print(error)

    @staticmethod
    async def main_async(url: str) -> None:
        client = OCRClient.create_client()
        recognize_business_license_request = (
            ocr_api_20210707_models.RecognizeBusinessLicenseRequest(url=url)
        )
        runtime = util_models.RuntimeOptions()
        try:
            await client.recognize_business_license_with_options_async(
                recognize_business_license_request, runtime
            )
        except Exception as error:
            print(error.message)
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)


if __name__ == "__main__":
    url = "https://img0.baidu.com/it/u=980771503,1131783134&fm=253&app=120&f=JPEG?w=500&h=667"
    OCRClient.main(url)
