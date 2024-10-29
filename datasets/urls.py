from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    
    # Create instances
    path('CreateDataset/', views.CreateDatasetAPIView.as_view(), name="create_dataset"),
    path('CreateTagForDatasetByDatasetID/<int:pk>/', views.CreateTagForDatasetByDatasetIDAPIView.as_view(), name="create_tag"),
    path('CreateTextForDatasetByDatasetID/<int:pk>/', views.CreateTextForDatasetByDatasetIDAPIView.as_view(), name="create_text"),
    
    # List of instances 
    path('GetListOfDatasets/', views.GetListOfDatasetsAPIView.as_view(), name="list_of_datasets"),
    path('GetListOfTagsOfDatasetByDatasetID/<int:pk>/', views.GetListOfTagsOfDatasetByDatasetIDAPIView.as_view(), name="list_of_tags"),
    path('GetListOfTextsOfDatasetByDatasetID/<int:pk>/', views.GetListOfTextsOfDatasetByDatasetIDAPIView.as_view(), name="list_of_texts"),

    # Details of instances by id
    path('GetDetailOfDatasetByID/<int:pk>/', views.GetDetailOfDatasetByIDAPIView().as_view(), name="details_of_dataset_by_id"),
    path('GetDetailOfTagByID/<int:pk>/', views.GetDetailOfTagByIDAPIView.as_view(), name="details_of_tag_by_id"),
    path('GetDetailOfTextByID/<int:pk>/', views.GetDetailOfTextByIDAPIView().as_view(), name="details_of_text_by_id"),

    # Update instances by id
    path('UpdateDatasetByID/<int:pk>/', views.UpdateDatasetByIDAPIView.as_view(), name="update_dataset_by_id"),
    path('UpdateTagByID/<int:pk>/', views.TagUpdateAPIView.as_view(), name="update_tag_by_id"),
    path('UpdateTextByID/<int:pk>/', views.TextUpdateAPIView.as_view(), name="update_text_by_id"),

    # Delete instances by id
    path('DeleteDatasetByID/<int:pk>/', views.DeleteDatasetByIDAPIView.as_view(), name="delete_dataset"),
    path('DeleteTagByID/<int:pk>/', views.TagDestroyAPIView.as_view(), name="delete_tag"),
    path('DeleteTextByID/<int:pk>/', views.TextDestroyAPIView.as_view(), name="delete_text"),

    # Count number of Text labeld with unique tag by tag id
    path('CountNumberOfTextLabeldByTagID/<int:pk>/', views.CountTextByTagAPIView.as_view(), name="dataset_count_text_by_tag"),
    
    # full text search within text
    path('FullTextSearchWithinText/<str:dataset_name>/<slug:search_string>/', views.TextSearchAPIView.as_view(), name='full_tex_search'),
]
