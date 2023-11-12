#!/usr/bin/env bash
set -e
set +x
# set -x

# Constants
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
printf -- "Script directory: '%s'\n" "${SCRIPT_DIR}"
START_DIR=$(pwd)
source "${SCRIPT_DIR}/bin/helper_functions.sh"

function install_config_files() {
  if [ -f "${HOME}/.config/susanoo_WeatherStation.conf" ]; then
    printf -- "An existing config file has been found\n"
    printf -- "Here is a diff of current version vs. template:\n"
    diff "${HOME}/.config/susanoo_WeatherStation.conf" "${SCRIPT_DIR}/bin/susanoo_WeatherStation_template.conf"
  else
    printf -- "No pre-existing config file found\n"
    cp "${SCRIPT_DIR}/bin/susanoo_WeatherStation_template.conf" "${HOME}/.config/susanoo_WeatherStation.conf"
    printf -- "New config file has been copied for user collecting the sensors data.\n"
  fi
  printf -- "After install script is done, adjust it with:\n"
  printf -- "vi %s/.config/susanoo_WeatherStation.conf\n\n" "${HOME}"
  read -r -p "Press Enter to continue..."

  if [ -f "${HOME}/../${WEB_USER}/.config/susanoo_WeatherStation.conf" ]; then
    printf -- "An existing config file has been found\n"
    printf -- "Here is a diff of current version vs. template:\n"
    diff "${HOME}/../${WEB_USER}/.config/susanoo_WeatherStation.conf" "${SCRIPT_DIR}/bin/susanoo_WeatherStation_template_Web.conf"
  else
    printf -- "No pre-existing config file found\n"
    cp "${SCRIPT_DIR}/bin/susanoo_WeatherStation_template_Web.conf" "${HOME}/../${WEB_USER}/.config/susanoo_WeatherStation.conf"
    sudo chown "${WEB_USER}" "${HOME}/../${WEB_USER}/.config/susanoo_WeatherStation.conf"
    sudo chgrp "${WEB_USER}" "${HOME}/../${WEB_USER}/.config/susanoo_WeatherStation.conf"
    # fixme Depending on system, the upper command may fail (when group for user is different than username).
    printf -- "New config file has been copied for web server.\n"
  fi
  printf -- "After install script is done, adjust it with:\n"
  printf -- "vi %s/.config/susanoo_WeatherStation.conf\n\n" "${HOME}/../${WEB_USER}"
  read -r -p "Press Enter to continue..."
}


# todo Below attributions should be replaced by a call to func. that manages a config file ~/.config/susanoo_WeatherStation.conf (GPIO numbers also could be informed there)
# Parsing of .ini/.conf files from bash is described:
#   here:     https://ajdiaz.wordpress.com/2008/02/09/bash-ini-parser/
#   or there: https://github.com/rudimeier/bash_ini_parser
printf -- "\n"
WEB_USER=$(ask_with_default "Inform user to run the Web server or press ENTER for default" "web")

printf -- "\nInform user to run the weather station\n(by default: user who launched the script, usually \"pi\" for default user on Raspberry Pi...)\n"
INSTALL_USER=$(ask_with_default "or press ENTER for default" "$(whoami)")

printf -- "\n"
PY_VENV=$(ask_with_default "Inform Python virtual environment path or press ENTER for default" "/usr/local/share/susanoo-py-venv")

# Test if the 'apt' package tool is available on running system:
package_tool_ok=true  # used later in install_python.sh
if ! command -v apt &> /dev/null
then
	printf -- "No 'apt' tool found.\n"
	printf -- "(all right if installing on unusual places such as Synology NAS,  etc...)\n"
	# Below variable package_tool_ok is used later in install_python.sh
	# shellcheck disable=SC2034
	package_tool_ok=false
fi

source "${SCRIPT_DIR}/install_python.sh"

# This script can be adapted to be executed from a Synology NAS to use it as web-server
# Pre-requisites:
# - activate ssh and connect as admin
# - add SynoCommunity as Package Sources (cf. https://synocommunity.com/ for more information).
# - add git package
# command should be 'synopkg install_from_server py3k', 'synopkg install_from_server MariaDB10'

printf -- "Installing MariaDB (database server and required Connector-C, etc...)...\n"
apt_install_or_skip mariadb-server
apt_install_or_skip libmariadb-dev

printf -- "\n\n*** APT installs for:... ***\n"
printf -- "- gpac to get 'MP4Box' command for webcam video captures\n"
# As detailed https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md
printf -- "Installing multimedia...\n"
apt_install_or_skip gpac

## Also useful for developing from ssh command-line:
# sudo apt install vim vim-addon-manager

## mkdir -p ~/.vim/autoload ~/.vim/bundle
## curl -LSso ~/.vim/autoload/pathogen.cim https://tpo.pe/pathogen.vim
## echo "execute pathogen#infect()" >> ~/.vimrc
## echo "syntax on" >> ~/.vimrc
## echo "filetype plugin indent on" >> ~/.vimrc
## cd ~/.vim/bundle
## git clone https://github.com/klen/python-mode.git

printf -- "\n\n*** Create folder where images will be saved... ***\n"
mkdir -p "${HOME}/meteo/captures/"

# Executed on dev machine / includes GitHub project:
# mkdir -p ~/workspace/meteo/src/lib
# git clone https://github.com/adafruit/Adafruit_Python_BMP.git

printf -- "\n\n*** User to run web-server from... ***\n"

if id "${WEB_USER}" &>/dev/null; then
  printf -- "User \"%s\" already exists. No need to create it.\n" "${WEB_USER}"
else
  printf -- "\nUser \"%s\" does not exist but is required to run the web-server.\n" "${WEB_USER}"
  # Ask for confirmation before creating the user
  if ask_confirmation "Create user \"${WEB_USER}\" to run web-server from? (you would be asked for a new password for this user)" "yes"; then
    sudo adduser "${WEB_USER}"  || printf -- "ERROR! Does user \"%s\" already exist?!\n" "${WEB_USER}"
    # extra option can be used: [--disabled-password]
    # This will be the user running the web server. It should have the bare minimum accesses for security reasons.
  else
    printf -- "User creation canceled.\n"
  fi
fi

source "${SCRIPT_DIR}/bin/create_server_pages.sh" "${HOME}" "${WEB_USER}"

if ask_confirmation "Should we create database?" "yes"; then
  printf -- "Create database...\n"
  #MariaDB
  sudo mariadb -u root -e "CREATE DATABASE meteo;"  # || printf -- "Ignoring error and proceeding: database already existing?\n"
  sudo mariadb -u root -e "CREATE USER '${INSTALL_USER}'@'localhost' IDENTIFIED BY 'SetRandomPassword123';"
  sudo mariadb -u root -e "GRANT all privileges on meteo.* TO '${INSTALL_USER}'@'localhost';"
  sudo mariadb -u root -e "CREATE USER 'web'@'localhost' IDENTIFIED BY 'SetRandomPassword123';"
  sudo mariadb -u root -e "GRANT SELECT on meteo.* TO 'web'@'localhost';"
  # To check users:        SELECT Host, User FROM mysql.user;
  mariadb meteo < "${HOME}/meteo/bin/db_initialization.sql"  # || printf -- "Ignoring error and proceeding...\n"

  printf -- "\n"
  printf -- "In order to use 'remote:' sensors (multiple weather stations/servers),\n"
  printf -- "you would need to configure your database to accept external connections.\n"
  printf -- "Check 'Activate remote access' for your database.\n"
  printf -- "For MySQL and MariaDB, comment parameter 'bind-address' that limit access to those IP\n"
  printf -- "in file below:\n"
  printf -- "\tcat /etc/mysql/my.cnf\n"
  printf -- "\n"
  printf -- "Appropriate user should also be created like:\n"
  printf -- "$ sudo mysql -u root\n"
  printf -- "> CREATE USER 'remote_pi'@'192.168.0.{server-IP}' IDENTIFIED BY 'SetRandomPassword123';\n"
  printf -- "> GRANT all privileges on meteo.* TO 'remote_pi'@'192.168.0.{server-IP}';\n"
  printf -- "\n"

  if [[ "${WEB_USER}" != "${INSTALL_USER}" ]] ; then
    # FIXME Below is for PostGreSQL, must be adapted for mariadb
    createuser "${WEB_USER}" --no-superuser --no-createdb --no-createrole || printf -- "Ignoring error and proceeding: DB user already exists?\n"
  fi
  # FIXME Below was used for PostgreSQL, the same command will probably be required for MariaDB/MySQL
  # psql --dbname meteo --command "GRANT SELECT ON ALL TABLES IN SCHEMA public TO ${WEB_USER};"
fi


install_config_files


printf -- "\n\n*** Setup startup to launch Web server... ***\n"
# get location of '/etc/rc.d' for this system:
init_script_folder=$(get_init_script_folder)
if [ "${init_script_folder}" = "${UNKNOWN_LOCATION_ERROR}" ]; then
  printf -- "Initialization script folder not found. Please install manually.\n"
  read -r -p "Press Enter to continue..."
else
  if ask_confirmation "Should we make web server launched at startup?" "yes"; then
    # The init_script_folder exists
    # cp "${SCRIPT_DIR}/susanoo_WeatherStation_startWebServer.sh /usr/local/etc/rc.d/weatherStationWeb.sh
    # FIXME For some systems (like Synology NAS) scripts launched at startup are in folder /usr/local/etc/rc.d/
    sudo cp "${SCRIPT_DIR}/bin/susanoo_WeatherStation_startWebServer.sh" "/etc/init.d/weatherStationWeb.sh"
    sudo chmod +x "/etc/init.d/weatherStationWeb.sh"
    sudo ln -s "/etc/init.d/weatherStationWeb.sh" "/etc/rc3.d/weatherStationWeb.sh"
    printf -- "Web server will be launched at restart.\n"
    read -r -p "Press Enter to continue..."
  fi
fi

cat << EOF


****************************************************************
*** INSTRUCTIONS TO MANUALLY FINISH THE INSTALLATION PROCESS ***
***  (all steps not yet automated but it should be easy...)  ***
****************************************************************

-
Add below line to crontab of user '\''${INSTALL_USER}'\'' by executing '\''crontab -e'\'':
* * * * *  ${PY_VENV}/bin/python3 ${HOME}/meteo/src/main/py/periodical_sensor_reading.py >> ${HOME}/susanoo-data.log 2>&1
-
If user can be specified in your OS (other than Raspbian):
* * * * *  ${INSTALL_USER}    ${PY_VENV}/bin/python3 "${HOME}/meteo/src/main/py/periodical_sensor_reading.py" >> "${HOME}/susanoo-data.log" 2>&1


As admin, add below lines at the end of /etc/rc.local, before last '\''exit 0'\'':
$ sudo vi /etc/rc.local
[...]
# Watchdog (only used for optional visible LED and possibility of shutting down the Raspberry Pi with button):
nohup -- ${PY_VENV}/bin/python3 -u ${HOME}/meteo/src/main/py/watchdog_gpio.py >> /var/log/watchdog_gpio.log 2>&1 &

# Camera trap:
sudo su - ${INSTALL_USER} --command \"nohup -- ${PY_VENV}/bin/python3 ${HOME}/meteo/src/main/py/video_capture_on_motion.py >> ${HOME}/meteo/video.log 2>&1\" &

# Webserver: (on a Synology NAS, it should be in /usr/local/etc/rc.d/weatherStationWeb.sh)
sudo su - ${WEB_USER} --command \"nohup -- ${PY_VENV}/bin/python3 ${HOME}/meteo/src/main/py/server3.py >> ${HOME}/../${WEB_USER}/server3.log\" &


# FIXME:
sudo -u ${WEB_USER} --login sh -c "cd /path/to/working_directory && python3 your_script.py"
sudo --user=${WEB_USER} --login sh -c "cd ${WEB_USER_HOME}/public_html/ && ${PY_VENV}/bin/python3 your_script.py"


# Required to keep WiFi always on:
sleep 30 && sudo iw dev wlan0 set power_save off &

exit 0
-

Also, if willing to start without graphical GUI, this can be configured with 'sudo raspi-config'.
EOF

cd "${START_DIR}"
printf -- "\n\n\n%s script terminated successfully.\n" "${BASH_SOURCE[0]}"
exit 0
