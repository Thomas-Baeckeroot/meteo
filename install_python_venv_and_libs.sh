#!/usr/bin/env bash
set -e
set -x

PY_VENV=$1

printf -- "\n\n*** Create Python virtual environment '%s'... ***\n" "${PY_VENV}"
# printf -- "(administrator rights required to create venv in shared folder)\n"
python3 -m venv "${PY_VENV}"
chmod -R 755 "${PY_VENV}"
printf -- "\nActivate the environment with 'source %s/bin/activate'\n" "${PY_VENV}"
source "${PY_VENV}/bin/activate"

printf -- "\n\nUpgrade existing packages to last version:\n"
python3 -m pip list | grep -v "Package" | grep -v "\-\-\-\-\-\-\-" | cut -d ' ' -f 1 | xargs -n1 pip3 install -U

printf -- "\n\n*** PIP Installs: ***\n"

printf -- "- pydevd for Python remote debugging\n"
# check https://raspberrypi.stackexchange.com/questions/70018/remotely-debug-python-code-on-pi-using-eclipse-in-windows for further details
pip3 install -U pydevd

printf -- "- gpiozero for CPU temperature reading and other GPIO\n"
pip3 install gpiozero

printf -- "- RPi.GPIO for input/output management\n"
pip3 install RPi.GPIO || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

printf -- "- Adafruit_GPIO for input/output management\n"
pip3 install Adafruit_GPIO || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

printf -- "- Adafruit_GPIO INSTALLED\n"

# note: if issues for Adafruit_GPIO install, launch with "python -m pip" instead of "pip"
printf -- "- tsl2561 for sensors reading\n"
# A tutorial? about how to use the pressure/humidity/light/temperature sensors with I2C/SPI:
# https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all
# https://pypi.org/project/tsl2561/
pip3 install tsl2561 || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

printf -- "- bluetin.io for HC-SR04 distance sensor reading\n"
pip3 install Bluetin_Echo || printf -- "Ignored errors. Ok if not run on Raspberry.\n"

printf -- "- svg.charts for drawing SVG graphics on web server\n\n"
pip3 install svg.charts

printf -- "- PyMySQL for database connection\n\n"
# pip3 install mariadb
pip3 install pymysql

printf -- "\n\n*** Install BMP sensors library... ***\n"
INITIAL_DIR=$(pwd)
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
python3 setup.py install || printf -- "Ignored errors. Ok if not run on Raspberry.\n"
cd "${INITIAL_DIR}"

exit 0