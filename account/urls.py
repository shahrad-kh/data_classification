from django.urls import path
from . import views


urlpatterns = [
    path('CreateOperator/', views.CreateOperatorAPIView.as_view(), name='create-operator'),
    path('Login/', views.LoginAPIView.as_view(), name='login'),
    path('Logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('UpdateOperatorAvailableDatasets/<int:pk>/', views.UpdateOperatorAvailableDatasetsAPIView.as_view(), name='update-available-datasets'),
]
