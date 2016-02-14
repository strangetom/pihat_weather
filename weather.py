import forecastio as f
import scrollphat as s
import time as t
from apikey import api_key

lat = 50.696734
lng = -1.295813

s.set_brightness(2)
forecast = f.load_forecast(api_key, lat, lng, units='si')
current_forecast = forecast.currently()
start_time = t.time()

while True:
	try:
		temp =  str(int(round(current_forecast.d['apparentTemperature'])))
		temp_str = temp + '\'C '
		summary = current_forecast.d['summary'].upper()
		display_str = temp_str + summary

		# 'M' and 'W' take 6 spaces, rather than 4
		num_m = display_str.count('M')
		num_w = display_str.count('W')
                # Each letter takes 4 LEDs to display (including trailing space)
                # -2 because the degree symbol only takes 2 LEDs
                # -11 because they are shown before we need to scroll
                # -1 because there's no trailing space after last letter
		scroll_len = len(display_str)*4 - 2 - 11 - 1 + 2*(num_m+num_w)

		s.clear()
		s.write_string(display_str)
		t.sleep(1)
		for i in range(scroll_len):
			t.sleep(0.08)
			s.scroll()
		t.sleep(0.5)

                # Update the weather forecast every 5 minutes
		if ((t.time() - start_time) > 5*60):
			try:
				forecast = f.load_forecast(api_key, lat, lng, units='si')
				current_forecast = forecast.currently()
			except:
				pass
			start_time = t.time()
			print(t.asctime()[11:-5], '\r')

	except KeyboardInterrupt:
		s.clear()
		break
