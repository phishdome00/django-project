from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User

from apps.models import App
from .serializers import AppSerializer,AppListSerializer


# Create your views here.


class AppCreateUpdateView(APIView):

    def post(self,request,format=None):

        user=request.user.is_superuser
        if user:
            data={}
            username=request.data.get('username', None)
            user_fk=User.objects.get(username=username).id
            data['user']=user_fk
            data['appname']=request.data.get('appname')
            data['appurl']=request.data.get('appurl')
            serializer = AppSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"permission error"}, status=status.HTTP_401_UNAUTHORIZED)
        
    def patch(self, request, pk, format=None):

        user=request.user.is_superuser
        if user:
            data={}
            username=request.data.get('username')
            if username:
                user_fk=User.objects.get(username=username).id
                data['user']=user_fk
            elif request.data.get('appname'):    
                data['appname']=request.data.get('appname')
            elif request.data.get('appurl'):
                data['appurl']=request.data.get('appurl')

            obj= App.objects.get(id=pk)
            serializer = AppSerializer(data=data, instance=obj, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"permission error"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        
        user=request.user.is_superuser
        if user:
            obj=App.objects.get(id=pk)
            obj.delete()
            return Response({"message":"App Data deleted Successfully !!!!"}, status=status.HTTP_200_OK)

class AppListView(APIView):

    def post(self,request,format=None):
        user=request.user.is_superuser
        if user:
            data={}
            username=request.data.get('username', None)
            user_fk=User.objects.get(username=username).id
            queryset = App.objects.filter(user=user_fk)
            serializer = AppListSerializer(queryset, many=True)
            return Response({"apps":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"permission error"}, status=status.HTTP_401_UNAUTHORIZED)

