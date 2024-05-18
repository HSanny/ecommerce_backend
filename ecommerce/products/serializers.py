from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    main_category = serializers.CharField()
    sub_category = serializers.CharField()
    ratings = serializers.FloatField()
    discount_price = serializers.FloatField()
    actual_price = serializers.FloatField()