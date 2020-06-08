#!/bin/bash
#Purpose = Backup of meteo DB and scripts
DATE=$(date +"%Y-%m-%d")
# TODO Backup of PostgreSQL DB to dump file
tar -zcvf "$HOME/meteo_$DATE.tgz" "$HOME/meteo"
