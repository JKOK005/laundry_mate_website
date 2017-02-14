from django.conf.urls import url, include
from django.contrib import admin
from website.views import *

urlpatterns = [
	url(r'^$', MainPage.as_view(), name="main-page"),
	url(r'^update$', PopulateDBHandler.as_view(), name="update-db")
]