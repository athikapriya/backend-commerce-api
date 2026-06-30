from rest_framework import serializers

from .models import Category


# =============== Start childCategorySerializer section ===============
class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            "name",
            "slug",
        )
# =============== End childCategorySerializer seciton ===============


# =============== Start Category Serializer section ===============
class CategorySerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id', 
            "name",
            "slug",
            "children",
        )
# =============== End Category Serializer seciton ===============