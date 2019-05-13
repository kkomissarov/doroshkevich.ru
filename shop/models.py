from django.db import models
from django.urls import reverse
from .utils import get_level, gen_slug, get_sort_name


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории')

    slug = models.SlugField(
        max_length=200,
        blank=True,
        verbose_name='Символльный код',
        unique=True
    )

    seo_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='SEO Title'
    )

    seo_description = models.CharField(
        max_length=400,
        blank=True,
        verbose_name='SEO Description'
    )

    top_text = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name='Верхний текст'
    )

    bottom_text = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name='Нижний текст'
    )

    activate = models.BooleanField(
        default=True,
        verbose_name='Категория включена'
    )

    parent = models.ForeignKey(
        'self',
        verbose_name='Родительское категория',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.DO_NOTHING)

    level = models.PositiveIntegerField(
        default=0)

    sort_name = models.CharField(max_length=400, blank=True)


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.sort_name

    def get_absolute_url(self):
        return reverse('category_view', kwargs={'slug': self.slug})

    #Получить родителей и ссылки на них для хлебных крошек
    def get_all_parents(self):
        if self.level > 0:
            all_parents = []
            obj = self.parent
            for i in range(0, self.level):
                name = obj.name
                link = obj.get_absolute_url()
                all_parents.append([name, link])
                if i < self.level:
                    obj = obj.parent
            return all_parents
        else:
            return None


    def save(self, *args, **kwargs):
        #сгенирировать слаг, если он пустой или категория еще не создана
        if not self.slug:
            self.slug = gen_slug(self.name)

        #посчитать уровень вложенности
        self.level = get_level(self)

        #сгенерировать имя для сортировки, включающее все родительские категории
        self.sort_name = get_sort_name(self)
        super().save(*args, **kwargs)

        #Пересохранить все дочерние категории, чтобы перегенирировать их sort_name и пересчитать уровень вложенности
        if self.children.count() > 0:
            childs = self.children.all()

            for child in childs:
                child.save()






class Product(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название товара')

    slug = models.SlugField(
        max_length=200,
        blank=True,
        verbose_name='Символьный код',
        unique=True,
        help_text='Это адрес страницы. Если оставить поле пустым, он сгенерируется автоматически.')

    price = models.PositiveIntegerField(
        blank=False,
        verbose_name='Цена',
        help_text='Целое число в рублях. Без копеек.')

    category = models.ForeignKey(
        Category,
        verbose_name='Вложенность по хлебным крошкам',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='main_products',
        help_text='В эту категорию будет вложен товар по хлебным крошкам'
        )

    secondary_categories = models.ManyToManyField(
        Category,
        verbose_name='Родительские категории',
        related_name='secondary_products',
        help_text='Товар будет выводиться в выбранных категориях.',
        blank=True)


    seo_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='SEO Title',
        help_text='Это поле будет заголовком страницы в браузере. Очень важное поле для поисковых систем. Заполнять нужно с умом',)

    seo_description = models.CharField(
        max_length=400,
        blank=True,
        verbose_name='SEO Description',
        help_text='Мета-описание. Пользователи его не видят, но поисковикам важно, чтобы оно было заполнено. Пустым оставлять можно, но не рекомендуется.')

    text_description = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name='Описание',
        help_text='''
            Текстовое описание поддерживает html-тэги. Нужно использовать их, если хочется отформатировать текст.<br> 
            Небольшая справка по тэгам:<br><br>
            &lt;p&gt;В такой текст заключается абзац&lt;/p&gt; <br><br>
            &lt;strong&gt;В таком тэге текст будет жирным&lt;/strong&gt; <br><br>
            &lt;br&gt; - такой одинарный тэг используется для переноса строки
        ''')

    active = models.BooleanField(
        default=True,
        verbose_name='Товар включен',
        help_text='Отключенные товары исчезают с сайта')

    status = models.CharField(
        choices=(('В наличии', 'В наличии'), ('Под заказ', 'Под заказ')),
        verbose_name='Статус',
        max_length=50,
        default='in_stock')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('product_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)




class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    image = models.ImageField(
        upload_to='product-photo/',
        blank=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'




class Infopage(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название страницы')

    slug = models.SlugField(
        max_length=200,
        blank=True,
        verbose_name='Символльный код',
        unique=True
    )

    content = models.TextField(
        max_length=3000,
        verbose_name='Содержание'
    )

    show_in_menu = models.BooleanField(
        verbose_name='Выводить в меню',
        default=True
    )

    seo_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='SEO Title',
        help_text='Это поле будет заголовком страницы в браузере. Очень важное поле для поисковых систем. Заполнять нужно с умом',)

    seo_description = models.CharField(
        max_length=400,
        blank=True,
        verbose_name='SEO Description',
        help_text='Мета-описание. Пользователи его не видят, но поисковикам важно, чтобы оно было заполнено. Пустым оставлять можно, но не рекомендуется.')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('infopage_view', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        #сгенирировать слаг, если он пустой или категория еще не создана
        if not self.slug:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Информационная страница'
        verbose_name_plural = 'Информационные страницы'



class Cart(models.Model):
    total = models.IntegerField(
        default=0
    )

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.total
        self.total = total
        self.save()


    def to_json(self):
        items_list = []

        if self.items.count() > 0:
            for item in self.items.all():
                json_item = {
                    'id': item.product.id,
                    'name': item.product.name,
                    'url': item.product.get_absolute_url(),
                    'img': item.product.images.first().image.url,
                    'qty': item.qty,
                    'total': item.total}
                items_list.append(json_item)

        cart_json = {
            'items': items_list,
            'count': sum([item.qty for item in self.items.all()]),
            'total': self.total
        }


        return cart_json

    def add_item(self, product_id):
        product = Product.objects.get(id=product_id)

        try:
            item = self.items.get(product=product)
            item.qty += 1
            item.save()

        except:
            item = CartItem.objects.create(product=product, cart=self)
            item.save()

        self.get_total()


    def remove_item(self, product_id):
        product = Product.objects.get(id=product_id)
        item = self.items.get(product=product)
        item.delete()

        self.get_total()

    def change_item_qty(self, product_id, new_qty):
        product = Product.objects.get(id=product_id)
        item = self.items.get(product=product)
        item.qty = new_qty
        item.save()
        self.get_total()

    def __str__(self):
        return 'Корзина №{} на общую сумму {} рублей'.format(self.id, self.total)





class CartItem(models.Model):
    product = models.ForeignKey(
        'Product',
        related_name='cart_item',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    cart = models.ForeignKey(
        'Cart',
        related_name='items',
        on_delete=models.CASCADE)

    name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Название товара',
        default='-')

    price = models.PositiveIntegerField(
        blank=True,
        verbose_name='Цена',
        default=0)

    qty = models.PositiveIntegerField(default=1)

    total = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.name = self.product.name
        self.total = self.product.price * self.qty
        super().save(*args, **kwargs)


    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name='Товар в корзине'
        verbose_name_plural='Товары в корзине'



class Order(models.Model):
    delivery_method = models.CharField(
        max_length=20,
        choices=(('mkad', 'Доставка в пределах МКАД'), ('r_post', 'Почтой России'), ('tk', 'Транспортной компанией')),
        verbose_name='Способ доставки')

    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя')

    last_name = models.CharField(
        max_length=50,
        default='Не указано',
        verbose_name='Фамилия')

    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон')

    email = models.EmailField(
        verbose_name='E-mail')

    city = models.CharField(
        max_length=50,
        default='Москва',
        verbose_name='Город доставки')

    delivery_address = models.CharField(
        max_length=200,
        verbose_name='Адрес доставки')

    delivery_company = models.CharField(
        max_length=100,
        default='Не указано',
        verbose_name='Транспортная компания')

    pay_type = models.CharField(
        max_length=50,
        choices=(('cash', 'Наличными курьеру'), ('card', 'Переводом на карту')),
        verbose_name='Способ оплаты')

    order_comments = models.TextField(
        max_length=500,
        verbose_name='Комментарий к заказу')

    cart = models.ForeignKey(
        'Cart',
        related_name='order',
        on_delete=models.CASCADE)

    date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='Дата заказа')

    def __str__(self):
        return 'Заказ №{} на сумму {} рублей'.format(self.id, self.cart.total)

    class Meta:
        verbose_name='Заказ'
        verbose_name_plural='Заказы'
