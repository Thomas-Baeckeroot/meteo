#!/usr/bin/env bash
set -e
set -x

echo "\n\n*** Install PIP (package manager)... ***"
curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python /tmp/get-pip.py

echo "\n\n*** Install postgresql database... ***"
sudo apt install -y postgresql libpq-dev python-psycopg2 && pip install psycopg2

# check https://raspberrypi.stackexchange.com/questions/70018/remotely-debug-python-code-on-pi-using-eclipse-in-windows for further details
echo "\n\n*** Install pydevd for Python remote debugging... ***"
sudo pip install pydevd

echo "\n\n*** Install gpiozero for CPU temperature reading and other GPIO... ***"
pip install gpiozero

# A tutorial? about how to use the pressure/humidity/light/temperature sensors with I2C/SPI:
# https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all

# https://pypi.org/project/tsl2561/
echo "\n\n*** Install RPi.GPIO for input/output management... ***"
pip install RPi.GPIO
# echo "\n\n*** Install Adafruit_GPIO for input/output management... ***"
# python -m pip install Adafruit_GPIO  # Don't know why it was not working without calling by 'python -m'
echo "\n\n*** Install tsl2561 for sensors reading... ***"
pip install tsl2561

# As detailed https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md
echo "\n\n*** Install gpac to get 'MP4Box' command for webcam video captures... ***"
sudo apt install -y gpac

# it has been installed the 2019-06 version by:
echo "\n\n*** Install libmicrohttpd12 for tests with 'motion'... ***"  # required yet?
sudo apt install -y libmicrohttpd12
## from https://github.com/Motion-Project/motion/releases
#echo "\n\n*** Install pi_stretch_motion for ?video-motion-detection?... ***"
#sudo dpkg -i pi_stretch_motion_4.2.2-1_armhf.deb

echo "\n\n*** Create forlder where images will be saved... ***"
mkdir /home/pi/meteo/captures/

# Executed on dev machine / includes GitHub projet:
# mkdir ~/workspace/meteo/src/lib 
# git clone https://github.com/adafruit/Adafruit_Python_BMP.git

echo "-"
echo "Add below line to crontab of user 'pi':"
echo "* * * * *  /home/pi/meteo/src/main/py/periodical_sensor_reading.py >> /var/log/meteo.log 2>&1"
echo "-"
echo "Add below 3 lines at the end of /etc/rc.local, before last 'exit 0':"
echo "/home/pi/meteo/src/main/py/watchdog_gpio.py >> /var/log/watchdog_gpio.log 2>&1 &"
echo "sudo su - pi -c \"/home/pi/meteo/src/main/py/video_capture_on_motion.py >> /home/pi/meteo/video.log 2>&1\" &"
echo "sudo su - web -c \"/home/pi/meteo/src/main/py/server3.py >> /home/web/server3.log\" &"
echo "-"
echo "With 'sudo raspi-config', you can configure to start without graphical GUI"

## Also useful for developping from ssh command-line:

# sudo apt install vim vim-addon-manager

## mkdir -p ~/.vim/autoload ~/.vim/bundle
## curl -LSso ~/.vim/autoload/pathogen.cim https://tpo.pe/pathogen.vim
## echo "execute pathogen#infect()" >> ~/.vimrc
## echo "syntax on" >> ~/.vimrc
## echo "filetype plugin indent on" >> ~/.vimrc
## cd ~/.vim/bundle
## git clone https://github.com/klen/python-mode.git

chmod +x ~/meteo/src/main/py/server3.py