from django.http import JsonResponse

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
# HTTP Route to receive an image and pass it to the segmentation model
def segment_image_view(request):
    if request.method == "POST":
        print("Received POST request")
        return HttpResponse("Received POST request").status_code(200)
    else:
        return HttpResponse("Error: POST request expected").status_code(405)