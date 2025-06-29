from django.db import models


#مدلی است که اطلاعات مربوط به گیاهان را ذخیره و برای آنها پروفایل می سازد.
#برای هر گیاه نام معمولی، نام علمی، نام فارسی، توضیحات، شرابط نگهاری و شرابط نگهداری به صورت فیلد های جداگانه را ذخیره می کند.
class Plants(models.Model):
    name = models.CharField(unique=True, max_length=100)
    scientific_name = models.CharField(unique=True, max_length=200, default='')
    persian_name = models.CharField(max_length=100, default='')

    description = models.TextField(default='')

    conditions = models.TextField(default='')

    deseases = models.TextField(default='')

    plant_image = models.ImageField(upload_to='plant_images/', null=True, blank=True)

    #features
    light = models.CharField(max_length=100, choices=[('low', 'کم'),
                                                      ('medium', 'متوسط'),
                                                      ('high', 'زیاد')], blank=True, default='')

    temperature = models.CharField(max_length=100, choices=[('warm', 'گرم'),
                                                           ('medium', 'متوسط'),
                                                           ('cold', 'سرد')], blank=True, default='')

    water = models.CharField(max_length=100, choices=[('high', 'زیاد'),
                                                      ('medium', 'متوسط'),
                                                      ('low', 'کم')], blank=True, default='')

    soil_type = models.CharField(max_length=100, choices=[('Loamy Soil', 'خاک لومی'),
                                                          ('Sandy Soil', 'خاک ماسه ای'),
                                                          ('Clay Soil', 'خاک رس'),
                                                          ('Peat Soil', 'خاک پیت'),
                                                          ('Chalky soil', 'خاک گچی'),
                                                          ('Silty Soil', 'خاک سیلتی'),
                                                          ('no soil', 'بدون خاک')], blank=True, default='')

    def __str__(self):
        return self.name

