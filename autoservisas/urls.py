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
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
]