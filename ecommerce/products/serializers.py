from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    product_id = serializers.CharField(read_only=True)
    product_name = serializers.CharField()
    category = serializers.CharField()
    rating = serializers.FloatField()
    rating_count = serializers.IntegerField()
    discounted_price = serializers.FloatField()
    actual_price = serializers.FloatField()
    discount_percentage = serializers.CharField()
    about_product = serializers.CharField()
    user_id = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
    user_name = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
    review_id = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
    review_title = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
    review_content = serializers.ListField(
        child=serializers.CharField(), allow_empty=True
    )
    img_link = serializers.URLField()
    product_link = serializers.URLField()
