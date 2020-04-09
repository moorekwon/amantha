from urllib.parse import urlparse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.authentication import BasicAuthentication

from restaurants.models import Restaurant, RestaurantCategory, RestaurantLocation, RestaurantImages
from restaurants.serializers import RestaurantSerializer, RestaurantCategorySerializer, RestaurantLocationSerializer, \
    RestaurantImagesSerializer, RestaurantCreateSerializer, RestaurantCategoryCreateSerializer

from urllib import parse

class RestaurantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    authentication_classes = (BasicAuthentication,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RestaurantSerializer
        elif self.request.method == 'POST':
            return RestaurantCreateSerializer


class RestaurantRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    authentication_classes = (BasicAuthentication,)

    serializer_class = RestaurantSerializer


class RestaurantCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = RestaurantCategory.objects.all()
    authentication_classes = (BasicAuthentication,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RestaurantCategorySerializer
        elif self.request.method == 'POST':
            return RestaurantCategoryCreateSerializer

    def perform_create(self, serializer):
        name = self.request.data['restaurant']
        restaurant = Restaurant.objects.get(name=name)
        serializer.save(restaurant=restaurant)


class RestaurantCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantCategory.objects.all()
    serializer_class = RestaurantCategorySerializer


class RestaurantLocationListCreateAPIView(generics.ListCreateAPIView):
    queryset = RestaurantLocation.objects.all()
    serializer_class = RestaurantLocationSerializer


class RestaurantLocationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantLocation.objects.all()
    serializer_class = RestaurantLocationSerializer


class RestaurantImagesListCreateAPIView(generics.ListCreateAPIView):
    queryset = RestaurantImages.objects.all()
    serializer_class = RestaurantImagesSerializer


class RestaurantImagesRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantImages.objects.all()
    serializer_class = RestaurantImagesSerializer


class RestaurantCategoryTypeList(generics.ListAPIView):

    def get_queryset(self):

        category_name = urlparse(self.kwargs['category_name'])
        print(category_name)
        if category_name is not None:
            queryset = RestaurantCategory.objects.filter(category=category_name)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RestaurantCategorySerializer
