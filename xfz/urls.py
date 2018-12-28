"""xfz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from apps.news import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index,name='index'),
    path('search/',views.search,name='search'),
    path('cms/',include('apps.cms.urls',namespace='cms')),
    path('account/',include('apps.xfzauth.urls',namespace='xfzauth')),
    path('news/',include('apps.news.urls',namespace='news')),
    path('course/', include('apps.course.urls', namespace='course')),
    path('payinfo/', include('apps.payinfo.urls', namespace='payinfo')),
    path('ueditor',include('apps.ueditor.urls', namespace='ueditor')),

]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
#如果是调试模式，打开toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls))
    )

