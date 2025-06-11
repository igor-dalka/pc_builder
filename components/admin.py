from django.contrib import admin
from .models import *

admin.site.register(motherboard)
admin.site.register(processor)
admin.site.register(gpu)
admin.site.register(ram)
admin.site.register(psu)
admin.site.register(chassis)
admin.site.register(fan)
admin.site.register(disc)
admin.site.register(cpu_cooler)
admin.site.register(thermal_paste)