from django.shortcuts import render, redirect
from .forms import SendApproach
from django.contrib import messages
from .models import Approach, ApproachAnswer

#ارسال پیشنهاد
def send_approach(request):
    if request.method == 'POST':
        form = SendApproach(request.POST)

        if form.is_valid():
            approach = form.save(commit=False)# از ذخیره فرم و اطلاعات آن چلوگیری می کنیم تا اطلاعاتی دیگر که به صورت پیشفرض ذخیره نمنی شوند را ذخیره کنیم
            approach.user = request.user#برای هر پشنهاد یک کاربر ذخیره می کنیم. یعنی این کاربر این پیشنهاد را ارسال کرده است که یک آبجکت از کلاس User است.
            approach.save()# فرم را ذخیره می کنیم.

            #به صورت پیشفرض برای هر پیشنهاد یک پاسخ در نظر می گیریم.
            approach_answer = ApproachAnswer(approach=approach, approach_answer="هنوز جوابی وجود ندارد")
            approach_answer.save()

            messages.success(request, 'پیشنهاد شما با موفقیت ثبت و در نزدیک ترین زمان به آن رسیدگی میشود')
            return redirect('accounts:profile')
    else:
        form = SendApproach()

    return render(request, 'approachs/send_approachs.html', {'form': form})


def approach_answer(request, id):
    approach = Approach.objects.get(id=id)#لینک مشاهده این فانکشن در صفحه پروفایل وجود دارد و همراه با لینک ارحاع به این صفحه، id مربوط به پیشنهاد نمنایش داده شده هم ارسال می گردد. در نتیجه با استفاده از این id پیشنهاد را دریافت می کنیم.

    approach_answer = approach.approach_answer.get()#پیشنهاد دریافت شده را با استفاده از متد get دریافت می کنیم و برای کاربر ارسال می کنیم.

    return render(request, 'approachs/answer.html', {'answer' : approach_answer})


def delete(request, id):
    approach = Approach.objects.get(id=id)#با استفاده از آ دی دریافت شده از لینک ارجاع دهنده، پیشنهاد را گرفته و با استفاده از متد delete آن را حذف می کنیم.
    approach.delete()

    messages.success(request, 'پیشنهاد شما با موفقیت حذف شد')
    return redirect('accounts:profile')


def delete_all(request):
    approachs = request.user.approach.all()#تمامی پیشنهادات مریوط به آن کاربر را دریافت می کنیم و حذف می کنیم.
    approachs.delete()

    messages.success(request, 'تمامی پیشنهادات حذف شدند')
    return  redirect('accounts:profile')


def edit_approach(request, id):
    approach = request.user.approach.get(id=id)#با استفاده از آی دی دریافت شده از لینک ارجاع دهنده پیشنهاد رو دریافت می کنیم.
    #از فرم SendApproach برای تغییر ایجاد کردن در پیشنهادات نیز استفاده می کنیم.
    if request.method == 'POST':
        form = SendApproach(request.POST, instance=approach)#اطلاعات مربوط به پیشنهاد را دریافت کرده و تغییرات و اطلاعات وارد شده در فرم را روی آن پیشنهاد اعمال می کنیم.

        if form.is_valid():
            edited_approach = form.save(commit=False)
            edited_approach.user = request.user

            edited_approach.save()
            return redirect('accounts:profile')

    else:
        form = SendApproach(instance=approach)

        return render(request, 'approachs/edit_approach.html', {'form' : form})

