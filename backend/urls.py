from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 前端页面 + 识别接口
    path('', include('plate.urls')),
]

# ⚠️ 非常关键：开发环境下让 Django 能访问识别结果图片
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
