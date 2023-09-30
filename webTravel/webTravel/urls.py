
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('imagine-and-travel/',include('AppTravel.urls'))
]
urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
handler404 = 'AppTravel.views.error_404'

admin.site.site_url = '/imagine-and-travel/'