from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'approachs'
urlpatterns = [
    path('send_approach/', views.send_approach, name='send_approach'),
    path('approach_answer/<int:id>', views.approach_answer, name='approach_answer'),
    path('delete/<int:id>', views.delete, name='delete_approach'),
    path('delete_all/', views.delete_all, name='delete_all_approachs'),
    path('edit_approach/<int:id>', views.edit_approach, name='edit_approach')
]

if settings.DEBUG is False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)