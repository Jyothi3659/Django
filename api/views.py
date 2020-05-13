from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .utils import get_and_authenticate_user, create_user_account
from django.contrib.auth import get_user_model, logout
from . import serializers
from .utils import get_and_authenticate_user

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        # import ipdb; ipdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.UserLoginSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
    
    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    # @action(methods=['POST', ], detail=False)
    # def logout(self, request):
    #     # import ipdb; ipdb.set_trace()
    #     logout(request)
    #     data = {'success': 'Sucessfully logged out'}
    #     return Response(data=data, status=status.HTTP_200_OK)






# from django.contrib.auth import get_user_model
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# from .serializers import *
# from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.generics import CreateAPIView
# from rest_framework.permissions import AllowAny
# from django.contrib.auth import get_user_model, logout


# class UserCreateAPIView(CreateAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserCreateSerializer
#     queryset = User.objects.all()


# class UserLoginAPIView(APIView):
#     permission_classes = [AllowAny]
#     # import ipdb; ipdb.set_trace()
#     serializer_class = UserLoginSerializer
#     def post(self, request, *args, **kwargs):
#         # import ipdb; ipdb.set_trace()
#         data = request.data
#         serializer = UserLoginSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             new_data = serializer.data
#             return Response(new_data, status = HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# class UserLogoutview(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         # import ipdb; ipdb.set_trace()
#         logout(request)
#         data = {'success': 'Sucessfully logged out'}
#         return Response(data=data, status=HTTP_200_OK)

# class Logout(APIView):
#     permission_classes = [AllowAny]
#     def get(self, request, format=None):
#         # simply delete the token to force a login
#         request.user.auth_token.delete()
#         return Response(status=HTTP_200_OK)


# class LoginView(APIView):
#     # permission_classes = (AllowAny,)
#     def post(self,request):
#         # import ipdb; ipdb.set_trace()
#         username = request.data.get('username',None)
#         password = request.data.get('password',None)
#         if username and password:
#             users = User.objects.all()
#             pswd = users.get(username=username).password   
#             user_obj = User.objects.filter(Q(username=username)).distinct()
#             if user_obj.exists() and user.count()==1:
#                 user_obj = user.first()
#             else:
#                 raise ValidationError("This username is not valid")
#                 return Response({"message": "Login Successfully", "data":data_list, "code": 200})
#             else:
#                 message = "Unable to login with given credentials"
#                 return Response({"message": message , "code": 500, 'data': {}} )
#         else:
#             message = "Invalid login details."
#             return Response({"message": message , "code": 500, 'data': {}})



#          def validate(self, data):
#         username = data.get('username', None)
#         username = data["password"]
#         user_obj = None

#         if not username:
#             raise ValidationError("A username or email is required to login.")
#         user = User.objects.filter(
#             Q(username = username)
#         ).distinct()

#         if user.exists() and user.count() == 1:
#             user_obj = user.first()

#         else:
#             raise ValidationError("This username is not valid")

#         if user_obj:
#             if not user_obj.check_password(password):
#                 raise ValidationError("Invalid Credentials please try again")