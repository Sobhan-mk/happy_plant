from django.urls import path
from .views import external_qa_page, ask_question, edit_question, show_answers, save_answer, cpecific_answer, delete, delete_all
from django.conf.urls.static import static
from djago.conf import settings

#این اپ دارای صفحه های  :
#پرسش سوال
#ویرایش سوال
#دادن جواب
#حذف سوال
#حذف تمامی سوالات
#صفحه ای که 10 سوال و جوابهای آنها را به صورت تصادفی نمایش می دهد.
app_name = 'qa'
urlpatterns = [
    path('search/', external_qa_page, name='external_qa_page'),
    path('ask_question/', ask_question, name='ask_questions'),
    path('edit_question/<int:id>', edit_question, name='edit_question'),
    path('show_answers/<int:id>', show_answers, name='show_answers'),
    path('answer/<int:id>', save_answer, name='save_answer'),
    path('specific_answers/<int:id>', cpecific_answer, name='specific_answers'),
    path('delete/<int:id>', delete, name='delete_question'),
    path('delete-all/', delete_all, name='delete_all_questions')
]

if settings.DEBUG is False:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)