from django.urls import path
from backend_diploma.views import create_map, get_clusters


urlpatterns = [
    path('set_map/', create_map),
    path('get_map/', get_clusters),
]