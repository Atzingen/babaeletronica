# -*- coding: latin-1 -*-
import time
import datetime
import sqlite3
import scipy
import sys
#from recolhe_dados import *

def cria_tabela_ambiente():
    db = sqlite3.connect('babaeletronica.db')
    queryCurs = db.cursor()
    queryCurs.execute('''CREATE TABLE IF NOT EXISTS ambiente
    (id INTEGER PRIMARY KEY,tempo TIMESTAMP DEFAULT (DATETIME('now')),temperatura REAL,umidade REAL, pressao REAL, temp_p REAL)''')
    db.commit()
    db.close()

def cria_tabela_dados_rp():
    db = sqlite3.connect('babaeletronica.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dados_rp
    (id INTEGER PRIMARY KEY,tempo TIMESTAMP DEFAULT (DATETIME('now')),ping0 REAL,ping1 INTEGER,cpu_temp REAL,d REAL,ram0 REAL,ram1 REAL,ram2 REAL,cpu_use REAL,Disk0 REAL,Disk1 REAL,Disk2 REAL,Disk3 REAL)''')
    db.commit()
    db.close()

def cria_tabela_config():
    db = sqlite3.connect('babaeletronica.db')
    cursor = db.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS config (
    id INTEGER PRIMARY KEY,
    'LEDs'  INTEGER UNIQUE,
    'FrameRate' INTEGER UNIQUE,
    'Rotacao'   INTEGER UNIQUE,
    'Vflip' INTEGER UNIQUE,
    'Hflip' INTEGER UNIQUE,
    't_preview' NUMERIC UNIQUE,
    't_desligar'    NUMERIC UNIQUE,
    'darkice'   INTEGER UNIQUE,
    'icecast'   INTEGER UNIQUE,
    'dth22_gpio'    INTEGER UNIQUE,
    'resolucao_video'    TEXT UNIQUE,
    'resolucao_foto'    TEXT UNIQUE
    )''')
    cursor.execute(''' INSERT INTO config DEFAULT VALUES''')
    db.commit()
    db.close

def cria_tabela_usuarios():
	db = sqlite3.connect('babaeletronica.db')
	cursor = db.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
	(id INTEGER PRIMARY KEY,mail TEXT,senha TEXT,tipo INTEGER,ultimo_acesso TIMESTAMP DEFAULT (DATETIME('now')), acessos INTEGER DEFAULT 0)''')
	db.commit()
	db.close()

def atualiza_acesso_usuario(chave_primaria):
	tempo  = datetime.datetime.now()
	db = sqlite3.connect('babaeletronica.db')
	cursor = db.cursor()
	cursor.execute('''UPDATE usuarios SET ultimo_acesso = ? WHERE id = ?''',(tempo,chave_primaria,))
	db.commit()
	db.close()
	if cursor.rowcount > 0:
		return True
	else:
		return False

def adiciona_usuario(mail,senha,tipo):
	try:
		a, b, c = checa_usuario(mail)
		if (a < 1):
			db = sqlite3.connect('babaeletronica.db')
			cursor = db.cursor()
			t_abs = datetime.datetime.now()
			cursor.execute('''INSERT INTO usuarios (mail,senha,tipo)
								VALUES(?,?,?)''',(mail,senha,tipo))
			db.commit()
			db.close()
			if cursor.rowcount > 0:
				return 1
			else:
				return 0
		else:
			return -1
	except:
		return 0

def checa_usuario(mail):
	try:
		db = sqlite3.connect('babaeletronica.db')
		cursor = db.cursor()
		cursor.execute('''SELECT * FROM usuarios WHERE mail = ?''',(mail,))
		row = cursor.fetchone()
		db.close()
		if row:
			return row[0], row[2], row[3]
		else:
			return None, None, None
	except:
		return None, None, None

def lista_usuarios():
	try:
		db = sqlite3.connect('babaeletronica.db')
		cursor = db.cursor()
		cursor.execute('''SELECT * FROM usuarios ''')
		rows = cursor.fetchall()
		db.close()
		return rows
	except:
		return None

def deleta_usuario(chave_primaria):
	try:
		db = sqlite3.connect('babaeletronica.db')
		cursor = db.cursor()
		cursor.execute('''DELETE FROM usuarios WHERE id = ? ''', (chave_primaria,))
		db.commit()
		db.close()
		if cursor.rowcount > 0:
			return True
		else:
			return False
	except:
		return None

def limpa_tabela_dados_rp():
    db = sqlite3.connect('babaeletronica.db')
    cursor = db.cursor()
    cursor.execute(''' DELETE FROM dados_rp ''')
    db.commit()
    db.close()

def limpa_tabela_config():
    db = sqlite3.connect('babaeletronica.db')
    cursor = db.cursor()
    cursor.execute(''' DELETE FROM config ''')
    db.commit()
    db.close()

def limpa_tabela_ambiente():
    db = sqlite3.connect('babaeletronica.db')
    cursor = db.cursor()
    cursor.execute(''' DELETE FROM ambiente ''')
    db.commit()
    db.close()

def atualiza_config(IDS,valores):
    try:
        db     = sqlite3.connect('babaeletronica.db')
        cursor = db.cursor()
        tempo  = datetime.datetime.now()
        for ID, valor in zip(IDS, valores):
            if ID == 'resolucao_video' or ID == 'resolucao_foto':
                comando = 'UPDATE config SET ' + str(ID) + ' = ' + '"' + str(valor) + '"' + ' WHERE id = 1'
            else:
                comando = 'UPDATE config SET ' + str(ID) + ' = ' + str(valor) + ' WHERE id = 1'
            cursor.execute(comando)
        db.commit()
        db.close()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except:
        return False

def adiciona_dados_ambiente(temperatura,umidade,pressao,temp_p):
    try:
        db     = sqlite3.connect('babaeletronica.db')
        cursor = db.cursor()
        tempo  = datetime.datetime.now()
        cursor.execute('''INSERT INTO ambiente (tempo,temperatura,umidade,pressao,temp_p) VALUES(?,?,?,?,?)''',(tempo,temperatura,umidade,pressao,temp_p))
        db.commit()
        db.close()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except:
        return False

def adiciona_dados_rp(ping0,ping1,cpu_temp,ram0,ram1,ram2,cpu_use,Disk0,Disk1,Disk2,Disk3):
    '''ping 2 valres [0] (float) ping em ms [1] (boolean) conecção ou nao
    cpu_temp 1 valor [0] (float)
    ram 3 valores [0] (float) total, [0] (float) usado, [0] (float) free
    cpu_use 1 valor [0] (float) uso da cpu
    Disk 4 valores [0] (float) espaço total, [1] (float) espaço usado, [2] (float) espaço livre [3] (float) porcentagem de uso
    data -> datetime.now()
    '''
    try:
        tempo  = datetime.datetime.now()
        db = sqlite3.connect('babaeletronica.db')    # cria uma conecção com o bando de dados (com)
        cursor = db.cursor()                            # cursor, para enviar os comandos sql
        cursor.execute('''INSERT INTO dados_rp (tempo,ping0,ping1,cpu_temp,ram0,ram1,ram2,cpu_use,Disk0,Disk1,Disk2,Disk3) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)''',(tempo,ping0,ping1,cpu_temp,ram0,ram1,ram2,cpu_use,Disk0,Disk1,Disk2,Disk3))
        db.commit()
        db.close()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception, e:
    	#print str(e), 'except'
        return False

def retorna_dados_config():
    createDB = sqlite3.connect('babaeletronica.db')
    queryCurs = createDB.cursor()
    queryCurs.execute("SELECT * FROM config WHERE id = 1")
    createDB.commit()
    return scipy.array(queryCurs.fetchall())

def retorna_dados_ambiente():
    createDB = sqlite3.connect('babaeletronica.db')
    queryCurs = createDB.cursor()
    queryCurs.execute("SELECT * FROM ambiente ORDER BY datetime(tempo) ASC")
    createDB.commit()
    return scipy.array(queryCurs.fetchall())

def retorna_dados_raspberry():
    createDB = sqlite3.connect('babaeletronica.db')
    queryCurs = createDB.cursor()
    queryCurs.execute("SELECT * FROM dados_rp ORDER BY datetime(tempo) ASC")
    createDB.commit()
    return scipy.array(queryCurs.fetchall())
