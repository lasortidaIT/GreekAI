from django.urls import path
from recognizer import views
from api.views import *


urlpatterns = [
    path('', views.index),
    path('api/greek-ai', UploadView.as_view(), name = 'prediction')
]
