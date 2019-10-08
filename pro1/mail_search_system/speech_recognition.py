import requests
import json
import uuid
import base64

# 获取申请的token
def get_token():
    url = "https://openapi.baidu.com/oauth/2.0/token"
    grant_type = "client_credentials"
    api_key = "3DW6KeoT2sv56yIIYgIrcXlb"                     # 自己申请的应用
    secret_key = "DtBG5jODm664HqT986hMYmZ2asyIHFul"            # 自己申请的应用
    data = {'grant_type': grant_type, 'client_id': api_key, 'client_secret': secret_key}
    r = requests.post(url, data=data)
    token = json.loads(r.text).get("access_token")
    return token

# 调用语音识别API进行文本化
def recognize(sig, rate, token):
    url = "http://vop.baidu.com/server_api"
    speech_length = len(sig)
    speech = base64.b64encode(sig).decode("utf-8")
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    rate = rate
    # 查看官方文档后进行参数的设置
    data = {
        "format": "wav",
        "lan": "en",
        "token": token,
        "len": speech_length,
        "rate": rate,
        "speech": speech,
        "cuid": mac_address,
        "channel": 1,
    }
    data_length = len(json.dumps(data).encode("utf-8"))
    headers = {"Content-Type": "application/json",
               "Content-Length": str(data_length)}
    r = requests.post(url, data=json.dumps(data), headers=headers)

    return r.json()

# # 测试代码
# filename = "./speechs/input.wav"
# signal = open(filename, "rb").read()
# rate = 16000
# token = get_token()
# recognize(signal, rate, token)
