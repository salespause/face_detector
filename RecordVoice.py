#!/usr/bin/env python
# coding:UTF-8
import subprocess
from datetime import datetime

# 音声をレコードするためのクラス
class RecordVoice:
    def __init__(self):
        self.isRecording = 0
        print("init")
        
    def startRecording(self):
        self.isRecording = 1
        fileName = "a.wav"
        subprocess.call("arecord -f cd -c 2 -D dsnoop " + fileName, shell=True)
        # subprocess.call("touch " + fileName, shell=True) # ファイル書き出し(テスト)
        
    def endRecording(self):
        print("send voice to server")
        subprocess.call("pkill arecord")
        # ここでwav消す前に送る
        cmd = 'curl -X POST -u 85575991-f440-415f-90a8-1cdca5b16f84:O7i5matSrnoC --header "Content-Type: audio/wav" --header "Transfer-Encoding: chunked" --data-binary a.wav "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?timestamps=true&word_alternatives_threshold=0.9&keywords=%22colorado%22%2C%22tornado%22%2C%22tornadoes%22&keywords_threshold=0.5&continuous=true&model=ja-JP_BroadbandModel"'
        watsonRet = subprocess.check_output(cmd, shell=True)
        print(watsonRet) 
        print("remove wav from dir")
        subprocess.call("rm a.wav")
        self.isRecording = 0