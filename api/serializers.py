from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from rest_framework.serializers import CharField, ValidationError

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    # import ipdb; ipdb.set_trace()
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token'
        ]
        extra_kwargs =  {"password":
                        {"write_only":True}
                    }

    def validate(self, data):
        # 
        username = data.get('username', None)
        password = data['password']
        user_obj = None
        # import ipdb; ipdb.set_trace()
        if not username:
            raise ValidationError("A username or email is required to login.")
        user = User.objects.filter(username = username)
        
        if user.exists() and user.count() == 1:
            user_obj = user.first()

        else:
            raise ValidationError("This username is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Invalid Credentials please try again")
        
        user_token = None
        user_id = None
        # import ipdb; ipdb.set_trace()
        for each in User.objects.filter(username = username).values('id'):
            user_id = each['id']
        user_temp = Token.objects.filter(user = user_id)
        for each in user_temp:
            user_token = each
        data["token"] = user_token
        return data
    
class AuthUserSerializer(serializers.ModelSerializer):
    
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('username', 'password', 'auth_token')
        #  read_only_fields = ('id', 'is_active', 'is_staff')
    
    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
        extra_kwargs =  {"password":
                        {"write_only":True}
                    }

    def create(self, validated_data):
        # import ipdb; ipdb.set_trace()
        username = validated_data['username'],
        password = validated_data['password']
        
        user_obj = User(
            username = username,
            password = password
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data




# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth import get_user_model
# from rest_framework.serializers import ModelSerializer
# from rest_framework.serializers import CharField, ValidationError
# from django.db.models import Q
# from rest_framework.authtoken.models import Token

# User = get_user_model()


# class UserSerializer(ModelSerializer):

#     password = CharField(write_only=True)

#     def create(self, validated_data):

#         user = User.objects.create(
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()

#         return user

#     class Meta:
#         model = User
#         # Tuple of serialized model fields (see link [2])
#         fields = ( "username", "password", )



# class UserCreateSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'password'
#         ]
#         extra_kwargs =  {"password":
#                         {"write_only":True}
#                     }

#     # def create(self, validated_data):
#     #     # import ipdb; ipdb.set_trace()
#     #     username = validated_data['username'],
#     #     password = validated_data['password']
        
#     #     user_obj = User(
#     #         username = username,
#     #         password = password
#     #     )
#     #     user_obj.set_password(password)
#     #     user_obj.save()
#     #     return validated_data

# # class UserLoginSerializer(ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = ('username','password')

# class UserLoginSerializer(ModelSerializer):
#     token = CharField(allow_blank=True, read_only=True)
#     username = CharField(required=False, allow_blank=True)
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'password',
#             'token'
#         ]
#         extra_kwargs =  {"password":
#                         {"write_only":True}
#                     }

#     def validate(self, data):
#         # 
#         username = data.get('username', None)
#         password = data['password']
#         user_obj = None
#         # import ipdb; ipdb.set_trace()
#         if not username:
#             raise ValidationError("A username or email is required to login.")
#         user = User.objects.filter(username = username)
        
#         if user.exists() and user.count() == 1:
#             user_obj = user.first()

#         else:
#             raise ValidationError("This username is not valid")

#         if user_obj:
#             if not user_obj.check_password(password):
#                 raise ValidationError("Invalid Credentials please try again")
        
#         user_token = None
#         user_id = None
#         # import ipdb; ipdb.set_trace()
#         for each in User.objects.filter(username = username).values('id'):
#             user_id = each['id']
#         user_temp = Token.objects.filter(user = user_id)
#         for each in user_temp:
#             user_token = each
#         data["token"] = user_token
#         return data
