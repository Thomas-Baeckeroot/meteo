# Release notes

---

### Version 0.0.9 (2023-11-18)

###### Features

- First version to be tagged
- camera parameters in config file

###### Bug Fixes

- Minor changes in installation script

###### Breaking Changes

- Server pages should be in folder `~/public_html/` now
  (Use `./bin/create_server_pages.sh "${HOME}" "${WEB_USER}"` to create required links, Eg. for Raspberry Pi install: `./bin/create_server_pages /home/pi web`)
- Config file name changed to susanoo_WeatherStation.conf . Use the below to rename it:

      mv ${HOME}/.config/meteo.conf ${HOME}/.config/susanoo_WeatherStation.conf
      WEB_USER=web
      sudo mv "${HOME}/../${WEB_USER}/.config/meteo.conf" "${HOME}/../${WEB_USER}/.config/susanoo_WeatherStation.conf"
