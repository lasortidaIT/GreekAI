import base64
import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .apps import *


class UploadView(APIView):
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    @staticmethod
    def post(request):
        if request.method == "POST":
            try:
                name = str(request.FILES['image'])
            except Exception as e:
                name = 'f'
            if 'f' == name:
                canvas_data = request.POST.get('image')
                header, pixels = canvas_data.split(',')

                with open('storage/cash/imageToSave.png', 'wb') as fh:
                    fh.write(base64.decodebytes(bytes(pixels, "utf-8")))

                filename = 'storage/cash/imageToSave.png'
            else:
                file = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save('storage/cash/' + file.name, file)

            image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, (64, 64)) / 255.0

            os.remove(filename)

            greek_ai = GreekAIModelConfig.model

            image = np.expand_dims(image, axis=0)
            image = torch.from_numpy(image)
            image = image.type('torch.FloatTensor')

            prediction = greek_ai(image)
            prediction = prediction.detach().cpu().numpy()[0]
            ind = np.argmax(prediction)
            rate = round(prediction[ind] * 100)

            codes = ['Lalpha', 'Lbeta', 'Lgamma', 'Ldelta', 'Lepsilon', 'Lzeta', 'Leta', 'Ltheta', 'Liota', 'Lkappa',
                     'Llambda', 'Lmu', 'Lnu', 'Lxi', 'Lomicron', 'Lpi', 'Lrho', 'Lsigma', 'Ltau', 'Lupsilon', 'Lphi',
                     'Lchi', 'Lpsi', 'Lomega',
                     'Ualpha', 'Ubeta', 'Ugamma', 'Udelta', 'Uepsilon', 'Uzeta', 'Ueta', 'Utheta', 'Uiota', 'Ukappa',
                     'Ulambda', 'Umu', 'Unu', 'Uxi', 'Uomicron', 'Upi', 'Urho', 'Usigma', 'Utau', 'Uupsilon', 'Uphi',
                     'Uchi', 'Upsi', 'Uomega']
            alphabet = 'αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
            code = codes[ind]
            symbol = alphabet[ind]

            return Response({
                'code': code,
                'probability': rate,
                'symbol': symbol,
            })
        else:
            return
