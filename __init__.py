# -*- coding: latin-1 -*-
from flask import Flask, render_template, request, url_for, flash, redirect, Response, jsonify
from flask import *
import os, sys, datetime
from subprocess import call
import thread
from functools import wraps
import numpy as np
from camera_pi import Camera  # Requires picamera (module camera_pi.py)
import recolhe_dados, baba_bd

app = Flask(__name__)
app.secret_key = 'fsdfsdfsdfsdfsfsd'

def loggin_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to loggin first !')
			return redirect(url_for('loggin'))
	return wrap


@app.route('/loggin', methods=['GET','POST'])
def loggin():
	if 'logged_in' in session:
		return redirect(url_for('logout'))
	try:
		if request.method == 'POST':
			email = request.form['email']
			senha = request.form['senha']
			print email, senha
			#nome =  email[:email.index('@')]
			_, senha_bd, level = baba_bd.checa_usuario(email)
			if senha_bd == senha:
				session['logged_in'] = True
				session['level'] = int(level)
				flash('Voce esta logado !')
				return redirect(url_for('home'))
			else:
				flash('erro no loggin !')
				return redirect(url_for('loggin'))

		'''
		if request.form['email'] != 'admin1@admin.com' or request.form['senha'] != 'admin1':
			flash('error in loggin !')
			return redirect(url_for('loggin'))
		else:
			session['logged_in'] = True
			flash('loggin ok !')
			return redirect(url_for('home'))
		'''
	except:
		pass
	return render_template('loggin.html')


@app.route('/logout')
@loggin_required
def logout():
	session.pop('logged_in',None)
	flash('you are logged out !')
	return redirect(url_for('home'))

@app.route('/')
@loggin_required
def home():
    return render_template('index.html')

@app.route('/camera')
@loggin_required
def camera():
	return render_template('camera.html')

@app.route('/audio')
@loggin_required
def audio():
	return render_template('audio.html')

@app.route('/ajustes', methods=['GET','POST'])
@loggin_required
def ajustes():
	if request.method == 'POST':
		cfg = baba_bd.retorna_dados_config()
		_, LEDs, FrameRate, Rotacao, Vflip, Hflip, t_preview, t_desligar, darkice, icecast, dth22_gpio, resolucao_video, resolucao_foto = cfg[0]
		try:
			print request.form['id'], request.form['valor']
		except:
			pass
		if str(request.form['id']) == 'restart-wsgi':
			thread.start_new_thread(comando,('sudo /home/pi/babaeletronica/./start_gevent.sh',))
		elif request.form['id'] == 'reiniciar':
			thread.start_new_thread(comando,('sudo reboot',))
		elif request.form['id'] == 'desligar':
			thread.start_new_thread(comando,('sudo halt',))
		elif request.form['id'] == 'limpa-ram':
			thread.start_new_thread(comando,('sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"',))
		elif request.form['id'] == 'envia-comando':
			texto = str(request.form['texto'])
			thread.start_new_thread(comando,(texto,))
		elif request.form['id'] == 'resolucao_video':
			baba_bd.atualiza_config(['resolucao_video'],[str(request.form['valor'])])
		elif request.form['id'] == 'resolucao_foto':
			baba_bd.atualiza_config(['resolucao_foto'],[str(request.form['valor'])])
		elif request.form['id'] == 'leds0':
			baba_bd.atualiza_config(['LEDs'],[0])
		elif request.form['id'] == 'leds1':
			baba_bd.atualiza_config(['LEDs'],[1])
		elif request.form['id'] == 'FrameRate':
			baba_bd.atualiza_config(['FrameRate'],[int(request.form['valor'])])
		elif request.form['id'] == 'Rotacao':
			baba_bd.atualiza_config(['Rotacao'],[int(request.form['valor'])])
		elif request.form['id'] == 'Hflip0':
			baba_bd.atualiza_config(['Hflip'],[0])
		elif request.form['id'] == 'Hflip1':
			baba_bd.atualiza_config(['Hflip'],[1])
		elif request.form['id'] == 'Vflip0':
			baba_bd.atualiza_config(['Vflip'],[0])
		elif request.form['id'] == 'Vflip1':
			baba_bd.atualiza_config(['Vflip'],[1])
		elif request.form['id'] == 'tempo_preview':
			baba_bd.atualiza_config(['t_preview'],[float(request.form['valor'])])
		elif request.form['id'] == 'tempo_desligar':
			baba_bd.atualiza_config(['t_desligar'],[float(request.form['valor'])])
		elif request.form['id'] == 'botao-darkice':
			if darkice == 1:
				thread.start_new_thread(comando,('''sudo kill $(ps aux | grep '[d]arkice' | awk '{print $2}')''',))
				baba_bd.atualiza_config(['darkice'],[0])
			else:
				thread.start_new_thread(comando,('darkice',))
				baba_bd.atualiza_config(['darkice'],[1])
		elif request.form['id'] == 'botao-icecast':
			if icecast == 1:
				thread.start_new_thread(comando,('sudo service icecast2 stop',))
				baba_bd.atualiza_config(['icecast'],[0])
			else:
				thread.start_new_thread(comando,('sudo service icecast2 start',))
				baba_bd.atualiza_config(['icecast'],[1])
		elif request.form['id'] == 'dth22_gpio':
			baba_bd.atualiza_config(['dth22_gpio'],[float(request.form['valor'])])
		return redirect(url_for('teste'))
		#return make_response("",204)
	else:
		users = baba_bd.lista_usuarios()
		return render_template('ajustes.html',users=users)

def comando(texto):
	os.system(texto)

@app.route('/teste')
@loggin_required
def teste():
	dth22_umidade, dth22_temp = recolhe_dados.leitura()
	bmp_temperatura, bmp_pressao = recolhe_dados.pressao()
	ram_total,ram_usada,ram_livre = recolhe_dados.getRAMinfo()
	uso_cpu = recolhe_dados.getCPUuse()
	temp_cpu = recolhe_dados.getCPUtemperature()
	sd_total, sd_usado, sd_livre, _ = recolhe_dados.getDiskSpace()
	a = baba_bd.retorna_dados_config()
	_,LEDs,FrameRate,Rotacao,Vflip,Hflip,t_preview,t_desligar,darkice,icecast,dth22_gpio, resolucao_video, resolucao_foto = a[0]
	valores = {'temp_cpu': temp_cpu,
			'uso_cpu':uso_cpu,
			'ram_livre': ram_livre,
			'ram_usada':ram_usada,
			'ram_total':ram_total,
			'sd_livre':sd_livre,
			'sd_usado':sd_usado,
			'sd_total':sd_total,
			'resolucao_video': resolucao_video,
			'resolucao_foto': resolucao_foto,
			'leds': LEDs,
			'FrameRate': FrameRate,
			'Rotacao': Rotacao,
			'flipH': Hflip,
			'flipV': Vflip,
			'tempo_preview': t_preview,
			'tempo_desligar': t_desligar,
			'darkice': darkice,
			'icecast': icecast,
			'dth22_gpio': dth22_gpio,
			'dth22_temp': dth22_temp,
			'dth22_umidade': dth22_umidade,
			'bmp_pressao': bmp_pressao,
			'bmp_temperatura': bmp_temperatura}
	return jsonify(result=valores)

@app.route('/ambiente')
@loggin_required
def ambiente():
	d = baba_bd.retorna_dados_ambiente()
	dados = []
	for dado in d:
		data = datetime.datetime.strptime(dado[1], "%Y-%m-%d %H:%M:%S.%f")
		dados.append([data,float(dado[2]),float(dado[3]),float(dado[4]),float(dado[5])])
	return render_template('ambiente.html',dados=dados)

@app.route('/video_feed')
@loggin_required
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == '__main__':
	app.run(host='0.0.0.0',threaded=True,debug=True, port=5001)
