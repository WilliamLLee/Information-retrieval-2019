import pyaudio
import wave
input_filename = "input.wav"               # 麦克风采集的语音输入
input_filepath = "./speechs/"              # 输入文件的path
in_path = input_filepath + input_filename

def get_audio(filepath):
    aa = str(input("=>start recording？   （yes/no） :"))
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

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    elif aa == str("no"):
        exit()
    else:
        print("incorrect input，please choose again!")

get_audio(in_path)

