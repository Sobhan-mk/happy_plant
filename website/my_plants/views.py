from django.shortcuts import render, redirect
from .models import Plants
from django.shortcuts import get_object_or_404
from .forms import SearchPlantNames, PlantRecommendation
from accounts.models import Profile
from django.contrib import messages
from django.db.models import Q


def house_plants_names(request):
    plant_names = Plants.objects.all()#تمامی گیاهان دریافت می شوند.

    if request.method == 'POST':
        #فرم جستوجو و فیلتر تعریف می شوند.
        search_form = SearchPlantNames(request.POST)
        filter_form = PlantRecommendation(request.POST)

        #در صورتی که نام تگ form در اطلاعات ارسال شده این ویو به نام search پر باشد، این قسمت اجرا می شود.
        if 'search' in request.POST:
            if search_form.is_valid():
                query = search_form.cleaned_data['query']#کلمه یا عبارت جستوجو شده را دریافت می کنیم.
                #با استفاده از مازول Q میتوانیم جستوجو هوشمند تری انجام دهیم. برای مصال اگر نیمی از نام گیاه هم نوشته شود، عمل جستوجو به درستی کار می کند و گیاه یافت می شود.
                #جستوجو علاوه بر نام عامیانه، در نام علمی و نا فارسی هم اجرا می شود.
                plant_names = Plants.objects.filter(
                    Q(name__icontains=query) |
                    Q(persian_name__icontains=query) |
                    Q(scientific_name__icontains=query)
                )
        #اگر در اطلاعات ارسال شده فرمی که نام filter دارد پر شده باشد، این قسمت اجرا می شود.
        elif 'filter' in request.POST:
            if filter_form.is_valid():
                #مفادیر نور و آب و دما و نوع خاک از فرم دریافت می شوند.
                light = filter_form.cleaned_data['light']
                water = filter_form.cleaned_data['water']
                temperature = filter_form.cleaned_data['temperature']
                soil_type = filter_form.cleaned_data['soil_type']
                #عمل جستوجو مشابه فسمت قبل انجام می شود.
                plant_names = Plants.objects.filter(
                    light__icontains=light,
                    water__icontains=water,
                    temperature__icontains=temperature,
                    soil_type__icontains=soil_type
                )
    else:
        search_form = SearchPlantNames()
        filter_form = PlantRecommendation()

    context = {
        'search_form': search_form,
        'filter_form': filter_form,
        'plant_names': plant_names,
    }

    return render(request, 'my_plants/house_plants_names.html', context)


def plant_detail(request, id):
    plant = get_object_or_404(Plants, id=id)#با استفاده از id دریافتی از لینک ارجاع دهنده گیاه مربوطه گرفته می شود
    if request.user.is_authenticated:#اگر کاربر اعتبار سنجی شده باشد، یا اگر وارد شده باشد و دارای حساب کاربری باشد، اینقسمت اجرا می شود.
        profile = get_object_or_404(Profile, user=request.user)#پروفایل و گیاهان ذخیره شده در پروفایل کاربر دریافت می شود تا در صورت وجود این گیاه در گیاهان خانگی ذخیره شده کاربر، به جای دکمه اضافه کردن، دکمه حذف این گیاه نمایش داده شود.
        user_plants = profile.users_plants.all()

        context = {'plant' : plant, 'user_plants' : user_plants}
    else:
        context = {'plant': plant}
    return render(request, 'my_plants/plant_detail.html', context)


def user_plant_adder(request, plant_id):

    plant = get_object_or_404(Plants, id=plant_id)#مانند فرایند پیشین گیاه را دریافت می کنیم
    if request.user.is_authenticated:#اگر کاربر  وارد شده باشد پروفایل کاربر را دریافت کرده و گیاه را به گیاهان خانگی پروفایل کاربر اضافه می کنیم
        profile = get_object_or_404(Profile, user=request.user)

        profile.users_plants.add(plant)
        profile.save()

        messages.success(request, f'{plant.name} به گیاهان شما اضافه شد.', "success")
        return redirect('my_plants:house_plants_names')
    else:
        return redirect('accounts:login')


def user_plant_remover(request, plant_id):
    plant = get_object_or_404(Plants, id=plant_id)#مشابه اضافه کردن عمل می کند. تنها تفاوت این است که به جای اضافه کردن گیاه، گیاه را حذف می کند.
    profile = get_object_or_404(Profile, user=request.user)

    messages.success(request, f'{plant.name} از گیاهان شما حذف شد', "success")

    profile.users_plants.remove(plant)
    return redirect('my_plants:house_plants_names')


def user_plant_remover_all(request):
    profile = get_object_or_404(Profile, user=request.user)#تمامی گیاهان کاربر گرفته شده و حذف می شوند.

    messages.success(request, 'تمام گیاهان حذف شدند ', "success")

    profile.users_plants.clear()
    return redirect('my_plants:house_plants_names')
