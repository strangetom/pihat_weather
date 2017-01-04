from papirus import Papirus
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime
import time 

import forecastio as f
from apikey import api_key

# Function to draw image
def draw_image(current_forecast, show_datetime):

	summary = current_forecast.d['summary']
	icon = current_forecast.d['icon']
	temperature = current_forecast.d['temperature']
	now = datetime.today()

	# Draw image
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, image.width, image.height), fill=1, outline=1)
	# Draw temperature
	draw.text( (16, 20), "{temp}'C".format(temp=round(temperature, 1)), font=temperature_font)
	# Draw icon
	icon = Image.open('./icons/{}.bmp'.format(icon))
	draw.bitmap((image.width - icon.width, 4), icon, fill=0)

	# Draw either summary or date and time
	if show_datetime:
		time_date = '{h:02d}:{m:02d} {date}'.format(h=now.hour, m=now.minute, date=now.strftime('%d %b'))
		x_pix = (200 - draw.textsize(time_date, font=text_font)[0])/2
		draw.text((x_pix, 72), time_date, fill=0, font=text_font)
	else:
		x_pix = (200 - draw.textsize(summary, font=text_font)[0])/2
		draw.text((x_pix, 72), summary, fill=0, font=text_font)


# Set up image to display
image = Image.new('1', (200, 96), 1)
temperature_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 34)
text_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 20)

# Set up display
papirus = Papirus()
papirus.clear()

# Set up weather forecast
lat = 53.768983
lng = -2.764714
forecast = f.load_forecast(api_key, lat, lng, units='si')
current_forecast = forecast.currently()
show_datetime = True

draw_image(current_forecast, show_datetime)
papirus.display(image)
papirus.update()


weather_update = time.time()
display_update = time.time()
update_display = ''


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
			current_forecast = forecast.currently()

			update_display = 'full'
			weather_update = time.time()

		# Draw image
		draw_image(current_forecast, show_datetime)
		papirus.display(image)

		# Update display
		if update_display == True:
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
