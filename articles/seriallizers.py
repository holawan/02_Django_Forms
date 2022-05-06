from dataclasses import fields
from rest_framework import serializers

from .models import Article

class ArticleSeriallizer(serializers.ModelSerializer) :

    class Meta :
        model = Article
        fields = '__all__'