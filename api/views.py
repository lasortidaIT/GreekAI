import base64
import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .apps import *


def define_index():
    max_index = -1
    for root, dirs, files in os.walk('storage/data'):
        for file in files:
            ind = int(file.split('_')[1].split('.')[0])
            if ind > max_index:
                max_index = ind
    return max_index + 1

data = {'index': define_index()}

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

                site = True
                api = False

                with open('storage/cash/imageToSave.png', 'wb') as fh:
                    fh.write(base64.decodebytes(bytes(pixels, "utf-8")))

                filename = 'storage/cash/imageToSave.png'
            else:
                file = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save('storage/cash/' + file.name, file)

                site = False
                api = True

            image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            image = cv2.resize(image, (64, 64)) / 255.0

            os.remove(filename)

            greek_ai = GreekAIModelConfig.model

            t = np.expand_dims(image, axis=0)
            t = torch.from_numpy(t)
            t = t.type('torch.FloatTensor')

            prediction = greek_ai(t)
            prediction = prediction.detach().cpu().numpy()[0]
            ind = np.argmax(prediction)
            rate = prediction[ind]

            codes = ['Lalpha', 'Lbeta', 'Lgamma', 'Ldelta', 'Lepsilon', 'Lzeta', 'Leta', 'Ltheta', 'Liota', 'Lkappa',
                     'Llambda', 'Lmu', 'Lnu', 'Lxi', 'Lomicron', 'Lpi', 'Lrho', 'Lsigma', 'Ltau', 'Lupsilon', 'Lphi',
                     'Lchi', 'Lpsi', 'Lomega',
                     'Ualpha', 'Ubeta', 'Ugamma', 'Udelta', 'Uepsilon', 'Uzeta', 'Ueta', 'Utheta', 'Uiota', 'Ukappa',
                     'Ulambda', 'Umu', 'Unu', 'Uxi', 'Uomicron', 'Upi', 'Urho', 'Usigma', 'Utau', 'Uupsilon', 'Uphi',
                     'Uchi', 'Upsi', 'Uomega']
            alphabet = 'αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
            code = codes[ind]
            symbol = alphabet[ind]

            save = False

            if rate > 0.991:
                cv2.imwrite(f'storage/data/{code}_{data["index"]}.png', image * 255)
                data['index'] += 1
                save = True

            rate = round(rate * 100)
            update_info(site, api, save)

            return Response({
                'code': code,
                'probability': rate,
                'symbol': symbol,
            })
        else:
            return


def update_info(site=False, api=False, save=False):
    f = open('storage/info.txt', 'r+')
    lines = f.readlines()

    if site:
        count = int(lines[0].split(':')[1]) + 1
        lines[0] = f'Classifications_on_site:{count}\n'
    if api:
        count = int(lines[1].split(':')[1]) + 1
        lines[1] = f'Classification_on_API:{count}\n'
    if save:
        count = int(lines[2].split(':')[1]) + 1
        lines[2] = f'Saved_images:{count}'

    f.seek(0)
    f.writelines(lines)
    f.close()
