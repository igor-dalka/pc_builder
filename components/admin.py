from django.contrib import admin
from .models import *

admin.site.register(Motherboard)
admin.site.register(Processor)
admin.site.register(GraphicsCard)
admin.site.register(RAM)
admin.site.register(PSU)
admin.site.register(Chassis)
admin.site.register(Fan)
admin.site.register(Disc)
admin.site.register(CPU_cooler)
admin.site.register(Thermal_Paste)