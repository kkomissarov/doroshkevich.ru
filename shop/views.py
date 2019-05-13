from django.shortcuts import HttpResponse, redirect, render
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Product, Category, Cart, CartItem, Order, Infopage
from .forms import OrderForm
from .utils import order_mail


def get_or_create_cart(request):
    try:
        cart = Cart.objects.get(id=request.session['cart_id'])
    except:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart


class ProductDetailView(DetailView):
    template_name = 'shop/product.html'
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        cart_items = CartItem.objects.filter(cart=cart)
        context['products_in_cart_ids'] = [item.product.id for item in cart_items]
        return context


class CategoryListView(ListView):
    template_name = 'shop/category.html'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(secondary_categories__slug=self.kwargs.get('slug'), active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs.get('slug'))
        cart = get_or_create_cart(self.request)


        #проверяем надо ли добавить на эту страницу правило noindex
        if 'page' in self.request.GET:
            context['is_noindex'] = True
        else:
            context['is_noindex'] = False

        try:
            cart_items = CartItem.objects.filter(cart=cart)
            context['products_in_cart_ids'] = [item.product.id for item in cart_items]
        except:
            context['products_in_cart_ids'] = []

        return context


class MainPageView(View):
    def get(self, request):
        return render(request, 'shop/mainpage.html')




class CartView(View):
    def get(self, request):
        cart = get_or_create_cart(request)
        order_form = OrderForm()
        context = {
            'cart': cart,
            'order_form': order_form,
        }
        return render(request, 'shop/cart.html', context=context)

    def post(self, request):
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_data = order_form.cleaned_data
            cart = Cart.objects.get(id=request.session['cart_id'])

            if cart.items.count() > 0: #Проверяем, что корзина не пустая
                order_data.update({'cart': cart})
                new_order = Order.objects.create(**order_data)
                new_order.save()
                order_mail(new_order) #Отправляем уведомления о новом заказе
                request.session['cart_id'] = None
                context ={'order': new_order}
                return render(request, 'shop/thank-you-page.html', context=context)
            else:
                context = {
                    'error': '''Невозможно оформить заказ, так как в Вашу корзину не добавлено ни одного товара. 
                                Возможно, это произошло, потому что Вы уже оформили заказ и пытаетесь сделать это 
                                повторно. Пожалуйста, проверьте своею электронную почту, возможно, мы уже выслали
                                Вам информацию о Вашем заказе.'''
                }
                return render(request, 'shop/error.html', context=context)

        else:
            context = {
                'error': '''К сожалению, мы не смогли оформить Ваш заказ, так как на сайте произошла неизвестная 
                            ошибка. Если Вы видите это сообщение, пожалуйста, напишите нам на электронную почту
                            при каких обстоятельствах произошла эта ошибка, и мы обязательно во всем разберемся.'''
            }
            return render(request, 'shop/error.html', context=context)


class InfopageView(DetailView):
    template_name = 'shop/infopage.html'
    model = Infopage




class Catalog(ListView):
    template_name = 'shop/catalog.html'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)

        try:
            cart_items = CartItem.objects.filter(cart=cart)
            context['products_in_cart_ids'] = [item.product.id for item in cart_items]
        except:
            context['products_in_cart_ids'] = []

        #проверяем надо ли добавить на эту страницу правило noindex
        if 'page' in self.request.GET:
            context['is_noindex'] = True
        else:
            context['is_noindex'] = False

        return context




#Возврощает текущее содержимое корзины в json, предварительно выполнив необходимые изменения
def get_json_cart(request):
    cart = Cart.objects.get(id=request.session['cart_id'])
    action = request.GET.get('action')
    product_id = request.GET.get('product_id')

    if action == 'delete':
        cart.remove_item(product_id)
    elif action == 'add':
        cart.add_item(product_id)
    elif action == 'change-qty':
        new_qty = request.GET.get('qty')
        cart.change_item_qty(product_id, int(new_qty))
    elif action == 'add-with-qty':
        qty = int(request.GET.get('qty'))
        product = Product.objects.get(id=int(product_id))
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.qty += qty
            cart_item.save()
            cart.get_total()
        except:
            cart_item = CartItem.objects.create(cart=cart, qty=qty, product=product)
            cart_item.save()
            cart.get_total()

    return JsonResponse(cart.to_json())


class SitemapView(View):
    def get(self, request):
        


        context={

        }

        return render(request, 'shop/sitemap.html', context=context)





