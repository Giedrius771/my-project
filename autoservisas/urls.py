from django.urls import path
from . import views
from .views import CustomPasswordResetView

urlpatterns = [
    path('', views.index, name='index'),
    path('statistics/', views.statistics, name='statistics'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:pk>/', views.AutomobilisDetailView.as_view(), name='automobilis-detail'),
    path('uzsakymai/', views.UzsakymaiListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<int:pk>/', views.UzsakymasDetailView.as_view(), name='uzsakymas-detail'),
    path('search/', views.search, name='search'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password-reset'),
    path('myautomobiliai/', views.LoanedAutomobiliaiByUserListView.as_view(), name='my-borrowed'),
    path('myautomobiliai/<uuid:pk>', views.AutomobiliaiByUserDetailView.as_view(), name='my-automobiliai'),
    path('myautomobiliai/new', views.AutomobilisByUserCreateView.as_view(), name='my-borrowed-new'),
    path('myautomobiliai/<int:pk>/update', views.AutomobilisByUserUpdateView.as_view(), name='my-automobiliai-update'),
    path('myautomobiliai/<int:pk>/delete', views.AutomobilisByUserDeleteView.as_view(), name='my-automobiliai-delete'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
]