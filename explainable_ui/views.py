from io import BytesIO

from django.http import JsonResponse, HttpResponseNotFound

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ultralytics import YOLO
from fastai.vision.all import *

resize_image = Resize((640, 640), method=ResizeMethod.Pad, pad_mode="zeros")

@csrf_exempt
# HTTP Route to receive an image and pass it to the segmentation model
def segment_image_view(request):
    print(request)
    if request.method == "POST":
        # read the file of the request and store it in a variable
        file = request.FILES['file']

        # convert the file to a PIL image
        img = PILImage.create(file)

        # convert the file from png to jpg
        model = YOLO('static/best_2.onnx')
        prediction = model.predict(resize_image(img), save=True)
        # read stored file from prediction.save_dir+prediction.path with os
        print(type(prediction[0]))
        file_location = f"{prediction[0].save_dir}/{prediction[0].path}"

        result_image = PILImage.create(file_location)
        format_image = BytesIO()
        result_image.save(format_image, format="png")
        response = HttpResponse(format_image.getvalue(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="output.png"'
        return response


    else:
        return HttpResponse("Error: POST request expected").status_code(405)
