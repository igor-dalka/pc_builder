from django.urls import path
from .views import CpuMoboCompatibilityView

urlpatterns = [
    path('check-cpu-mobo/', CpuMoboCompatibilityView.as_view(), name='check_cpu_mobo'),
]