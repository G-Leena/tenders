from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.userhome),
    path('viewtenders/', views.viewtenders),
    path('viewsubcat/', views.viewsubcat),
    path('viewsearchtenders/', views.viewsearchtenders),
    path('funds/', views.funds),
    path('payment/',views.payment),
    path('success/',views.success),
    path('cancel/',views.cancel),
    path('viewfunds/',views.viewfunds),
    path('cpuser/',views.cpuser),
    path('epuser/',views.epuser),
]
