from django.urls import path
from .views import *

urlpatterns = [
    path('shotlist/', ShotListView.as_view(), name='shotlist-list'),
    path('shotlist/<int:pk>/', ShotListDetailView.as_view(), name='shotlist-detail'),
    path('consentform/', ConsentFormView.as_view(), name='consentform-list'),
    path('consentform/<int:pk>/', ConsentFormDetailView.as_view(), name='consentform-detail'),
    path('project/', ProjectView.as_view(), name='project-list'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]
