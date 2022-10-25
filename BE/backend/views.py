from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from PIL import Image 
from rest_framework.response import Response
import base64
from io import BytesIO
import pyzbar.pyzbar as pyzbar

# Create your views here.


def index(request):
    return HttpResponse("Hello World")

def read_frame(frame):
        try:
            # 바코드 정보 decoding
            barcodes = pyzbar.decode(frame)
            # 바코드 정보가 여러개 이기 때문에 하나씩 해석
            for barcode in barcodes:
                # 바코드 rect정보
                x, y, w, h = barcode.rect
                # 바코드 데이터 디코딩
                barcode_info = barcode.data.decode('utf-8')
                # 인식한 바코드 사각형 표시
            return barcode_info
        except Exception as e:
            print(e)

class inferance(APIView):
    

    def post(self,request) :
        print("Post Request")
        rowimg = request.data
        img = Image.open(BytesIO(base64.b64decode(rowimg['img']['base64'])))

        barcode = read_frame(img);
        print(barcode)
        return JsonResponse(dict(result = barcode))