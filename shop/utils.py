from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string

def get_level(category):
    if category.parent==None:
        return 0
    else:
        return category.parent.level + 1


#Генерация слага по умолчанию
def gen_slug(name):
    slug_name = slugify(name, allow_unicode=True)

    ciryllic = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
                'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

    translite = ['a', 'b', 'v', 'g', 'd', 'e', 'e', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p',
                'r', 's', 't', 'u', 'f', 'h', 'c', 'ch', 'sh', 'sh', '', 'y', '', 'e', 'yu', 'ya']

    print(ciryllic[1])

    for elem in range(0, len(ciryllic)):
        slug_name = slug_name.replace(ciryllic[elem], translite[elem])

    return slug_name


#Получить имя со вложенностью (для упорядоченного вывода в админке)
def get_sort_name(category):
    if category.level > 0:
        parents = []
        obj = category.parent
        for i in range(0, category.level):
            parents.append(obj.name)
            if i < category.level:
                obj = obj.parent
        sort_name = str()
        for parent in reversed(parents):
            sort_name += parent + ' > '

        sort_name += category.name
        return sort_name

    else:
        return category.name



#Уведомительные письма при оформлении заказа
def order_mail(order):

    #Уведомление администратору
    def admin_order_notification():
        msg_from = 'info@doroshkevich.ru'
        msg_to = ['komiccarov@gmail.com', 'nadezhda.d@hotmail.com']
        msg_title = 'Новый заказ на сайте!'

        context = {
            'order': order
        }

        msg_txt = render_to_string('shop/email/new_order.txt', context)
        msg_html = render_to_string('shop/email/new_order.html', context)

        send_mail(msg_title, msg_txt, msg_from, msg_to, html_message=msg_html)

    #Уведомление клиенту
    def client_order_notification():
        msg_from = 'info@doroshkevich.ru'
        msg_to = [order.email]
        msg_title = 'Ваш заказ на doroshkevich.ru'

        context = {
            'order': order
        }

        msg_txt = render_to_string('shop/email/client_order_notification.txt', context)
        msg_html = render_to_string('shop/email/client_order_notification.html', context)

        send_mail(msg_title, msg_txt, msg_from, msg_to, html_message=msg_html)

    admin_order_notification()
    client_order_notification()
