from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.urls import reverse
from django.http import HttpResponse, Http404
import azbankgateways
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException
from books.models import Book
from pages.views import cart_view
from allauth.account.models import EmailAddress
from .models import Cart, OrderInfo, OrderedProductsInfo

# Create your views here.
    

def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    if request.method == 'POST':
        # Get the product ID and amount from the form POST data
        email = EmailAddress.objects.get(user=request.user)
        cart_items = Cart.objects.filter(user=email)
        price = 0
        for item in cart_items:
            price += item.product.price * item.quantity

    # amount = 50000
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = "+989112221234"  # اختیاری

    factory = bankfactories.BankFactory()

    try:
        # print(str(bank_models.BankType.PAYV1))
        bank = (
            factory.create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(price)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse("callback-gateway"))
        bank.set_mobile_number(user_mobile_number)  # اختیاری

        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید.
        bank_record = bank.ready()
        request.session['tracking_code'] = bank_record.tracking_code
        bank_object = bank_models.banks.Bank.objects.get(tracking_code=bank_record.tracking_code)
        print(str(bank_object.bank_type))
        bank_object.callback_url = reverse("callback-gateway")
        print(f"Info 1: Tracking Code is: {bank_record.tracking_code}, Callback URL is: {bank_object.callback_url}")
        # request.session['created_at'] = str(bank_record.created_at)
        

        # هدایت کاربر به درگاه بانک
        context = bank.get_gateway()
        return render(request, "redirect_to_bank.html", context=context)
    except AZBankGatewaysException as e:
        logging.critical(e)
        return render(request, "redirect_to_bank.html")
    
def successful_payment(request):
    template = 'success.html'
    tracking_code = request.session.get('tracking_code')
    context = {}
    context['tracking_code'] = tracking_code
    for key in list(request.session.keys()):
        if not key.startswith("_"):
            del request.session[key]
    return render(request, template, context)

def failed_payment(request):
    template = 'failure.html'
    tracking_code = request.session.get('tracking_code')
    context = {}
    context['tracking_code'] = tracking_code
    for key in list(request.session.keys()):
        if not key.startswith("_"):
            del request.session[key]
    return render(request, template, context)


def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404
    
    if str(bank_record.status).lower() == 'complete':
        status = 'Successful'
    else:
        status = 'Failed'

    email = EmailAddress.objects.get(user=request.user)
    order_info = OrderInfo.objects.create(
        gateway_id=int(bank_record.pk),
        user=email,
        price=(bank_record.amount),
        tracking_code=tracking_code,
        created_at=bank_record.created_at,
    )
    # delete duplicates
    duplicates = OrderInfo.objects.filter(tracking_code=tracking_code)
    if len(duplicates) > 1:
        for i in duplicates:
            if i != duplicates[0]:
                i.delete()
    print(str(bank_record.status))
    cart_items = Cart.objects.filter(user=email).all()
    for item in cart_items:
        OrderedProductsInfo.objects.create(
            order=OrderInfo.objects.get(tracking_code=tracking_code),
            product=item.product,
            quantity=item.quantity,
        )

    total_products = len(OrderedProductsInfo.objects.filter(order=OrderInfo.objects.get(tracking_code=tracking_code)))
    OrderInfo.objects.get(tracking_code=tracking_code).total_products = total_products

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.

        # delete cart items after success
        cart_items.delete()
        # make it so that the data in the session will be reset and deleted after the success page is shown
        return redirect('success')

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    # the failed payments should be recorded and shown in the profile as well
    return redirect('failure')


