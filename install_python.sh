#!/usr/bin/env bash
set -e
# set +x

source "${SCRIPT_DIR}/helper_functions.sh"

printf -- "Install Python & dependencies...\n\n"

printf -- "WEB_USER = ${WEB_USER}\n"
printf -- "package_tool_ok = ${package_tool_ok}\n"
printf -- "Python(3) Virtual environment = ${PY_VENV}\n"


printf -- "\n\n*** APT-install for Python 3... ***\n"
if [ "$package_tool_ok" = true ]
then
	sudo apt install -y python3 python3-dev
else
	if ! command -v python3 &> /dev/null
	then
		printf -- "Could not find neither Python3 nor Apt.\n"
		fail "Python3 must be installed manually first!"
	fi
fi

printf -- "\n\n*** Create Python virtual environment... ***\n"
printf -- "(administrator rights required to create venv in shared folder)\n"
sudo python3 -m venv ${PY_VENV}
sudo chmod -R 755 ${PY_VENV}
printf -- "\nActivate the environment with 'source ${PY_VENV}/bin/activate'\n"
source ${PY_VENV}/bin/activate

printf -- "\n\n*** APT installs for Python PIP3 (Python package manager)... ***\n"
# Instead of the below 'python3-pip' install, depending on your Linux distro, it may be more reliable to follow
# instructions from https://pip.pypa.io/en/stable/installing/ :
# curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
# [sudo] python3 /tmp/get-pip.py
if [ "$package_tool_ok" = true ]
then
	sudo apt install -y python3-pip
else
	sudo python3 -m ensurepip
	sudo python3 -m pip install --upgrade pip
fi

apt_install_or_skip python3-picamera

printf -- "\n\nUpgrade existing packages to last version:\n"
sudo pip3 list | grep -v "Package" | grep -v "\-\-\-\-\-\-\-" | cut -d ' ' -f 1 | xargs -n1 sudo pip3 install -U

printf -- "\n\n*** PIP Installs: ***\n"

printf -- "- pydevd for Python remote debugging\n"
# check https://raspberrypi.stackexchange.com/questions/70018/remotely-debug-python-code-on-pi-using-eclipse-in-windows for further details
sudo pip3 install -U pydevd

printf -- "- gpiozero for CPU temperature reading and other GPIO\n"
sudo pip3 install gpiozero

printf -- "- RPi.GPIO for input/output management\n"
sudo pip3 install RPi.GPIO || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

printf -- "- Adafruit_GPIO for input/output management\n"
sudo pip3 install Adafruit_GPIO || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

# note: if issues for Adafruit_GPIO install, launch with "python -m pip" instead of "pip"
printf -- "- tsl2561 for sensors reading\n"
# A tutorial? about how to use the pressure/humidity/light/temperature sensors with I2C/SPI:
# https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all
# https://pypi.org/project/tsl2561/
sudo pip3 install tsl2561 || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

printf -- "- bluetin.io for HC-SR04 distance sensor reading\n"
sudo pip3 install Bluetin_Echo || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

printf -- "- svg.charts for drawing SVG graphics on web server\n\n"
sudo pip3 install svg.charts

# Uncomment below to update all pip packages:
# sudo pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 sudo pip3 install -U
# sudo pip3 list | grep -v "Package" | grep -v "\-\-\-\-\-\-\-" | cut -d ' ' -f 1 | xargs -n1 sudo pip3 install -U

# sudo pip3 install mariadb
sudo pip3 install pymysql


# Replaced by apt install (preferable)
# sudo pip3 install psycopg2

printf -- "\n\n*** Install BMP sensors library... ***\n"
cd /tmp
# sudo apt-get install git build-essential python-dev python-smbus
# Remove any pre-existing folder:
sudo rm -rf /tmp/Adafruit_Python_BMP
printf -- "*** BMP sensors: cloning... ***\n\n"
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
# printf -- "\n*** BMP sensors: Python 2... ***\n\n"
# sudo python setup.py install || printf -- "Ignored errors. Ok if not run on Raspberry.\n"
printf -- "\n*** BMP sensors: Python 3... ***\n\n"
sudo python3 setup.py install || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

# Executed on dev machine / includes GitHub projet:
# mkdir -p ~/workspace/meteo/src/lib
# git clone https://github.com/adafruit/Adafruit_Python_BMP.git


# After an upgrade of Python3 on Synology NAS, modules are dropped =>
# curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
# PATH=$PATH:/var/packages/py3k/target/usr/local/bin
# PATH=$PATH:/volume1/@appstore/MariaDB10/usr/local/mariadb10/bin
# sudo python3 /tmp/get-pip.py
# sudo python3 -m pip install pydevd gpiozero svg.charts
# sudo python3 -m pip install PyMySQL
# TODO @NAS: Uninstall if still unecessary: PhpMyAdmin ( < Web Station    & < Php7.2?)
