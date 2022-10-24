from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from drf_writable_nested import WritableNestedModelSerializer

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'username')
        
    def create(self, validated_data):
        user = User(username=validated_data['username'].lower())
        user.email = validated_data['email']
        user.is_active = True
        user.is_staff=False
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSignupSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    user_fk = UserSignUpSerializer()
    profile_id = serializers.SerializerMethodField()
    class Meta(object):
        model = Profile
        fields = ('profile_id','user_fk', 'phone_no', 'user_type', 'slug')

    def get_profile_id(self, obj):
        return obj.id



class ProfileLoginSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    class Meta(object):
        model = Profile
        fields = ('id', 'phone_no', 'slug', 'user_type')

    def get_user_type(self,obj):
        if obj.user_type==1:
            return "Admin"
        elif obj.user_type==2:
            return "Editor"
        elif obj.user_type==3:
            return "Customer"
        else:
            return "No User Type"



class UserLoginSerializer(serializers.ModelSerializer):

    '''
        This Serializer is for User Details
    '''
    profile = ProfileLoginSerializer()
    class Meta(object):
        model = User
        fields = ('id','first_name', 'last_name', 'email', 'username', 'profile', 'date_joined', 'is_active', 'last_login')
        