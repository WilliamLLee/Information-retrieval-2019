##############################
# get data from source files
# filename:init.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.5
##############################

import pyaudio
import wave
import requests
import json
import uuid
import base64


input_filename = "input.wav"               # 麦克风采集的语音输入
input_filepath = "./speechs/"              # 输入文件的path
in_path = input_filepath + input_filename

def get_audio(filepath):
    aa = 'yes' #str(input("=>start recording？   （yes/no） :"))
    if aa == str("yes") :
        CHUNK = 256
        FORMAT = pyaudio.paInt16
        CHANNELS = 1                # 声道数
        RATE = 16000                # 采样率
        RECORD_SECONDS = 10         # 采样时间
        WAVE_OUTPUT_FILENAME = filepath   #文件存储路径
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("*"*10, "recording begins：please input audio in 20 seconds! ")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("*"*10, "recording end\n")

        stream.stop_stream()
        stream.close()
        p.terminate()

        # 以WAV格式保存音频
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return "succeed recording!"
    elif aa == str("no"):
        exit()
    else:
        return ("incorrect input，please choose again!")


# 获取申请的token
def get_token():
    url = "https://openapi.baidu.com/oauth/2.0/token"
    grant_type = "client_credentials"
    api_key = "PGphNioub6eYG13TjkKWP8LE"                     # 自己申请的应用
    secret_key = "ST46oX71GGdbb4AdyuW5r5ollC7uHs67"            # 自己申请的应用
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


#get_audio(in_path)
# 测试代码
# filename = "./speechs/input.wav"
# signal = open(filename, "rb").read()
# rate = 16000
# token = get_token()
# print(recognize(signal, rate, token))
