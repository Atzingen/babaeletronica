import time
import io
import threading
import baba_bd, recolhe_dados
try:					# Para ser usado no raspberry pi
	import picamera
	class Camera(object):
		thread = None   # background thread that reads frames from camera
		frame = None  	# current frame is stored here by background thread
		last_access = 0 # time of last client access to the camera

		def initialize(self):
			if Camera.thread is None:
				# start background frame thread
				Camera.thread = threading.Thread(target=self._thread)
				Camera.thread.start()

				# wait until frames start to be available
				while self.frame is None:
					time.sleep(0)

		def get_frame(self):
			Camera.last_access = time.time()
			self.initialize()
			return self.frame

		@classmethod
		def _thread(cls):
			with picamera.PiCamera() as camera:
				# camera setup
				cfg = baba_bd.retorna_dados_config()
				cfg = baba_bd.retorna_dados_config()
				_, LEDs, FrameRate, Rotacao, Vflip, Hflip, t_preview, t_desligar, _, _, _, resolucao_video, resolucao_foto = cfg[0]
				print LEDs, FrameRate, Rotacao, Vflip, Hflip, t_preview, t_desligar, resolucao_video, resolucao_foto
				if int(LEDs) == 1:
					print "ligando o led"
					recolhe_dados.toogle_led(True)
				else:
					print "led desligado"
					recolhe_dados.toogle_led(False)
				resolucao_video_x, resolucao_video_y = resolucao_video.split('x')
				resolucao_foto_x, resolucao_foto_y = resolucao_foto.split('x')
				camera.resolution = (int(resolucao_video_x),int(resolucao_video_y))
				camera.hflip = bool(Hflip)
				camera.vflip = bool(Vflip)
				camera.rotation = int(Rotacao)
				camera.framerate = int(FrameRate)
				# camera.start_preview()
				time.sleep(float(t_preview))
				stream = io.BytesIO()
				for foo in camera.capture_continuous(stream, 'jpeg',use_video_port=True):
					# store frame
					stream.seek(0)
					cls.frame = stream.read()
					# reset stream for next frame
					stream.seek(0)
					stream.truncate()
					# if there hasn't been any clients asking for frames in
					# the last 10 seconds stop the thread
					if time.time() - cls.last_access > float(t_desligar):
						recolhe_dados.toogle_led(False)
						break
			recolhe_dados.toogle_led(False)
			cls.thread = None

except :	# para testar fora do raspberry pi
	class Camera(object):
		"""An emulated camera implementation that streams a repeated sequence of
		files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

		def __init__(self):
			self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

		def get_frame(self):
			return self.frames[int(time()) % 3]
	pass
