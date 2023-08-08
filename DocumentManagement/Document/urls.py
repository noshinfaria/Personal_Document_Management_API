from django.urls import path
#now import the views.py file into this code
from . import views
from .views import Shared_user, PostEditView, document_list


urlpatterns=[
    path('upload/', views.document_upload, name="upload"),
    path('list/', document_list.as_view(), name="list"),
    path('postedit/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    path('delete/<int:pk>/', views.delete_file, name="delete-file"),
    path('shareduser/<int:pk>/', Shared_user.as_view(), name='shared-user'),
    path('sharedfile/', views.shared_file, name="shared-file"),
]