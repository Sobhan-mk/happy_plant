from django.db import models


#عکس از کاربر دریافت می شود
class PlantLeaf(models.Model):
    image = models.ImageField(upload_to='plant_leaf_images')

#این مدل بیماری های گیاهان را ذخیره و برای آنها پروفایل می سازد.
#برای هر بیماری نام عمومی، نام علمی، نام فارسی، علایم، راه های تشخیص، دلایل ایجاد و منابع اطلاعات را بیان می کند.
class PlantDiseases(models.Model):
    common_name = models.CharField(max_length=100, default='none')
    persian_name = models.CharField(max_length=100, null=True, blank=True, default='هنوز نام فارسی وجود ندارد')
    scientific_name = models.CharField(max_length=100)
    symptoms = models.TextField(null=True, blank=True, default='فعلا اطلاعاتی در دسترس نیست')
    causes = models.TextField(default='فعلا اطلاعاتی در دسترس نیست')
    detection = models.TextField(null=True, blank=True, default='فعلا اطلاعاتی در دسترس نیست')
    management = models.TextField(default='فعلا اطلاعاتی در دسترس نیست')

    image = models.ImageField(upload_to='plant_disease_image', default='none')

    refrense = models.TextField()

    def __str__(self):
        return self.common_name

    def get_refrence(self):
        return self.refrense.split('وو')





