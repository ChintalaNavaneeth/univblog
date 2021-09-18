from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('post/<int:id>/<slug:slug>', post, name='post'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('view_all/<str:query>', view_all, name='view_all'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('newblog/<int:id>', newblog, name='newblog'),
    path('delete/<int:id>', deleteblog, name='deleteblog'),
    path('edit/<int:id>', editblog, name='editblog'),
    path('pagenotfound/', pagenotfound, name='pagenotfound'),



] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)

handler404 = 'blog.views.pagenotfound'
