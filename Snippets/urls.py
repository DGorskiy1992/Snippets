"""Snippets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from MainApp import views

urlpatterns = [
                  path('', views.index_page, name="index"),
                  path('snippets/add', views.add_snippet_page, name="snippets_add"),
                  path('snippets/delete/<int:id>', views.snippet_delete, name="snippet_delete"),
                  path('snippets/edit/<int:id>', views.snippet_edit, name="snippet_edit"),
                  path('snippets/list', views.snippets_page, name="snippets_list"),
                  path('snippets/<int:id>', views.snippet_page, name="snippet_page"),
                  path('snippets/search', views.snippets_search, name="snippet_search"),
                  path('login', views.login_page, name='login'),
                  path('logout', views.logout, name='logout'),
                  path('registration', views.register, name='registration'),
                  path('my_snippets', views.my_snips, name='my_snips'),
                  path('comment/add', views.comment_add, name="comment_add"),
                  path('admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
