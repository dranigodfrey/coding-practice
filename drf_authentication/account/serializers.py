from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

# get the user account model 
User = get_user_model()

class UserAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'user_role', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name',]