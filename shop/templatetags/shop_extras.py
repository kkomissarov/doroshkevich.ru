from django import template
from ..models import Category, Cart, Infopage
register = template.Library()


#Главное меню
@register.inclusion_tag('shop/main_menu.html')
def main_menu():
    main_categories = Category.objects.filter(level=0)
    return {'main_categories': main_categories}


#Главное меню
@register.inclusion_tag('shop/top_menu.html')
def top_menu():
    infopages = Infopage.objects.filter(show_in_menu=True)
    return {'infopages': infopages}


#Виджет корзины
@register.simple_tag(takes_context=True)
def cart_qty(context):
    try:
        cart = Cart.objects.get(id=context.request.session['cart_id'])
        cart_qty = sum([item.qty for item in cart.items.all()])
    except:
        cart_qty = 0
    return cart_qty

