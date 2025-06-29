from django.contrib import admin
from .models import Approach, ApproachAnswer

#مدل پیشنهادات را در ادمین پنل نمایش می دهیم.
admin.site.register(Approach)
admin.site.register(ApproachAnswer)
