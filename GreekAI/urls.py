from django.contrib import admin
from django.urls import path
from start.views import index
from greek_ai.views import greek

urlpatterns = [
    path('', index),
    path('api/greek-ai', greek)
]
