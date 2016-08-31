from recolhe_dados import *
from baba_bd import *
#import datetime, os
# import linecache
# import sys

try:
	ping, cpu_temp, ram, cpu_use, Disk = raspberry_dados()
	resultado  = leitura()
	umidade, temperatura = resultado[0], resultado[1]
	resultado2 = pressao()
	temp_p, pressao = resultado2[0], resultado2[1]
	adiciona_dados_rp(ping[0], ping[1], cpu_temp, ram[0], ram[1], ram[2], cpu_use, Disk[0], Disk[1], Disk[2], Disk[3])
	adiciona_dados_ambiente(temperatura, umidade, pressao, temp_p)
except Exception, e:
	pass

