from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('map/', views.map_view, name='map'),
    path('get-traffic-data/', views.get_traffic_data, name='get_traffic_data'),
]