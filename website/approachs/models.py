from django.db import models
from accounts.models import User


#این مدل برای ذخیره پیشنهادات کاربران ساخته شده است
class Approach(models.Model):
    user = models.ForeignKey(User, related_name='approach', on_delete=models.CASCADE)#با استفاده از فیلد moldes.ForeignKey مدل را به مدل User اربتاط می دهیم. به گونه ای که هر کاربر می تواند چند پیشنهاد داشته باشد اما هر پیشنهاد تنها می تواند یک کاربر داشته باشد.
    title = models.CharField(max_length=50)
    detail = models.TextField()
    positive_or_negative = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.title

#برای ذخیره پاسخ هر پیشنهاد ساخته می شود.
class ApproachAnswer(models.Model):
    approach = models.ForeignKey(Approach, on_delete=models.CASCADE, related_name='approach_answer')#در اینجا کلاس ApproachAnswer به Approach رط داده می شود به گونه ای که هر پیشنهاد میتواند پند پاسخ داشته باشد.
    approach_answer = models.TextField(default=None)

    def __str__(self):
        return f'{self.approach.user.username}, {self.approach.title}, {self.approach_answer}'
