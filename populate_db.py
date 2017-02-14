from datetime import datetime
from random import gauss
import requests
import time

# for _ in range(users):
# 	record 				= WashingRecord()
# 	record.city 		= city
# 	record.state 		= state
# 	record.time_stamp 	= datetime(2017,2,14, gauss(mu,sigma)%24, gauss(mu,sigma)%60, gauss(mu,sigma)%60)
# 	print(record.time_stamp)


if __name__ == "__main__":
	country 	= 'japan'
	city 		= 'tokyo'
	time_interval 	= 2		# Seconds
	mu 			= 19
	sigma 		= 5.5
	payload 				= {}
	no_of_data_gen 			= 50
	is_local_host 			= True
	device_updater_url 		= "update"

	if(is_local_host):
		initial_url 		= "http://localhost:8000/"
	else:
		initial_url 		= "<To-be-implemented>"

	device_updater_full_url 	= initial_url + device_updater_url

	for _ in range(no_of_data_gen):
		payload.update({'country': country, 'city': city, 'time_stamp': datetime(2017,2,14, int(gauss(mu,sigma)%24), int(gauss(mu,sigma)%60), int(gauss(mu,sigma)%60))})
		r 	= requests.get(device_updater_full_url, params=payload)
		time.sleep(time_interval)
