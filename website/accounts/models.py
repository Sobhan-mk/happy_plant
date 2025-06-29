from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from my_plants.models import Plants

#ساخت مدیر کلاس کاربر برای ساخت حساب کاربری معمولی و ساخت کاربر ادمین یا superuser
class UserManager(BaseUserManager):
    #ساخت حساب کاربری معمولی
    def create_user(self, username, email, password):
        if not username:
            raise ValueError('plz enter username')
        
        if not email:
            raise ValueError('plz enter email')
        
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user
    #ساخت حساب کاربری ادمین که قابلتی دسترسی به ادمین پنل را دارد
    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        
        user.is_admin = True

        user.save(using=self._db)

        return user
        

#custom user model:مدل کاربر شاخصی سازی شده
class User(AbstractBaseUser):
    #فیلد های مورد نیاز برای ساخت حساب کاربری
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ['email']

    #معرفی مدیر مدل کاربر
    objects = UserManager()

    #در صورت فراخوانی اسم کلاس User این متد اجرا میشود
    def __str__(self):
        return self.username

    #دسترسی های کاربر رو مورد بررسی قرار میدهد
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin


#مدل پورفایل که اطلاعات مربوط به اون کاربر یا اطلاعات اضافه همراه با اطلاعات کاربر رو در خودش ذخیره می کنه
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    users_plants = models.ManyToManyField(Plants, blank=True)

    def __str__(self):
        return f'{self.user.username} profile'





