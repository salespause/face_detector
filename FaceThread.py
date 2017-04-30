#!/usr/bin/env python
# coding:UTF-8

import cv2
import threading
import urllib
import Post 
import json
from time import sleep
from datetime import datetime

class FaceThread(threading.Thread):
	def __init__(self, frame):
		print('[FaceThread]<init>')
		super(FaceThread, self).__init__()
		self._cascade_path = '/usr/local/opt/opencv3/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml'
		self._frame = frame

	def run(self):
		#グレースケール変
		print('[FaceThread]<run>')
		self._frame_gray = cv2.cvtColor(self._frame, cv2.COLOR_RGB2GRAY)
		#カスケード分類器の特徴量を取得する
		self._cascade = cv2.CascadeClassifier(self._cascade_path)

		#物体認識（顔認識）の実行
		self._facerect = self._cascade.detectMultiScale(self._frame_gray, scaleFactor=1.2, minNeighbors=3, minSize=(10, 10))

		if len(self._facerect) > 0:
			print('顔が検出されました。')
			self._color = (255, 255, 255) #白
			for self._rect in self._facerect:
				# 出した顔を囲む矩形の作成
				# 出力に反映される(サーバに投げるときは要注意だよね)
				cv2.rectangle(self._frame, tuple(self._rect[0:2]),tuple(self._rect[0:2] + self._rect[2:4]), self._color, thickness=2)

			#現在の時間を取得
			# self._now = datetime.now().strftime('%Y%m%d%H%M%S')
			#認識結果の保存(ここで送信する)
			# self._image_path = self._now + '.jpg'
			cv2.imwrite("facePhoto.jpg", self._frame)
			# 1. imwriteをrailsに送信する
			# 2. 結果を，nodeに送信する
			# retが帰ってきたと想定(string, "true"か"false"で)
			facePost = Post("https://notification-test.au-syd.mybluemix.net/api/v1/captured_images")
			faceID = json.loads(facePost.post("facePhoto.jpg"))["captured_image"]["id"]
			isSalseUrl = "https://notification-test.au-syd.mybluemix.net/api/v1/captured_images/" + faceID + "/check?black_list_id=1"
			result = json.loads(urllib.urlopen(isSalseUrl))["isSales"]
			nodeUrl = 'https://salespause-phone.au-syd.mybluemix.net/status/sales'
			values = {'isSalse' : result}
			data = urllib.parse.urlencode(values)
			data = data.encode('ascii') # data should be bytes
			req = urllib.request.Request(nodeUrl, data)
			with urllib.request.urlopen(req) as response:
			       the_page = response.read()
			sleep(10)
