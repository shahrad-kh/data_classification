from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('dataset-list-create/', views.DatasetListCreateAPIView.as_view(), name="dataset_list_create"),
    path('dataset-detail/<int:pk>/', views.DatasetRetrieveAPIView().as_view(), name="dataset_detail"),
    path('dataset-update/<int:pk>/', views.DatasetUpdateAPIView.as_view(), name="dataset_update"),
    path('dataset-delete/<int:pk>/', views.DatasetDestroyAPIView.as_view(), name="dataset_delete"),
    path('dataset-count-text-by-tag/<int:pk>/', views.CountTextByTagAPIView.as_view(), name="dataset_count_text_by_tag"),
    path('tag-list-create/', views.TagListCreateAPIView.as_view(), name="tag_list_create"),
    path('tag-detail/<int:pk>/', views.TagRetrieveAPIView.as_view(), name="tag_detail"),
    path('tag-update/<int:pk>/', views.TagUpdateAPIView.as_view(), name="tag_update"),
    path('tag-delete/<int:pk>/', views.TagDestroyAPIView.as_view(), name="tag_delete"),
    path('text-list-create/', views.TextListCreateAPIView.as_view(), name="text_list_create"),
    path('text-detail/<int:pk>/', views.TextRetrieveAPIView().as_view(), name="text_detail"),
    path('text-update/<int:pk>/', views.TextUpdateAPIView.as_view(), name="text_update"),
    path('text-delete/<int:pk>/', views.TextDestroyAPIView.as_view(), name="text_delete"),
]
