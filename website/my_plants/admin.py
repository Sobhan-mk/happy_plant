from django.contrib import admin
from .models import Plants

#لیست گیاهان را در ادمین پنل نمایش می دهد.
admin.site.register(Plants)

