import numpy as np
import time
import datetime
from django.shortcuts import render
from django.views.generic import TemplateView, View
from website.countries import *
from website.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponse

class WashingTimeAzureQueryMixin(object):
	def __init__(self, *args, **kwargs):
		self.record_limit 				= 50
		super(WashingTimeAzureQueryMixin, self).__init__(*args, **kwargs)

	def __to_seconds(self, datetime_time_obj):
		return datetime_time_obj.hour *3600 + datetime_time_obj.minute *60 + datetime_time_obj.second

	def __seconds_to_display(self, sec): 
		return time.strftime('%H:%M', time.gmtime(sec))

	def __init_time_stamp_dict(self, start_time, end_time, interval_time):
		assert end_time > start_time
		start_time_seconds 				= self.__to_seconds(start_time)
		end_time_seconds 				= self.__to_seconds(end_time)
		interval_seconds 				= self.__to_seconds(interval_time)
		time_stamps 					= list(range(start_time_seconds, end_time_seconds, interval_seconds))
		return time_stamps

	def __get_aggregated_dict(self, time_stamp_rec_filtered, start_time, end_time, interval_time, **kwargs):
		time_stamps 				= self.__init_time_stamp_dict(start_time, end_time, interval_time)
		vector 						= [0] *(len(time_stamps) -1)
		count_i = 0; count_j = 1;

		for each_time_stamp in time_stamp_rec_filtered:
			time_obj  		= each_time_stamp.time_stamp.time()
			time_to_sec 	= self.__to_seconds(time_obj)
			if(time_to_sec < time_stamps[count_j]):
				pass
			else:
				while(time_to_sec >= time_stamps[count_j]):
					if(count_j >= len(time_stamps) -1):
						break
					else:
						count_j += 1
						count_i += 1			
			vector[count_i] 	+= 1
		return {'data':vector, 'time_stamps': list(map(self.__seconds_to_display, time_stamps))}

	def get_aggregated_timestamp_dict(self, selected_country, selected_city, **kwargs):
		time_stamp_rec_raw 			= WashingRecord.objects.filter(country=selected_country, city=selected_city).order_by('time_stamp')
		time_stamp_rec_filtered 	= time_stamp_rec_raw[:self.record_limit]
		return self.__get_aggregated_dict(time_stamp_rec_filtered=time_stamp_rec_filtered, **kwargs)

class MainPage(WashingTimeAzureQueryMixin, TemplateView):
	template_name 		= "index.html"

	def __init__(self, *args, **kwargs):
		super(MainPage, self).__init__(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context 				= super(MainPage, self).get_context_data(**kwargs)
		request_obj 			= self.request
		context['no_of_users'] 	= 0
		
		if(request_obj.GET.get('city') or request_obj.GET.get('country')):
			if(request_obj.GET.get('city')):
				selected_country, selected_city = request_obj.GET.get('city').split('-')

				start_time 						= datetime.time(7,0,0) 		# 7 am
				end_time 						= datetime.time(20,0,0) 	# 8 pm
				interval_time 					= datetime.time(2,0,0) 		# 2 hours
				aggregated_dict					= self.get_aggregated_timestamp_dict(selected_country=selected_country, selected_city=selected_city,
													start_time=start_time, end_time=end_time, interval_time=interval_time)
				context['no_of_users'] 			= aggregated_dict['data']
				context['time_stamps'] 			= aggregated_dict['time_stamps']
				context['selected_city'] 		= selected_city
			else:
				selected_country				= request_obj.GET.get('country')

			context['selected_country'] 	= selected_country
			context['all_city'] 			= country[selected_country]['city']
		context['all_country'] 				= country
		context['total_users'] 				= 200
		return context

class PopulateDBHandler(View):
	def get(self, request_obj):
		new_rec 			= WashingRecord()
		new_rec.country 	= request_obj.GET.get('country')
		new_rec.city 		= request_obj.GET.get('city')
		new_rec.time_stamp 	= request_obj.GET.get('time_stamp')
		new_rec.save()
		HttpResponse('Success')