from django.db import models
from accounts.models import User

#مدلی است که برای ثبت سوال ساخته شده است.
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')#هر سوال یک فیلد به نام user دارد که بیان کننده کاربر ثبت کننده آن است. به گونه ای که با مدل User در ارتباط است و هر کاربر می تواند چندسوال داشته باشد
    #هر سوال می تواند درباره یکی از موضوعات زیر باشد
    topics = (
        ('a', 'مشکل یا بیماری گیاهان'),
        ('b', 'نحوه نگهداری'),
        ('c', 'مواد مغذی گیاهان'),
        ('d', 'ظاهر گیاهان'),
        ('e', 'اطلاعات عمومی درباره گیاهان'),
        ('f', 'روش های تکثیر گیاهان'),
        ('g', 'زادگاه گیاهان'),
        ('h', 'خاک گیاه'),
        ('i', 'آب گیاه'),
        ('j', 'نور گیاه'),
        ('k', 'دما و رطوبت گیاه'),
        ('l', 'هرس کردن گیاه'),
        ('m', 'محصولات گیاه'),
        ('n', 'نام کاشف'),
        ('o', 'محل اکتشاف'),
        ('p', 'نام علمی گیاهان'),
        ('q', 'نام فارسی گیاهان'),

    )

    topic = models.CharField(max_length=100, choices=topics, blank=True, null=True)

    title = models.CharField(max_length=100)
    detail = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#این مدل بریا ذخیره جواب ساخته شده است
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)#هر جواب می تواند یک سوال داشته باشد.
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    detail = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} to: {self.question.title}"


