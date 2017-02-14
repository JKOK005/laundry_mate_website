from django.contrib import admin
from website.models import *

# Register your models here.
@admin.register(WashingRecord)
class WashingRecordAdmin(admin.ModelAdmin):
    pass