from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),                      # <-- все твои ViewSet-ы
    path('api/auth/', include('djoser.urls')),              # <-- регистрация, users/me/
    path('api/auth/', include('djoser.urls.authtoken')),    # <-- логин/логаут через токены
    # path('api/users/', include('users.urls')),            # <-- если у тебя нет кастомного users.urls — УБРАТЬ
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)