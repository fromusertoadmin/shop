# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render
from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count, Prefetch
# from utils.emails import SendingEmail

from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

from untitled6.settings import FROM_EMAIL, EMAIL_ADMIN
from emails.models import EmailSendingFact
from django.forms.models import model_to_dict

def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, order=None, defaults={"nmb": nmb})
        if not created:
            print ("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    #common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in  products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print (products_in_basket)
    for item in products_in_basket:
        print(item.order)

    form=CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            email = data["email"]
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1,
                                         customer_email=email)

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,
                                                  order=order)

            email = SendingEmail()
            email.sending_email(type_id=1, order=order)
            email.sending_email(type_id=2, email=order.customer_email, order=order)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())


class SendingEmail(object):
    from_email = "BestShopEver <%s>" % FROM_EMAIL
    reply_to_emails = [from_email]
    target_emails = []
    bcc_emails = []

    def sending_email(self, type_id, email=None, order=None):

        if not email:
            email = EMAIL_ADMIN

        target_emails = [email]

        readyr = dict()

        if type_id == 1:
            subject = "Новый заказ"
            readyr["order_fields"] = model_to_dict(order)
            readyr["order"] = order
            readyr["products_in_order"] = order.productinorder_set.filter(is_active=True)
            message = get_template('emails_templates/order_notification_admin.html').render(readyr)

        elif type_id == 2:
            subject = 'Ваш заказ в итнтернет магазине получен!'
            readyr["order_fields"] = model_to_dict(order)
            readyr["order"] = order
            readyr["products_in_order"] = order.productinorder_set.filter(is_active=True)
            message = get_template('emails_templates/order_notification_customer.html').render(readyr)

        msg = EmailMessage(
                        subject, message, from_email=self.from_email, to=target_emails,
                        bcc=self.bcc_emails, reply_to=self.reply_to_emails
        )

        msg.content_subtype = 'html'
        msg.mixed_subtype = 'related'
        msg.send()

        kwargs = {
            "type_id": type_id,
            "email": email
        }
        if order:
            kwargs["order"] = order
        EmailSendingFact.objects.create(**kwargs)

        print('Email was sent successfully!')