from django.shortcuts import render, redirect
from .forms import *
from .models import User, Profile
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib.auth import update_session_auth_hash
import re



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import User


#این فانکش هنگام ساخت کاربر جدید فرم مربوط به ساخت کاربر جدید رو نشان داده و اطلاتعات فرم را بررسی می کند.
def register(request):
    #اگر متد POST باشد یعنی اطلاعاتی از طرف کاربر برای ما ارسال شده و اگر متد GET باشد یعنی کاربر درخواست ننمایش صفحه را دارد.
    error_message = ''
    email_initial = request.GET.get('email', '')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST, email_initial=email_initial)
        if form.is_valid():
            data = form.cleaned_data

            if User.objects.filter(username=data['username']).exists():#چک برای وجود نداشتن نام کاربری از قبل
                error_message = 'نام کاربری قبلا ثبت شده است'
            elif User.objects.filter(email=data['email']).exists():#چک برای وجو نداشتن ایمیل از قبل
                error_message = 'ایمیل قبلا ثبت شده است'
            elif data['password_1'] != data['password_2']:#چک کردن برای مساوی بودن رمز عبور و تکرار رمز عبور
                error_message = 'رمز عبور طابقت ندارد'
            elif len(data['password_1']) <= 8:#چک می کند که طول رمز عبور حتما از 8 بیشتر باشد
                error_message = 'طول رمز عبور شما حداقل باید 10 کاراکتر باشد'
            elif not re.search(r'[A-Z]', data['password_1']):#چک میکند که در رمز عبور حروف بزرگ انگلیسی وجود داشته باشد
                error_message = 'باید در رمز عبور خود از حروف انگلیسی بزرگ استفاده کنید.'
            elif not re.search(r'\d', data['password_1']):#چک می کند که در رمز عبور اعداد وجود داشته باشد
                error_message = 'باید در رمز عبور خود از اعداد استفاده کنید.'
            elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', data['password_1']):#چک میکند که در رمز عبور علامت وجود داشته باشد
                error_message = 'باید در رمز عبور خود از علامت هایی مانند @،#،%، ... استفاده کنید.'
            else:#اگر همه شرط ها درست بودند با استفاده از مدیر مدل User و متد create_user حساب کاربری جدیدی ساخته می شود.
                User.objects.create_user(username=data['username'], email=data['email'], password=data['password_2'])
                messages.success(request, 'حساب کاربری شما ساخته شد', 'success')
                return redirect('home:home')# بازگشت به صفحه خانه
        else:
            error_message = 'آدرس ایمیل شما در قالب درستی نیست'
    else:
        form = UserRegisterForm(email_initial=email_initial)

    context = {'form': form, 'error_message': error_message}
    return render(request, 'accounts/register.html', context)


#هنگام ورود کاربر فرم ورود را نشان می دهد
def login(request):
    error_message = None
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        #در صورت تمیز بودن اطلاعات فرم فرایند ساخت کاربر اجرا می شود.
        if form.is_valid():
            data = form.cleaned_data
           #چک می کند که آیا این نام کاربری از قبل رد دیتا بیس وجود داشته است یا خیر
            if not User.objects.filter(username=data['username']).exists():
                error_message = 'کاربر یافت نشد'

            else:
                user = authenticate(request, username=data['username'], password=data['password'])
                if user is not None:
                    dj_login(request, user)

                    messages.success(request, 'ورود موفقیت آمیر بود', 'success')
                    
                    return redirect('home:home')
                else:
                    error_message = 'نام کاربری یا روز عبور اشتباه است'
                
    else:
        form = UserLoginForm()

    context = {'form': form, 'error_message': error_message}

    return render(request, 'accounts/login.html', context)

#در صفحه پروفایل، فرم به روز رسانی کاربر نمایش داده می شود و در صورت تمیز بودن اطلاعات، اطلاعات کاربری به روز رسانی می شوند.
def profile(request):
    if request.method == 'POST':

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                          request.FILES,
                                          instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'پروفایل بروز رسانی شد', 'success')

            return redirect('home:home')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    #پروفایل آن کاربر گرفته می شود
    profile = Profile.objects.get(user_id=request.user.id)
    #گیاهان خانگی موجود در پروفایل کاربر گرفته می شود.
    user_plants = profile.users_plants.all()
    #سوال های پرسیده شده توسط کاربر گرفته می شود.
    user_questions = request.user.questions.all()
    #انتقادات کاربر گرفته می شود.
    user_approachs = request.user.approach.all()
    #تمامی اطلاعات گرفته شده به template فرستاده و ننمایش داده می شود.
    context = {
        'profile' : profile,
        'user_form' : user_form, 
        'profile_form' : profile_form,
        'user_plants' : user_plants,
        'user_questions' : user_questions,
        'user_approachs' : user_approachs
    }

    return render(request, 'accounts/profile.html', context)


#با استفاده از متد logout کاربر خارج می شود.
def signout(request):
    logout(request)
    messages.success(request, 'شما خارج شدید')
    return redirect('home:home')


#در صورت درست بودن رمز عبور قدیمی و مساوی بودن رمز عبور جدید و تکرار ارمز عبور، رمز عبور کاربر تغییر پیدا می کند.
#این ویو مشابه ویو ساخت حساب کاربری عمل می کند.
def change_password(request):
    error = ''
    if request.method == 'POST':
        form = ChangePassword(data=request.POST)

        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            repeat_password = form.cleaned_data['repeat_password']
            if request.user.check_password(old_password):
                if new_password == repeat_password:
                    if len(new_password) <= 8:
                        error = 'رمز عبور شما باید حداقل دارای 8 کاراکتر باشد'
                    elif not re.search(r'[A-Z]', new_password):
                        error = 'باید در رمز عبور شما حروف بزرگ انگلیسی وجود داشته باشد'
                    elif not re.search(r'\d', new_password):
                        error = 'رمز عبور شما باید شامل اعداد باشد'
                    elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                        error = 'رمز عبور شما یاید شامل علامت هایی مثل @،#،... باشد.'
                    else:
                        request.user.set_password(new_password)
                        request.user.save()

                        update_session_auth_hash(request, request.user)

                        messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')
                        return redirect('accounts:profile')

                else:
                    error = 'رمز عبور جدید با تکرار آن مطابقت ندارد'
            else:
                error = 'رمز عبور قدیمی شما درست نیست'

    else:
        form = ChangePassword()

    context = {
        'form': form,
        'error': error
    }

    return render(request, 'accounts/change_password.html', context)
