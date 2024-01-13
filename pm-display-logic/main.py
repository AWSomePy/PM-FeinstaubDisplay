import time
import requests
import datetime 
from requests.exceptions import HTTPError
from PIL import Image, ImageDraw, ImageFont, ImageColor
import math
import uuid
import os

print('timestamp: ', datetime.datetime.now())


sensor_station = '13463'
rest_host = 'http://192.168.2.100:5001'
path_to_font_file = '/home/pi/scripts/pm-display/PICO-8_mod.ttf' 

def query_data_from_sensorcom():
	try:
		response = requests.get('https://data.sensor.community/airrohr/v1/sensor/'+sensor_station+'/')
		response.raise_for_status()
		# access JSOn content
		jsonResponse = response.json()
		print("Entire JSON response")
		print(jsonResponse)

		return jsonResponse

	except HTTPError as http_err:
		print(f'HTTP error occurred: {http_err}')
	except Exception as err:
		print(f'Other error occurred: {err}')



def extract_data(jsonresponse):
	try:
		pm25 = jsonresponse[0]["sensordatavalues"][1]["value"] ### hardcoded 2 Datenpaket. immer PM2.5? to do: suche erste index containing P2, dann erneute nach KEY-Name
		print(pm25)
		return (pm25.split('.'))[0]
	except Exception as e:
		print("extract_data exception", e)

def post_clear_bkg():
	try:
		headers = {
	    'accept': 'application/json',
	    'Content-Type': 'application/x-www-form-urlencoded',
		}

		data = {
		    'r': '0',
		    'g': '0',
		    'b': '0',
		    'push_immediately': 'true',
		}

		response = requests.post(rest_host+'/fill', headers=headers, data=data)	
	except Exception as e:
		print("extract_data exception", e)

def post_scrolltext(msg, fontsize,posx, posy, id,c_r=255, c_g=255, c_b=255):
	try:
		headers = {
		    'accept': 'application/json',
		    'Content-Type': 'application/x-www-form-urlencoded',
		}

		data = {
		    'text': msg,
		    'x': posx,
		    'y': posy,
		    'r': c_r,
		    'g': c_g,
		    'b': c_b,
		    'identifier': id,
		    'font': fontsize,
		    'width': '64',
		    'movement_speed': '0',
		    'direction': '0',
		}

		response = requests.post(rest_host+'/sendText', headers=headers, data=data)
	except Exception as e:
		print("extract_data exception", e)

def post_pixoo(msg_text, posy):
	try:
		

		headers = {
		'accept': 'application/json',
		'Content-Type': 'application/x-www-form-urlencoded',
		}

		data = {
		    'text': msg_text,
		    'x': '1',
		    'y': posy,
		    'r': '0',
		    'g': '0',
		    'b': '255',
		    'push_immediately': 'true',
		}

		response = requests.post(rest_host+'/text', headers=headers, data=data)
		print(response)
	except Exception as e:
		print("extract_data exception", e)

def post_draw_line(ypos):
	try:

		headers = {
	    'accept': 'application/json',
	    'Content-Type': 'application/x-www-form-urlencoded',
		}

		data = {
		    'start_x': '0',
		    'start_y': ypos,
		    'stop_x': '64',
		    'stop_y': ypos,
		    'r': '255',
		    'g': '255',
		    'b': '255',
		    'push_immediately': 'true',
		}

		response = requests.post(rest_host+'/line', headers=headers, data=data)
	except Exception as e:
		print("extract_data exception", e)

def post_draw_rectangle(x1, y1, x2, y2,r,g,b):
	try:
		headers = {
		    'accept': 'application/json',
		    'Content-Type': 'application/x-www-form-urlencoded',
		}

		data = {
		    'top_left_x': x1,
		    'top_left_y': y1,
		    'bottom_right_x': x2,
		    'bottom_right_y': y2,
		    'r': r,
		    'g': g,
		    'b': b,
		    'push_immediately': 'true',
		}

		response = requests.post(rest_host+'/rectangle', headers=headers, data=data)
	except Exception as e:
		print("extract_data exception", e)

def check_ok_nok(pm_value,limit):
	try:
		if 	int(feinstaubdatapunkt) < limit:
			return "OK", 0,255,0
		else:
			return "nicht OK", 255,0,0
	except Exception as e:
		print("extract_data exception", e)


def post_gif(filename):
	try:

		headers = {
		    'accept': 'application/json',
		    # requests won't add a boundary if this header is set when you pass files=
		    # 'Content-Type': 'multipart/form-data',
		}

		files = {
		    'gif': (filename, open(filename, 'rb'), 'image/png'),
		    'speed': (None, '100'),
		    'skip_first_frame': (None, 'false'),
		}

		response = requests.post(rest_host+'/sendGif', headers=headers, files=files)
	except Exception as e:
		print("extract_data exception", e)

data = query_data_from_sensorcom()

feinstaubdatapunkt = extract_data(data)
print(feinstaubdatapunkt)

if feinstaubdatapunkt:
	img1 = Image.new(mode="RGBA", size=(64,64), color='black')
	draw = ImageDraw.Draw(img1)


	###############LIN scale
	x1=6
	y1=10
	x2=x1+4
	y2=y1+4
	rec = 0
	col1 = "lime"
	draw.rectangle([x1+rec,y1,x2+rec,y2], fill =col1)
	rec = rec+6
	col1 = "orange"
	draw.rectangle([x1+rec,y1,x2+rec,y2], fill =col1) 
	rec = rec+6
	draw.rectangle([x1+rec,y1,x2+rec,y2], fill =col1)
	rec = rec+6
	draw.rectangle([x1+rec,y1,x2+rec,y2], fill =col1) 
	rec = rec+6

	draw.rectangle([x1+rec,y1,x2+rec,y2], fill =col1)
	rec = rec+6
	col1 = "red"
	draw.rectangle([x1+rec,y1,x2+rec,y2], fill =col1) 
	rec = rec+6
	draw.rectangle([x1+rec,y1,x2+rec,y2], fill =col1)
	rec = rec+6
	draw.rectangle([x1+rec,y1,x2+rec,y2], fill =col1) 


	max_scale_lin = 40 #yg/m3
	# scale_ratio_arrow = (57-x1)/max_scale_lin  ##all x pixels from scale, per 50 ygm3
	# value_datapoint_arrow = int(x1 + int(feinstaubdatapunkt)*scale_ratio_arrow)
	if int(feinstaubdatapunkt)<=5:
		value_datapoint_arrow=8
	if int(feinstaubdatapunkt)>5:
		value_datapoint_arrow=8+6
	if int(feinstaubdatapunkt)>10:
		value_datapoint_arrow=8+6+6
	if int(feinstaubdatapunkt)>15:
		value_datapoint_arrow=8+6+6+6
	if int(feinstaubdatapunkt)>20:
		value_datapoint_arrow=8+6+6+6+6
	if int(feinstaubdatapunkt)>25:
		value_datapoint_arrow=8+6+6+6+6+6
	if int(feinstaubdatapunkt)>30:
		value_datapoint_arrow=8+6+6+6+6+6+6
	if int(feinstaubdatapunkt)>35:
		value_datapoint_arrow=8+6+6+6+6+6+6+6
	if int(feinstaubdatapunkt)>40:
		value_datapoint_arrow = 62
	draw.polygon([(value_datapoint_arrow,y2+2), (value_datapoint_arrow-2, y2+4), (value_datapoint_arrow+2,y2+4)], fill = (255,255,255))

	unicode_text = u"feinstauB pM2.5"
	font = ImageFont.truetype(path_to_font_file, 5, encoding="unic")
	draw.text((2, 2), unicode_text, fill='white', font=font)

	font = ImageFont.truetype(path_to_font_file, 5, encoding="unic")
	text2 = u"µg/m"
	draw.text((25, 57), text2, fill='white', font=font)

	font = ImageFont.truetype(path_to_font_file, 5, encoding="unic")
	text25 = u"3" #hoch 3
	draw.text((42, 55), text25, fill='white', font=font)

	col_data = "white"
	thres1 = 5 #WHO
	thres2 = 25 # EU Grenzwert
	thres3 = 40

	if int(feinstaubdatapunkt)<=thres1:
		col_data = "lime"
	if int(feinstaubdatapunkt)>thres1:
		col_data = "orange"
	if int(feinstaubdatapunkt)>thres2:
		col_data = "red"
	if int(feinstaubdatapunkt)>thres3:
		col_data = "magenta"


	if len((str(int(feinstaubdatapunkt)))) == 1:
		x_datapoint = 26
	if len((str(int(feinstaubdatapunkt)))) == 2:
		x_datapoint = 11
	if len((str(int(feinstaubdatapunkt)))) == 3:
		x_datapoint = 0
	font = ImageFont.truetype(path_to_font_file, 30, encoding="unic")
	text3 = (str(int(feinstaubdatapunkt)))
	draw.text((x_datapoint, 23), text3, fill=col_data, font=font)

	font = ImageFont.truetype(path_to_font_file, 5, encoding="unic")
	text4 = u"0"
	draw.text((1, 10), text4, fill='gray', font=font)

	font = ImageFont.truetype(path_to_font_file, 5, encoding="unic")
	text4 = u"40"
	draw.text((55, 10), text4, fill='gray', font=font)

	filename_unique = str(uuid.uuid1())+"lin1.png"
	img1.save(filename_unique)
	# img1.show()
	post_gif(filename_unique)

	time.sleep(10)

	os.remove(filename_unique)



	# gif = []
	# images = [img1, img2, img3] #images, just convert it into PIL.Image obj
	# for image in images:
	#     gif.append(image)
	# gif[0].save(filename_unique+'lin_temp_result.gif', save_all=True,optimize=False, append_images=gif[1:], loop=0)




