
from django.contrib import admin
from django.urls import path, include

from userAuth import views

from django.conf import settings
from django.conf.urls import handler404
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('auth/', include('userAuth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('finance/', include('finance.urls')),
    path('deals/', include('deals.urls')),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'userAuth.views.notFound'


