
from django.urls import path
from .views import home
app_name = "student"
urlpatterns = [
    path('', home, name='home'),
]
