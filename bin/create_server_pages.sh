#!/usr/bin/env bash
set -e
# set -x

# FIXME Make sure we have 2 arguments

L_SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
L_HOME="$1"
L_WEB_USER="$2"

source "${L_SCRIPT_DIR}/helper_functions.sh"

# TODO Create a variable that replaces '${L_HOME}/../${L_WEB_USER}' by direct '${HOME_WEB_USER}' (without '..')
sudo mkdir -p "${L_HOME}/../${L_WEB_USER}/public_html"
sudo chmod 755 "${L_HOME}/../${L_WEB_USER}/public_html"
printf -- "Folder 'public_html' created in home of user '%s'\n" "${L_WEB_USER}"
create_link "${L_HOME}/meteo/src/main/py/public_html/index.html.py" "${L_HOME}/../${L_WEB_USER}/public_html/index.html"
create_link "${L_HOME}/meteo/src/main/py/public_html/graph.svg.py" "${L_HOME}/../${L_WEB_USER}/public_html/graph.svg"
create_link "${L_HOME}/meteo/src/main/py/public_html/capture.html.py" "${L_HOME}/../${L_WEB_USER}/public_html/capture.html"
sudo mkdir -p "${L_HOME}/../${L_WEB_USER}/public_html/html"
sudo chmod 755 "${L_HOME}/../${L_WEB_USER}/public_html/html"
create_link "${L_HOME}/meteo/src/main/py/public_html/html/favicon.svg" "${L_HOME}/../${L_WEB_USER}/public_html/html/favicon.svg"
create_link "${L_HOME}/meteo/captures" "${L_HOME}/../${L_WEB_USER}/public_html/captures"
printf -- "Links created in 'public_html' pointing to adequate folder '%s'\n" "${L_HOME}/meteo/...\n"
