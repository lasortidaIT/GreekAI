from django.shortcuts import render
import cv2
from PIL import Image
import numpy as np
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import requests


def index(request):
    return render(request, "index.html")
