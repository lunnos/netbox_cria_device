from django.urls import path
from . import views

app_name = 'netbox_cria_device'

urlpatterns = [
    path('devices/add/', views.CustomDeviceAddView.as_view(), name='device_add_custom'),
    path('sites/add/modal/', views.SiteCreateModalView.as_view(), name='site_add_modal'),
]