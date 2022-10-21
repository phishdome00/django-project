from django.urls import path
from .views import *

urlpatterns = [
    path('add/', AppCreateUpdateView.as_view()),
    path('list/', AppListView.as_view()),
    path('edit/<int:pk>/', AppCreateUpdateView.as_view()),
    path('remove/<int:pk>/', AppCreateUpdateView.as_view()),

]
