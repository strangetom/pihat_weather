from __future__ import print_function
import time
from papirus import Papirus
import RPi.GPIO as GPIO
from eink_images import drawImage_forecast, drawImage_sunInfo, drawImage_next2Days

import forecastio as f
from apikey import api_key

# Set up display
papirus = Papirus()
papirus.clear()

# Get initial weather forecast
lat = 53.768983
lng = -2.764714
forecast = f.load_forecast(api_key, lat, lng, units='si')
print("Weather update: {h:02d}:{m:02d}:{s:02d}".format(h=time.localtime().tm_hour, m=time.localtime().tm_min, s=time.localtime().tm_sec))
show_datetime = True

# Initial image
img = drawImage_forecast(forecast, show_datetime)
papirus.display(img)
papirus.update()

weather_update = time.time()
display_update = time.time()
secondary_display = 0
update_display = ''

# Set up buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)
GPIO.setup(19, GPIO.IN)
# GPIO 26 is first from left
# GPIO 19 is second from left
# GPIO 20 is third from left
# GPIO 16 is fourth from left
# GPIO 21 is fifth from left

while True:
	try:

		# Update display every 10 seconds
		if (time.time() - display_update) > 10:
			update_display = 'partial'
			show_datetime = not show_datetime
			display_update = time.time()

		# Update weather forecast every 5 minutes
		if (time.time() - weather_update) > 5*60:
			forecast = f.load_forecast(api_key, lat, lng, units='si')

			print("Weather update: {h:02d}:{m:02d}:{s:02d}".format(h=time.localtime().tm_hour, m=time.localtime().tm_min, s=time.localtime().tm_sec))
			update_display = 'full'
			weather_update = time.time()

		# Draw image
		img = drawImage_forecast(forecast, show_datetime)
		papirus.display(img)

		if GPIO.input(26) == False:
			img = drawImage_sunInfo(forecast)
			papirus.display(img)
			papirus.update()

			update_display = 'full'
			secondary_display = time.time()

		if GPIO.input(19) == False:
			img = drawImage_next2Days(forecast)
			papirus.display(img)
			papirus.update()

			update_display = 'full'
			secondary_display = time.time()

		# Update display
		if time.time() - secondary_display > 5:
			if update_display == 'full':
				papirus.update()
				update_display = ''
			elif update_display == 'partial':
				papirus.partial_update()
				update_display = ''
			else:
				pass


	except KeyboardInterrupt:
		papirus.clear()
		break
