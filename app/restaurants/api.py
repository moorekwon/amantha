from rest_framework import generics, permissions
from rest_framework.authentication import BasicAuthentication

from restaurants.models import Restaurant, RestaurantCategory, RestaurantLocation, RestaurantImages
from restaurants.serializers import RestaurantSerializer, RestaurantCategorySerializer, RestaurantLocationSerializer, \
    RestaurantImagesSerializer, RestaurantCreateSerializer, RestaurantCategoryCreateSerializer


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
        name = self.request.data['restaurant_name']
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
