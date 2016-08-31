#!/bin/sh
{
sudo kill $(ps aux | grep '[p]ython gevent_run.py' | awk '{print $2}')
}
sleep 5
cd /home/pi/babaeletronica
sudo python gevent_run.py &
