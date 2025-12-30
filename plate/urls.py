from django.urls import path
from .views import index, detect

urlpatterns = [
    path('', index),           # 首页
    path('detect/', detect),   # YOLO 检测接口
]
