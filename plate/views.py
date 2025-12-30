import os
import uuid
import cv2
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO


# ======================
# 模型加载（只加载一次）
# ======================
PLATE_MODEL = YOLO(os.path.join(settings.BASE_DIR, 'weights', 'license_plate_detector.pt'))
COMMON_MODEL = YOLO(os.path.join(settings.BASE_DIR, 'weights', 'yolov8n.pt'))


def index(request):
    """前端页面"""
    return render(request, 'index.html')


@csrf_exempt
def detect(request):
    """YOLO 检测接口"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'})

    image_file = request.FILES.get('image')
    detect_type = request.POST.get('type')

    if not image_file:
        return JsonResponse({'error': 'No image uploaded'})

    # ========= 保存上传图片 =========
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    img_name = f"{uuid.uuid4().hex}.jpg"
    img_path = os.path.join(upload_dir, img_name)

    with open(img_path, 'wb+') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    img = cv2.imread(img_path)

    # ========= 选择模型 =========
    if detect_type == 'plate':
        model = PLATE_MODEL
        classes = None
    elif detect_type == 'person':
        model = COMMON_MODEL
        classes = [0]  # person
    elif detect_type == 'car':
        model = COMMON_MODEL
        classes = [2]  # car
    elif detect_type == 'traffic_light':
        model = COMMON_MODEL
        classes = [9]  # traffic light
    else:
        return JsonResponse({'error': 'Invalid detect type'})

    # ========= YOLO 推理 =========
    results = model(img, classes=classes)
    annotated_img = results[0].plot()

    # ========= 保存结果图片 =========
    result_dir = os.path.join(settings.MEDIA_ROOT, 'results')
    os.makedirs(result_dir, exist_ok=True)

    result_name = f"result_{uuid.uuid4().hex}.jpg"
    result_path = os.path.join(result_dir, result_name)

    cv2.imwrite(result_path, annotated_img)

    # ========= 返回给前端 =========
    return JsonResponse({
        'image_url': settings.MEDIA_URL + 'results/' + result_name
    })
