"""PRAI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from praiapp.views import signup,login,userlogin,logout,home,sentiment,demo,wordpress,dashboard,post,delete,analyse,delcomment
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/',signup),
    url(r'^message/',signup),
    url(r'^login/',login),
    url(r'^userlogin/',userlogin),
    url(r'^logout/',logout),
    url(r'^home/',home),
    url(r'^sentiment/',sentiment),
    url(r'^demo/',demo),
    url(r'^wordpress/',wordpress),
    url(r'^dashboard/',dashboard),
    url(r'^post/',post),
    url(r'^delete/',delete),
    url(r'^analyse/(?P<ids>\d+)/$',analyse),
    url(r'^delete/comment/',delete),



]