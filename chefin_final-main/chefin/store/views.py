from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from chefin.settings import POSTER_POS_API_KEY
from django.shortcuts import render
from .helpers import *
from .models import *
import requests
from chefin.settings import POSTER_POS_API_KEY
from cloudipsp import Api, Checkout
from django.shortcuts import render, HttpResponseRedirect
from .helpers import *
from .models import *
from store.templatetags.custom_filters import mul_price
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.cache import cache
from decimal import Decimal
import json


def menu(request):
    api_key = POSTER_POS_API_KEY
    fill_database(api_key)

    query = request.GET.get('query')
    category = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category__icontains=category)

    context = {
        'title': 'Chefin',
        'products': products,
        'product_id': products.values_list('product_id', flat=True),
    }

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Если заголовок 'HTTP_X_REQUESTED_WITH' содержит значение 'XMLHttpRequest',
        # то это может быть AJAX-запрос
        product_data = []
        for product in products:
            product_data.append({
                'name': product.name,
                'category': product.category,
                # Добавьте другие поля продукта, которые вам необходимы
            })
        return JsonResponse({'products': product_data})

    return render(request, 'store/base.html', context)


def rolu(requests):
    products = Product.objects.all()

    context = {
        'title': 'Роли',
        'products': products,
    }

    return render(requests, 'store/rolu.html', context)


def pizza(requests):
    products = Product.objects.all()

    context = {
        'title': 'Піца',
        'products': products,
    }

    return render(requests, 'store/pizza.html', context)


def salat(requests):
    products = Product.objects.all()

    context = {
        'title': 'Салати',
        'products': products,
    }

    return render(requests, 'store/salat.html', context)


def osnovni(requests):
    products = Product.objects.all()

    context = {
        'title': 'Основні страви',
        'products': products,
    }

    return render(requests, 'store/osnovni.html', context)


def soups(requests):
    products = Product.objects.all()

    context = {
        'title': 'Супи',
        'products': products,
    }

    return render(requests, 'store/soups.html', context)


def zakyski(requests):
    products = Product.objects.all()

    context = {
        'title': 'Закуски',
        'products': products,
    }

    return render(requests, 'store/zakyski.html', context)


def garniry(requests):
    products = Product.objects.all()

    context = {
        'title': 'Гарніри',
        'products': products,
    }

    return render(requests, 'store/garniry.html', context)


def hot(requests):
    products = Product.objects.all()

    context = {
        'title': 'Гарячі страви',
        'products': products,
    }

    return render(requests, 'store/hot.html', context)


def cold_drinks(requests):
    products = Product.objects.all()

    context = {
        'title': 'Холодні напої',
        'products': products,
    }

    return render(requests, 'store/cold_drinks.html', context)


def beer(requests):
    products = Product.objects.all()

    context = {
        'title': 'Розливне пиво',
        'products': products,
    }

    return render(requests, 'store/beer.html', context)


def dostavka_ta_oplata(requests):
    context = {
        'title': 'Доставка та оплата',

    }

    return render(requests, 'store/dostavka_ta_oplata.html', context)


def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    request.session.setdefault('basket', {})
    basket = request.session['basket']

    # Получение данных из тела запроса
    data = json.loads(request.body)
    comment = data.get('comment')
    product_poster = data.get('product_poster')

    # Создание JSON-представления товара с комментарием и постером
    product_json = product.to_json()
    product_json['comment'] = comment
    product_json['product_poster'] = product_poster

    basket[product_id] = product_json

    request.session.modified = True
    return HttpResponseRedirect(request.META['HTTP_REFERER'])






def basket_remove(request, product_id):
    basket = request.session.get('basket', {})


    if str(product_id) in basket:
        del basket[str(product_id)]
        request.session['basket'] = basket
        request.session.modified = True

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return JsonResponse({'success': False})


def profile(request):
    # Получаем текущую корзину из сессии пользователя
    basket = request.session.get('basket', {})
    basket_items = []
    for product_id, item in basket.items():
        item['id'] = product_id
        basket_items.append(item)

    context = {
        'title': 'Корзина',
        'baskets': basket_items,
        'mul_price': mul_price,
        'savedValue': 1,
    }
    return render(request, 'store/baskets.html', context)



def add_to_cart(request):
    api = Api(merchant_id=1397120,
              secret_key='Not for tests. Test credentials: https://docs.fondy.eu/docs/page/2/ ')
    checkout = Checkout(api=api)
    data = {
        "currency": "UAH",
        "amount": 12000
    }
    url = checkout.url(data).get('checkout_url')
    context = {
        'title': 'Store',
        'url': url
    }
    return render(request, 'store/add_to_cart.html', context)


def inform(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        quantity = body.get('number')
        product_poster = body.get('product_poster')
        print(quantity)
        print(product_poster)
        if quantity is not None:
            # Обработка значения quantity
            # ...

            # Возвращаем успешный JSON-ответ
            return JsonResponse({'status': 'success', 'message': 'Value received'})

    # Возвращаем JSON-ответ об ошибке
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def zayvka(request):
    return render(request, 'store/zayvka.html')

class Search(ListView):
    template_name = 'store/search_results.html'
    context_object_name = 'news'
    paginate_by = 45

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        if query:
            self.queryset = Product.objects.filter(Q(name__icontains=query) | Q(category__icontains=query))
            if self.queryset.exists():
                return super().get(request, *args, **kwargs)
        return redirect('menu')  # Перенаправляем на другую страницу, например, 'menu'




