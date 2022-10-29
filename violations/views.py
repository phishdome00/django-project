from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Violation
from .serializers import ViolationListSerializer,ViolationCreateUpdateSerializer
from django.db.models import Q
import datetime

# Create your views here.

class ViolationsListView(APIView):

    def post(self,request,format=None):

        data=request.data
        from_date=data.get('from_date')
        to_date=data.get('to_date')
        app=data.get('app')

    
        start_time = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        end_time = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
  
        queryset = Violation.objects.filter(app=app)

        data=[]
        for i in queryset:
            if type(i.date)==str:
                i.date = datetime.datetime.strptime(i.date, '%Y-%m-%d').date()
            if i.date>=start_time and i.date<=end_time:
                data.append(i)


        serializer = ViolationListSerializer(data, many=True)
        return Response({"violations":serializer.data}, status=status.HTTP_200_OK)

class ViolationsCreateUpdateView(APIView):

    def post(self,request,format=None):

        data=request.data
        serializer = ViolationCreateUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self,request,pk,format=None):

        data=request.data
        try:
            obj = Violation.objects.get(id=pk)
        except:
            return Response({"message":"Invalid Id"})
        serializer = ViolationCreateUpdateSerializer(data=data, instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViolationsDeleteAllView(APIView):
    def delete(self,request,format=None):
        Violation.objects.all().delete()
        return Response({"message":"All Records Deleted !!!!!!!!"})


class ViolationsDeleteView(APIView):
    def delete(self,request,pk,format=None):
        Violation.objects.get(id=pk).delete()
        return Response({"message":"Record Deleted !!!!!!!!"})

