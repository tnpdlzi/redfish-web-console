from django.urls import path

from restApi import views

urlpatterns = [
    path('api/server', views.server_list),
    path('api/check', views.server_check),
    path('api/deleteServer', views.delete_server),
    path('api/dashboard', views.dashboard_list),
    path('api/instances', views.instance_list),
    path('api/messages', views.message_list),
    path('api/details', views.details),
    path('api/processors', views.processor_list),
    path('api/bios', views.bios_list),
    path('api/memory', views.memory_list),
    path('api/ethernet', views.ethernet_list),
    path('api/storages', views.storage_list),
    path('api/logs', views.log_list),
    path('api/chassis', views.chassis_list),
    path('api/ThermalSubsystem', views.ThermalSubsystem_list),
    path('api/PowerSubsystem', views.PowerSubsystem_list),
    path('api/EnvironmentMetrics', views.EnvironmentMetrics_list),
    path('api/Sensors', views.Sensors_list),
    path('api/Thermal', views.Thermal_list),
    path('api/Power', views.Power_list),
    path('api/telegraf', views.telegraf),
    path('api/Charts', views.ChartUid_list),
    path('api/EditDashboard', views.edit_Dashboard),
    path('api/CardList', views.getCardData),
    # path('api/getThreshold', views.getThreshold),
    # path('api/sensorTemperatures', views.sensor_temps),
]