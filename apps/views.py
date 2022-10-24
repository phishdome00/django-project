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
        user=request.user
        data=request.data

        # set to mutable
        data._mutable = True

        data['user']=user.pk

        serializer = AppSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def patch(self, request, pk, format=None):
        data=request.data
        obj= App.objects.get(id=pk)
        serializer = AppSerializer(data=data, instance=obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        obj=App.objects.get(id=pk)
        obj.delete()
        return Response({"message":"App Data deleted Successfully !!!!"}, status=status.HTTP_200_OK)

class AppListView(APIView):

    def get(self,request,format=None):
        user=request.user
        queryset = App.objects.filter(user=user)
        serializer = AppListSerializer(queryset, many=True)
        return Response({"apps":serializer.data}, status=status.HTTP_200_OK)


