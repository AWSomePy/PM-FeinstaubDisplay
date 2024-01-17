# PM-FeinstaubDisplay

Script und Workflow für ein Feinstaub-Display basierend auf dem Divoom Pixoo 64. [https://divoom.com/products/pixoo-64](https://divoom.com/products/pixoo-64)

Messdatenanzeige von [https://sensor.community/](https://maps.sensor.community/#9/48.8676/9.4095) Station.

![feinstaub display](https://github.com/AWSomePy/PM-FeinstaubDisplay/blob/main/pm-display-logic/images/feinstaub_display.JPG)

## REST API - communication with Pixo64
setup the great project [https://github.com/4ch1m/pixoo-rest](https://maps.sensor.community/#9/48.8676/9.4095) to interact via REST API with Pixoo64

-modify `.env` setup the IP to pixoo (according the introduction) and setup port for REST

-recommended to create launcher.sh to start REST API on reboot
`cd /home/pi/scripts/pixoo-rest/pixoo-rest/`

`nano launcher.sh`

```
#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python scrip$

cd /
cd home/pi/scripts/pixoo-rest/pixoo-rest
/usr/local/bin/python3 app.py
cd /
```
run launcher.sh to start REST API. By opening the brwoser with respective IP and Port, the swager UI should be available
`sh launcher.sh`

## Setup and configure Pull logic to send PM/Feinstaub Data to Pixoo64 display
- copy folder `pm-display-logic` including python file and TTF (font for pixoo) to your linux env.
- install all python dependencies. Tested with python 3.7, but should work also with newer versions.
- customize the configuration directly in python file:

`sensor_station = '13463'` choose you sensor station ID on [https://maps.sensor.community/#9/48.8676/9.4095](https://maps.sensor.community/#9/48.8676/9.4095)

`rest_host = 'http://192.168.2.100:5001'` select the IP and PORT where your REST API runs. 

`path_to_font_file = '/home/pi/scripts/pm-display/PICO-8_mod.ttf' ` pixoo64 has limited pixel density, therefore a special font is used. make sure you insert absolut path to the *.ttf file

run the pyton script to test and verify if everthing is setup properly

`cd /home/pi/scripts/pm-display/` (location of python file)

`python main.py` or `python3 main.py`

## Run Python file periodically
trigger the main.py periodically. Default is 1 minute, setup via crontab.

`crontab -e`

optional: if REST API runs on same machine, with a restart the REST starts:

`@reboot sh /home/pi/scripts/pixoo-rest/pixoo-rest/launcher.sh >/home/pi/scripts/pixoo-rest/pixoo-rest/logslauncher/cronlog 2>&1`

add this to the end of crontab file:

`* * * * * sleep 0; /usr/local/bin/python3 /home/pi/scripts/pm-display/main.py >> /home/pi/scripts/pm-display/logmain.log 2>&1`



