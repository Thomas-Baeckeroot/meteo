#!/usr/bin/env bash
set -e
# set -x  # uncomment this line for debugging...

source "${SCRIPT_DIR}/helper_functions.sh"

printf -- "Install Python & dependencies...\n\n"

printf -- "WEB_USER = %s\n" "${WEB_USER}"
printf -- "package_tool_ok = %s\n" "${package_tool_ok}"
printf -- "Python(3) Virtual environment = %s\n" "${PY_VENV}"

# Check for Python3
printf -- "\n\n*** APT-install for Python 3... ***\n"
if [ "$package_tool_ok" = true ]
then
  printf -- "\nAdministrator password is required for some actions: installing necessary package on system, creating venv, ...\n"
	sudo apt install -y python3 python3-dev
else
	if ! command -v python3 &> /dev/null
	then
		printf -- "Could not find neither Python3 nor Apt.\n"
		fail "Python3 must be installed manually first!"
	fi
fi

printf -- "\n\n*** APT installs for Python PIP3 (Python package manager)... ***\n"
printf -- "(administrator/sudo password may be required)\n"
# Instead of the below 'python3-pip' install, depending on your Linux distro, it may be more reliable to follow
# instructions from https://pip.pypa.io/en/stable/installing/ :
# curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
# [sudo] python3 /tmp/get-pip.py
if [ "$package_tool_ok" = true ]
then
	sudo apt install -y python3-pip
	sudo apt install -y python3-venv
else
	sudo python3 -m ensurepip
	sudo python3 -m pip install --upgrade pip
fi

# Create virtual environment with required libraries
sudo "${SCRIPT_DIR}/install_python_venv_and_libs.sh" "${PY_VENV}"
# sudo sh -c ./install_python_venv_and_libs.sh
# sudo sh -c ./install_python_venv_and_libs.sh

printf -- "\n\n*** Install Python3 camera module... ***\n"
apt_install_or_skip python3-picamera

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

