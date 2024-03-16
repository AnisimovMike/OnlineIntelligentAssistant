from django.urls import path, re_path
from WebSite import views

urlpatterns = [
    path('', views.index),
    path('about', views.about),
    path('gallery/<int:sheet_id>', views.gallery),
    path('statistics', views.statistics),
    path('articles/<int:article_id>', views.articles),
    path('my_routs', views.my_routs),
    path('cur_route/<int:route_id>', views.cur_route),
    path('recommendations', views.recommendations),
    path('routing/<int:route_id>', views.routing),
    path('routing', views.choose_route),
    path('send_mes', views.send_mes),
    path('new_route', views.new_route),
    path('create_route/<str:city>', views.create_route),
    path('patch_route/<int:route_id>', views.patch_route),
    path('login', views.user_login),
    path('registration', views.registration),
    re_path('^.', views.index),
]
