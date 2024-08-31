from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.urls import reverse
from django.http import HttpResponse, Http404
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException
from books.models import Book

# Create your views here.
# This view is for when there's a Purchase button in the book_details page only

def go_to_gateway_view(request):
    # خواندن مبلغ از هر جایی که مد نظر است
    if request.method == 'POST':
        # Get the product ID and amount from the session
        expected_product_id = request.session.get('selected_product_id')
        expected_price = request.session.get('selected_product_price')

        # Get the product ID and amount from the form POST data
        product_id = request.POST.get('product_id')
        price = int(get_object_or_404(Book, id=product_id).price)

    # amount = 50000
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = "+989112221234"  # اختیاری

    factory = bankfactories.BankFactory()

    # Validate that the POSTed product ID and amount match the session data
    if str(product_id) == str(expected_product_id) and price == int(expected_price): 
        try:
            bank = (
                factory.create(bank_models.BankType.ZIBAL)
            )  # or factory.create(bank_models.BankType.BMI) or set identifier
            bank.set_request(request)
            bank.set_amount(price)
            # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
            bank.set_client_callback_url(reverse("callback-gateway"))
            bank.set_mobile_number(user_mobile_number)  # اختیاری

            # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
            # پرداخت برقرار کنید.
            bank_record = bank.ready()

            # هدایت کاربر به درگاه بانک
            context = bank.get_gateway()
            return render(request, "redirect_to_bank.html", context=context)
        except AZBankGatewaysException as e:
            logging.critical(e)
            return render(request, "redirect_to_bank.html")
    else:
        return redirect(f"/book/{expected_product_id}/")
    

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

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        return HttpResponse("پرداخت با موفقیت انجام شد.")

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
    )
    



