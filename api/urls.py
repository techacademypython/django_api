from django.urls import path
from api.views import main_index, api_main_news, api_news_update

urlpatterns = [
    path('', main_index, name="main_index"),
    path('news/', api_main_news, name="api_main_news"),
    path('news/<int:id>', api_news_update, name="api_news_update"),
]
