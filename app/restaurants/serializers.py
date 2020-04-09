from .models import Restaurant, RestaurantCategory, RestaurantLocation, RestaurantImages
from rest_framework import serializers


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'id',
            'name',
            'address1',
            'name_address1_unique',
            'address2',
            'point',
            'phone',
            'price_range',
            'parking',
            'opening_hours',
            'menu',
            'restaurant_type',
            'date_joined',
            'date_update',
        )


class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'name',
            'address1',
            'name_address1_unique',
            'address2',
            'point',
            'phone',
            'price_range',
            'parking',
            'opening_hours',
            'menu',
            'restaurant_type',
            'date_joined',
            'date_update',
        )

    def to_representation(self, instance):
        return RestaurantSerializer(instance).data


class RestaurantCategorySerializer(serializers.ModelSerializer):
    restaurants = RestaurantSerializer(many=True, read_only=True)
    class Meta:
        model = RestaurantCategory
        fields = (
            'id',
            'restaurant',
            'category',
            'thumbnail',
            'date_joined',
            'date_update',
            'restaurants',
        )


class RestaurantCategoryCreateSerializer(serializers.ModelSerializer):
    # restaurants = RestaurantSerializer(many=True, read_only=True)
    class Meta:
        model = RestaurantCategory
        fields = (
            'category',
            'thumbnail',
            'date_joined',
            'date_update',
        )


class RestaurantLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantLocation
        fields = (
            'id',
            'restaurant',
            'location',
            'date_joined',
            'date_update',
        )


class RestaurantLocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantLocation
        fields = (
            'restaurant',
            'location',
            'date_joined',
            'date_update',
        )


class RestaurantImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImages
        fields = (
            'id',
            'restaurant',
            'photo',
            'date_joined',
            'date_update',
        )


