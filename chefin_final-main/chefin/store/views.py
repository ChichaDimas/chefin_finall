from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
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
from django.http import HttpResponseBadRequest


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


def cart_info(request):
    # Получение текущей корзины из сессии пользователя
    basket = request.session.get('basket', {})
    basket_items = []
    for product_id, item in basket.items():
        item['id'] = product_id
        basket_items.append(item)
    print(basket_items)

    # Получение списка значений product_poster из товаров в корзине
    product_posters = [item['product_poster'] for item in basket_items]
    print(product_posters)

    # Возврат информации о товарах в корзине в формате JSON
    return JsonResponse({'items': basket_items, 'product_posters': product_posters})


def basket_add(request, product_id):
    # Получение данных из тела запроса
    data = json.loads(request.body)
    comment = data.get('comment')
    product_poster = data.get('product_poster')
    price = data.get('price')
    name = data.get('name')
    image = data.get('image')
    description = data.get('description')

    # Создание JSON-представления товара с комментарием и постером
    product_json = {
        'comment': comment,
        'product_poster': product_poster,
        'price': price,
        'name': name,
        'image': image,
        'description': description,
    }

    # Получение или инициализация корзины в сессии пользователя
    basket = request.session.get('basket', {})

    # Проверка, что товар уже присутствует в корзине
    if str(product_id) in basket:
        print('есть в корзине')
        return JsonResponse({'success': False, 'message': 'Product already exists in the basket.'})

    # Добавление товара в корзину
    basket[str(product_id)] = product_json

    # Обновление корзины в сессии пользователя
    request.session['basket'] = basket
    request.session.modified = True

    return JsonResponse({'success': True})



def basket_remove(request, product_id):
    # Получение текущей корзины из сессии пользователя
    basket = request.session.get('basket', {})

    # Проверка, что товар с данным ID присутствует в корзине
    if str(product_id) in basket:
        del basket[str(product_id)]
        request.session['basket'] = basket
        request.session.modified = True

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Product not found in the basket.'})


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
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        street = request.POST.get('street')
        home_number = request.POST.get('home_number')
        home_gear = request.POST.get('home_gear')
        home_room = request.POST.get('home_room')
        delivery_time = request.POST.get('delivery_time')
        delivery_count = request.POST.get('delivery_count')
        comment_do_zakaza = request.POST.get('comment_do_zakaza')


        print(name)
        print(number)
        print(street)
        print(home_number)
        print(home_gear)
        print(home_room)
        print(delivery_time)
        print(delivery_count)
        print(comment_do_zakaza)

        return redirect('zayvka')

    # return redirect('zayvka')
    return render(request, 'store/zayvka.html')




def add_to_cart(request):
    # Инициализация API-клиента Fondy

    print('syka_bliattt')

    api = Api(merchant_id='1397120', secret_key='Not for tests. Test credentials: https://docs.fondy.eu/docs/page/2/')

    # Создание объекта Checkout для проведения платежа
    checkout = Checkout(api=api)

    # Параметры платежа
    order_id = '12345'  # Уникальный идентификатор заказа
    amount = 12000  # Сумма платежа в валюте (например, в копейках)
    currency = 'UAH'  # Код валюты (например, 'USD', 'EUR', 'UAH')
    description = 'Оплата заказа'  # Описание платежа

    # Параметры клиента
    email = 'customer@example.com'  # Email клиента
    phone = '+1234567890'  # Телефон клиента

    # Создание платежа
    data = {
        'order_id': order_id,
        'amount': amount,
        'currency': currency,
        'description': description,
        'email': email,
        'phone': phone,
        'server_callback_url': 'https://your-server-callback-url.com',  # URL для обработки уведомлений о платеже
        # Дополнительные параметры платежа (если необходимо)
        # 'param1': 'value1',
        # 'param2': 'value2',
    }

    # Получение URL платежной страницы
    try:
        response = checkout.url(data)
        checkout_url = response.get('checkout_url')
        return JsonResponse({'url': checkout_url})
    except Exception as e:
        return HttpResponse(str(e), status=500)




# def add_to_cart(request):
#     print("функция сработала")
#     api_url = 'https://api.fondy.eu/api/checkout/url/'
#     merchant_id = '1397120'
#     secret_key = 'Not for tests. Test credentials: https://docs.fondy.eu/docs/page/2/'
#
#     data = {
#         "currency": "UAH",
#         "amount": 12000
#     }
#
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Basic {merchant_id}:{secret_key}'
#     }
#
#     response = requests.post(api_url, json=data, headers=headers)
#     if response.status_code == 200:
#         checkout_url = response.json().get('checkout_url')
#         response_data = {
#             'url': checkout_url
#         }
#         return JsonResponse(response_data)
#     else:
#         # Обработка ошибки, если необходимо
#         return HttpResponse('Error')



# def add_to_cart(request):
#     print(9999)
#     api = Api(merchant_id=1397120,
#               secret_key='Not for tests. Test credentials: https://docs.fondy.eu/docs/page/2/ ')
#     checkout = Checkout(api=api)
#     data = {
#         "currency": "UAH",
#         "amount": 12000
#     }
#     url = checkout.url(data).get('checkout_url')
#     context = {
#         'title':'Store',
#         'url': url
#     }
#     return render(request,'store/add_to_cart.html',context)




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




