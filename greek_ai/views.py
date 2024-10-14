from django.shortcuts import render
from django.shortcuts import render
import cv2
import numpy as np
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import keras
from django.core.files.storage import FileSystemStorage


model = keras.models.load_model("ml/model.keras")
letters = ['Lalpha', 'Lbeta', 'Lgamma', 'Ldelta', 'Lepsilon', 'Lzeta', 'Leta', 'Ltheta', 'Liota', 'Lkappa',
                   'Llambda', 'Lmu', 'Lnu', 'Lxi', 'Lomicron', 'Lpi', 'Lrho', 'Lsigma', 'Ltau', 'Lupsilon', 'Lphi',
                   'Lchi', 'Lpsi', 'Lomega',
                   'Ualpha', 'Ubeta', 'Ugamma', 'Udelta', 'Uepsilon', 'Uzeta', 'Ueta', 'Utheta', 'Uiota', 'Ukappa',
                   'Ulambda', 'Umu', 'Unu', 'Uxi', 'Uomicron', 'Upi', 'Urho', 'Usigma', 'Utau', 'Uupsilon', 'Uphi',
                   'Uchi', 'Upsi', 'Uomega']


@csrf_exempt
def greek(request):
    if request.method == 'POST':
        try:
            name = str(request.FILES['image'])
        except:
            name = 'f'
        if 'letter.png' == name:
            file = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
        else:
            canvas_data = request.POST.get('image')
            header, pixels = canvas_data.split(',')

            with open("imageToSave.png", "wb") as fh:
                fh.write(base64.decodebytes(bytes(pixels, "utf-8")))

            filename = "imageToSave.png"

        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (64, 64)) / 255.0

        letter, value = make_prediction(image)

        return JsonResponse({'letter_code': letter})
    else:
        return None


def make_prediction(image):
    arr = np.array([image])
    predictions = model.predict(arr)
    likely = np.argmax(predictions[0])
    value = round(predictions[0][likely])
    return letters[likely], value
