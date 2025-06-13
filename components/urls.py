from django.urls import path
from . import views

urlpatterns = [
    path('components/<str:component_type>/', views.ComponentListView.as_view(), name='component-list'),
]