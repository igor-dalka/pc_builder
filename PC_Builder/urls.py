from django.contrib import admin
from django.urls import path, include
from components import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('components.urls')),
    path('build-ui/', views.PCBuildUIView.as_view(), name='build-ui')
]