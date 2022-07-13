from rest_framework import serializers 
from WebCaosNews.models import UserProfile


class PerdiodistasSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["first_name","last_name","profile_pic","bio"]