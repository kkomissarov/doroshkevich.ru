from django.contrib import admin
from .models import Product, ProductImage, Category, CartItem, Order, Infopage
from django.utils.html import format_html


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 4

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]
    list_display = ('name', 'price')
    search_fields = ('name',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'price', 'slug', 'text_description', 'active', 'status'),
        }),

        ('Связи', {
            'fields': ('category', 'secondary_categories', ),
        }),

        ('SEO', {
            'fields': ('seo_title', 'seo_description',),
        }),
    )
    filter_horizontal = ('secondary_categories',)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    exclude = ('level', 'sort_name',)
    ordering = ('sort_name', )
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'activate', 'parent'),
        }),

        ('SEO', {
            'fields': ('seo_title', 'seo_description', 'top_text', 'bottom_text'),
        }),

    )



class OrderAdmin(admin.ModelAdmin):

    readonly_fields = ('order__number', 'date', 'cart__total', 'delivery_method', 'first_name', 'last_name', 'phone', 'email', 'city',
        'delivery_address', 'delivery_company', 'pay_type', 'order_comments', 'cart__products')

    list_display = ('order__number', 'date', 'first_name', 'city', 'delivery_address', )

    exclude = ('cart', )


    fieldsets = (
        ('Основная информация', {
            'fields': ('order__number','date', 'cart__products', 'cart__total', 'order_comments'),
        }),

        ('Информация о доставке', {
            'fields': ('delivery_method', 'city', 'delivery_address', 'delivery_company', 'pay_type'),
        }),

        ('Информация о клиенте', {
            'fields': ('first_name', 'last_name', 'phone', 'email', ),
        }),

    )

    #Общая сумма заказа
    def cart__total(self, obj):
        return str(obj.cart.total) + ' рублей'
    cart__total.short_description = 'Сумма заказа'


    #Номер заказа
    def order__number(self, obj):
        return obj.id
    order__number.short_description = 'Номер заказа'

    #Таблица с товарами в заказе
    def cart__products(self, obj):
        cart_content = obj.cart.items.all()

        result = ['<tr><th>Название</th> <th>Количество</th> <th>Цена за шт.</th></tr>']
        for item in cart_content:
            try:
                result.append('<tr><td><a href="{}" target="_blank">{}</a></td> <td> {} шт</td>  <td>{} рублей</td></tr>'.format(
                    item.product.get_absolute_url(),
                    item.name,
                    item.qty,
                    item.price))
            except:
                result.append('<tr><td>{} (недоступен)</td><td> {} шт</td><td>{} рублей</tr></td>'.format(
                    item.name,
                    item.qty,
                    item.price
                ))


        return format_html('<table>' + ''.join(result) + '</table>')
    cart__products.short_description = 'Товары в заказе'



class InfopageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'content', 'show_in_menu')
        }),


        ('SEO', {
            'fields': ('seo_title', 'seo_description'),
        }),

    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Infopage, InfopageAdmin)
