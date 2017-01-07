from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime

temperature_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 34)
text_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 20)

def drawImage_forecast(forecast, show_datetime):

	current_forecast = forecast.currently()
	summary = current_forecast.d['summary']
	icon = current_forecast.d['icon']
	temperature = current_forecast.d['temperature']
	now = datetime.today()

	image = Image.new('1', (200, 96), 1)
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

	return image

def drawImage_sunInfo(forecast):

	today = forecast.daily().data[0]
	sunrise = today.sunriseTime
	sunset = today.sunsetTime

	image = Image.new('1', (200, 96), 1)
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, image.width, image.height), fill=1, outline=1)

	sunrise_icon = Image.open('./icons/sunrise.bmp')
	sunset_icon = Image.open('./icons/sunset.bmp')
	draw.bitmap((0,2), sunrise_icon, fill=0)
	draw.bitmap((0,51), sunset_icon, fill=0)

	draw.text( (60, 10), "{h:02d}:{m:02d}".format(h=sunrise.hour, m=sunrise.minute), font=text_font)
	draw.text( (60, 58), "{h:02d}:{m:02d}".format(h=sunset.hour, m=sunset.minute), font=text_font)

	return image