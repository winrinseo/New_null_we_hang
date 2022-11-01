from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from PIL import Image 
from rest_framework.response import Response
import base64
from io import BytesIO
import pyzbar.pyzbar as pyzbar
import requests
import json

# Create your views here.
apikey = "f697a7b1127e4141af74"

parsed_data = {}
def main():
    try:
        st = 1
        while(True):
            url = "http://openapi.foodsafetykorea.go.kr/api/f697a7b1127e4141af74/C005/json/"+str(st)+"/"+str(st+999)
            print(url)
            data = requests.get(url)
            jsondata = json.loads(data.text)
            print(jsondata['C005']['total_count'])
            if(jsondata['C005']['total_count'] == "0"): 
                print(jsondata)
                if(jsondata['C005']['RESULT']['CODE'] == "ERROR-500"):
                    continue
                else : break
            for js in jsondata['C005']['row']:
                parsed_data[js['BAR_CD']] = js['PRDLST_NM']

            st += 1000
    except:
        print(jsondata)


def index(request,barcode_id):
    print(parsed_data[str(barcode_id)])
    return HttpResponse("Hello World")

def read_frame(frame):
        try:
            # 바코드 정보 decoding
            barcodes = pyzbar.decode(frame)
            # 바코드 정보가 여러개 이기 때문에 하나씩 해석
            for barcode in barcodes:
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

        barcode = str(read_frame(img))
        ret = 0
        text = "찾는 제품이 없습니다."
        if(barcode in parsed_data):
            ret = 1
            text = parsed_data[barcode]
        print(barcode,text)
        return JsonResponse(dict(result = ret, text = text))
    


main()
