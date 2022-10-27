from django.urls import path
from .views import *

urlpatterns = [
    path('list/', ViolationsListView.as_view()),
    path('delete-all/', ViolationsDeleteAllView.as_view()),
    path('delete/', ViolationsDeleteView.as_view()),
    path('create/', ViolationsCreateUpdateView.as_view()),
    path('update/<int:pk>/', ViolationsCreateUpdateView.as_view()),




]
