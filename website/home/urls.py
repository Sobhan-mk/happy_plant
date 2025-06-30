from django.urls import path
from .views import home
from django.conf import settings
from django.conf.urls.static import static


app_name = "home"
urlpatterns = [
    path('', home, name="home")
]

if settings.DEBUG is False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)