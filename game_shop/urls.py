from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include('accounts.urls')),
                  path('api/v1/shop/', include('product.urls')),
                  path('api/v1/checkout/', include('checkout.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
