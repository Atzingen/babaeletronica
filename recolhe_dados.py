# -*- coding: latin-1 -*-
import os
from baba_bd import *
try:
    import Adafruit_DHT
    import Adafruit_BMP.BMP085 as BMP085
    import RPi.GPIO as gp
except:
    pass

# Configuracoes dos pinos gpio para o controle do led IF
gp.setmode(gp.BCM)
gp.setup(23,gp.OUT)

def toogle_led(LEDs_status):
    gp.output(23,LEDs_status)


################################ Ambiente ######################################################
def leitura():
    print 'leitura'
    try:
        sensor = Adafruit_DHT.DHT22
        pin = 14
        [umidade, temperatura] = Adafruit_DHT.read_retry(sensor, pin)
        if isinstance(umidade, float) and isinstance(temperatura, float):
            return [umidade, temperatura]
        else:
            return [-10, -10]
    except:
        return [-10, -10]


def pressao():
	try:
		sensor = BMP085.BMP085()
		temperatura = sensor.read_temperature()
		pressao = sensor.read_pressure()/100.0
		return temperatura, pressao
	except:
		return -10, -10



############################### Rasberry status ###################################################
# Return Ping latency at www.google.com
def ping_latency():
    try:
        pingAddress = 'www.google.com'
        rawPingFile = os.popen('ping -c 5 %s' % (pingAddress))
        rawPingData = rawPingFile.readlines()
        rawPingFile.close()
        if len(rawPingData) < 2:
            # Failed to find a DNS resolution or route
            failed = True
            latency = 0
        else:
            index = rawPingData[1].find('time=')
            if index == -1:
                # Ping failed or timed-out
                failed = True
                latency = 0
            else:
                # We have a ping time, isolate it and convert to a number
                failed = False
                latency = rawPingData[1][index + 5:]
                latency = latency[:latency.find(' ')]
                latency = float(latency)
        return latency, failed
    except:
        return 0, False

# Return CPU temperature as a character string
def getCPUtemperature():
    try:
        res = os.popen('vcgencmd measure_temp').readline()
        return float((res.replace("temp=","").replace("'C\n","")))
    except:
        return 0

# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    try:
        p = os.popen('free')
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i==2:
                return ( [ float(i) for i in line.split()[1:4] ] )
    except:
        return [0,0,0]

# Return % of CPU used by user as a character string
def getCPUuse():
    try:
        a = str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())
        return float(a)
    except:
        return 0

# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def getDiskSpace():
    try:
        p = os.popen("df -h /")
        i = 0
        while 1:
            i = i +1
            line = p.readline()
            if i==2:
                data = line.split()[1:5]
                res = []
                for d in data:
                    if 'G' in d:
                        res.append(float(d.replace('G',''))*10E10)
                    elif 'M' in d or 'm' in d:
                        res.append(float(d.replace('M',''))*10E6)
                    elif 'k' in d or 'K' in d:
                        res.append(float(d.replace('K',''))*10E3)
                    elif '%' in d:
                        res.append(float(d.replace('%','')))
                return res
    except:
        return [0,0,0,0]

def raspberry_dados():
    ping     = ping_latency()
    cpu_temp = getCPUtemperature()
    ram      = getRAMinfo()
    cpu_use  = getCPUuse()
    Disk     = getDiskSpace()
    return ping, cpu_temp, ram, cpu_use, Disk


if __name__ == '__main__':
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
