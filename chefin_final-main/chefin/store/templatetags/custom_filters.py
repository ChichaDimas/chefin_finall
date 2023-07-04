from django import template

register = template.Library()

@register.filter
def mul_price(quantity, price):

    print(price)
    print(quantity)
    try:
        if quantity and price:
            return int(quantity) * int(price)
        else:
            return ''
    except (ValueError, TypeError):
        return ''




@register.filter
def dictuniq(value, key):
    return {d[key]: d for d in value}.values()