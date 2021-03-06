from django.urls import path

from . import apis
urlpatterns = [
    path('restaurants/', apis.RestaurantListCreateAPIView.as_view()),
    path('restaurants/category/', apis.RestaurantCategoryListCreateAPIView.as_view()),
    path('restaurants/category/<category_name>/', apis.RestaurantCategoryTypeList.as_view()),

]