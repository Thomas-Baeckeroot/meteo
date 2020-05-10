# meteo
Weather station &amp; + with Raspberry Pi

With a simple Raspberry Pi (eventually a 0) connected to weather sensors, make a weather station that include:
- data history
- consulting data through web interface
- possibly a webcam

The idea is to start with a blank raspian (simple 'Raspbian Buster Lite' ok),
- login,
- (launch command line "sudo apt install git" of course...) 
- clone this repository with "git clone https://github.com/Thomas-Baeckeroot/meteo.git"
- then follow instruction of "sudo meteo/install.sh"...

# GPIO pins

|                     |                         |     |     |                         |                   |
|--------------------:| -----------------------:|:---:|:---:|:----------------------- |:------------------|
|                     |                   3.3V  | ` 1`| ` 2`|  5V                     |                   |
|             Sensors |**SDA < I2C** /~~GPIO 2~~| ` 3`| ` 4`|  5V                     |                   |
|  Temp./humidity/... |**SCL < I2C** /~~GPIO 3~~| ` 5`| ` 6`|  GND                    |                   |
|                     |               **GPIO 4**| ` 7`| ` 8`|**GPIO 14** / UART > TXD |                   |
|                     |                    GND  | ` 9`| `10`|**GPIO 15** / UART > RXD |                   |
|                     |              **GPIO 17**| `11`| `12`|**GPIO 18** / PCM > CLK  | Mvt detector (in) |
|                     |              **GPIO 27**| `13`| `14`|  GND                    |                   |
|(distance sensor-out)|              **GPIO 22**| `15`| `16`|**GPIO 23**              |(distance sensor-in)|
|                     |                   3.3V  | `17`| `18`|**GPIO 24**              |                   |
|                     | MOSI < SPI / **GPIO 10**| `19`| `20`|  GND                    |                   |
|                     | MISO < SPI /  **GPIO 9**| `21`| `22`|**GPIO 25**              | Watchdog LED - green blink (out)   |
|                     | SCLK < SPI / **GPIO 11**| `23`| `24`|**GPIO 7**               |                   |
|                     |                    GND  | `25`| `26`|**GPIO 8**               |                   |
|                     |                   ID SD | `27`| `28`|  ID SC                  |                   |
|                     |               **GPIO 5**| `29`| `30`|  GND                    |                   |
|         relay (out) |               **GPIO 6**| `31`| `32`|**GPIO 12**              | btn (in)          |
|         relay (out) |              **GPIO 13**| `33`| `34`|  GND                    |                   |
| CPU fan relay (out) |   FS < PCM / **GPIO 19**| `35`| `36`|**GPIO 16**              | btn (in)          |
|         relay (out) |              **GPIO 26**| `37`| `38`|**GPIO 20** / PCM > DIN  | btn (in)          |
|                     |                    GND  | `39`| `40`|**GPIO 21** / PCM > DOUT | Shutdown btn (in) |

