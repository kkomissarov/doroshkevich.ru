from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from shop.sitemaps import ProductSitemap, CategorySitemap, InfopageSitemap



sitemaps = {
    'product_sitemap': ProductSitemap,
    'category_sitemap': CategorySitemap,
    'infopage_sitemap': InfopageSitemap,
}




urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('', include('shop.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


