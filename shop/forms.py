from django import forms

class OrderForm(forms.Form):
    delivery_method = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=([('mkad', 'Доставка в пределах МКАД'), ('r_post', 'Почтой России'), ('tk', 'Транспортной компанией')]))

    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    city = forms.CharField(max_length=50, required=False)
    delivery_address = forms.CharField(max_length=200, required=True,)
    delivery_company = forms.CharField(max_length=100, required=False)
    pay_type = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=([('cash', 'Наличными курьеру'), ('card', 'Переводом на карту')]))

    order_comments = forms.CharField(widget=forms.Textarea, max_length=500, required=False)

    #Добавляем атрибуты для всех полей
    delivery_method.widget.attrs.update({'id': 'delivery_type'})
    first_name.widget.attrs.update({'id': 'first_name', 'placeholder': 'Иван'})
    last_name.widget.attrs.update({'id': 'last_name', 'placeholder': 'Иванов'})
    phone.widget.attrs.update({'id': 'phone', 'placeholder': '8(926)000-00-00'})
    email.widget.attrs.update({'id': 'email', 'placeholder': 'your_mail@mail.ru'})
    city.widget.attrs.update({'id': 'city', 'placeholder': 'Санкт-Петербург'})
    delivery_address.widget.attrs.update({'id': 'delivery_address', 'placeholder': 'ул. Ленина, дом 101, кв. 17'})
    delivery_company.widget.attrs.update({'id': 'delivery_company', 'placeholder': 'Деловые Линии'})
    pay_type.widget.attrs.update({'id': 'pay_type'})
    order_comments.widget.attrs.update({'id': 'order_comments', 'rows': '6', 'cols': '5', 'placeholder': 'Ваши комментарии и пожелания'})


    #Меняем лейблы для всех полей
    delivery_method.label = 'Способ доставки'
    first_name.label = 'Ваше имя'
    last_name.label = 'Ваша фамилия'
    phone.label = 'Контактный телефон'
    email.label = 'Электронная почта'
    city.label = 'Город доставки'
    delivery_address.label = 'Адрес доставки'
    delivery_company.label = 'Транспортная компания'
    pay_type.label = 'Способ оплаты'
    order_comments.label = 'Комментарий к заказу'

    def clean_city(self):
        city = self.cleaned_data['city']
        if not city:
            city = 'Москва'
        return city

    def clean_delivery_company(self):
        delivery_company = self.cleaned_data['delivery_company']
        if not delivery_company:
            delivery_company = 'Не указано'
        return delivery_company

    def clean_order_comments(self):
        order_commennts = self.cleaned_data['order_comments']
        if not order_commennts:
            order_commennts = 'Не указано'
        return order_commennts