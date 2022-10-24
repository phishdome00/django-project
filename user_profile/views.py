from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import ProfileSignupSerializer,UserLoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
import random
from django.utils import timezone
from django.core.mail import send_mail


# Create your views here.

class AuthSignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request,format=None):
        try:
            data = request.data
            try:
                user=User.objects.get(email=data['user_fk']['email'])
                if user:
                    return Response({"message":"Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                pass
            serializer = ProfileSignupSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get (id=serializer.data['user_fk'].get('id'))
                ## Signing in ##
                login(request, user)
                serializer = UserLoginSerializer(user)
                token, created = Token.objects.get_or_create(user=user)
                user_details = serializer.data
                user_details['token'] = token.key
                return Response(user_details, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        except Exception as e:
            return Response({"message":"Username aleady exists"}, status=status.HTTP_400_BAD_REQUEST)


class AuthLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request,format=None):
        data = request.data
        username = data.get('username', None)
        email = data.get('email',None)
        password = data['password']

        if username:
            try:
                user=User.objects.get(username=username)
            except:
                return Response({"message":"Username Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
        elif email:
            try:
                user=User.objects.get(email=email)
            except Exception as e:
                return Response({"message":"Email Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
            
        if username:

            try:
                ## Authenticate ##
                user = authenticate(username=username, password=password)
            except:
                user = None

        elif email:
            try:
                username=user.username
                ## Authenticate ##
                user = authenticate(username=username, password=password)
            except:
                user = None

        if user is not None:
            ## Login ##
            login(request, user)
            serializer = UserLoginSerializer(user)
            token, created = Token.objects.get_or_create(user=user)
            user_details = serializer.data
            user_details['token'] = token.key
            return Response(user_details, status=status.HTTP_200_OK)

        return Response({"message":"Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class AuthChangePasswordView(APIView):
    permission_classes = (AllowAny,)

    def put(self,request,format=None):
        try:
            user = request.user
            if user:
                data = request.data
                password1 = data.get('new_password')
                password2 = data.get('confirm_password')
                if password1==password2:
                    user.set_password(password1)
                    user.save()
                    return  Response({"message":"Password Change Successfully"})
                else:
                    return Response({"message":"Passsword not match"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

class SocialLoginView(APIView):
    def post(self,request,format=None):
        try:
            user = User.objects.get(email=request.data['email'])
        except:
            user = None




class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request,format=None):
        email = request.data['email']
        user = self.get_id_from_email(email)
        if not user:
            return Response({"message": "EMAIL_NOT_EXIST"}, status=status.HTTP_400_BAD_REQUEST)        
        otp = int(random.randrange(111111,999999))
        user.profile.otp = otp
        user.profile.otp_send_time = timezone.now()
        user.profile.save()
        
        body = "Hello! Your OTP to reset password is "+ str(otp) +". The OTP is valid for 1 Hour!"
        send_mail('Reset Password',
                body,
                'Dont Reply <puneet76.sharma@gmail.com>',
                [email],
                fail_silently=False,
            )
        return Response({"message":"OTP Sent"})

    def get_id_from_email(self,email):
        try:
            user = User.objects.get(email=email)
            if user:
                return user
        except Exception as e:
            return None


class VerifyOTPView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        otp = request.data['otp']
        try:
            user = self.get_id_from_email(request.data['email'])
        except:
            return Response({"message": "EMAIL_NOT_EXIST"}, status=status.HTTP_400_BAD_REQUEST)        

        if user.profile.otp != otp:
            return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)        
        time_now = timezone.now()
        time_difference = time_now.hour - user.profile.otp_send_time.hour

        if ( (time_difference >= 1) or (time_now.date() != user.profile.otp_send_time.date())):
            return Response({"message": "OTP_EXPIRED"}, status=status.HTTP_400_BAD_REQUEST)        
            
        user.profile.otp=1
        user.profile.save()
        return Response({"message":"OTP_VERIFID"}, status=status.HTTP_200_OK)
    
    
    def get_id_from_email(self,email):
        try:
            user = User.objects.get(email=email)
            if user:
                return user
        except Exception as e:
            return None
    

class ResetPasswordView(APIView):

    permission_classes = (AllowAny,)

    """
    Reset Password 

    """

    def put(self, request, format=None):
        # data ={}
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']
        if new_password == confirm_password:
            try:
                user = self.get_id_from_email(request.data['email'])
            except:
                return Response({"message":"INVALID_CREDENTIALS"}, status=status.HTTP_200_OK)

            if user.profile.otp == '1':
                user.set_password(new_password)
                user.save()
                user.profile.otp=None
                user.profile.otp_send_time=None
                user.profile.save()

                return Response({"message":"PASSWORD_RESET_SUCCESSFULLY"}, status=status.HTTP_200_OK)

            else:
                return Response({"message":"PASSWORD_RESET_FAILED"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"PASSWORD_DOES_NOT_MATCH"}, status=status.HTTP_400_BAD_REQUEST)



    
    def get_id_from_email(self,email):
        try:
            user = User.objects.get(email=email)
            if user:
                return user
        except Exception as e:
            return None