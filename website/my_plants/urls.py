from django.contrib.auth.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

#برای نشان دادن توضیحات و پروفایل هر گیاه، حذف و اضافه کردن گیاهان به پروفال کاربر باید id گیاه از طرف لینک ارجاع دهنده دریافت شود.
app_name = 'my_plants'
urlpatterns = [
    path('house plants names/', views.house_plants_names, name='house_plants_names'),
    path('house plants names/<int:id>/', views.plant_detail, name='plant_detail'),
    path('plant_adder/<int:plant_id>/', views.user_plant_adder, name='user_plant_adder'),
    path('plant_remover/<int:plant_id>/', views.user_plant_remover, name='user_plant_remover'),
    path('plant_remover_all/', views.user_plant_remover_all, name='user_plant_remover_all'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
