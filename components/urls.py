from django.urls import path
from . import views

urlpatterns = [
    path('components/<str:component_type>/', views.ComponentListView.as_view(), name='component-list'),
    path('component-detail/<str:component_type>/<int:component_id>/', views.ComponentDetailView.as_view(), name='component-detail'),
    path('builds/<int:build_id>/', views.PCBuildDetailView.as_view(), name='build-detail'),
    path('compatibility-check/', views.CompatibilityCheckView.as_view(), name='compatibility-check'),
]