from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.views import LoginView, APIView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.models import Address, PhoneNumber, Profile
from users.permissions import IsUserAddressOwner, IsUserProfileOwner
from users.serializers import (
    AddressReadOnlySerializer,
    PhoneNumberSerializer,
    ProfileSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    VerifyPhoneNumberSerialzier,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


User = get_user_model()

class ProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """

    serializer_class = ProfileSerializer
    permission_classes = (IsUserProfileOwner,)
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        try:
            # Retrieve token from headers
            auth_header = self.request.headers.get("Authorization")
            if auth_header is None:
                raise AuthenticationFailed("Authorization header is missing")
            
            # Extract token from the header
            token = auth_header.split(" ")[1]
            print(token)

            # Decode the token to get user information
            decoded_token = JWTAuthentication().get_validated_token(token)
            user_id = decoded_token["user_id"]

            # Retrieve user profile based on user_id
            profile = Profile.objects.get(user_id=user_id)
            return profile

        except Exception as e:
            raise AuthenticationFailed("Invalid token")


class UserRegistrationAPIView(RegisterView):
    """
    Register new users using phone number or email and password.
    """

    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            print(errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Include the user's data or a success message in the response
        return Response(
            {"message": "Registration successful", "user": serializer.data}, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

class UserLoginAPIView(LoginView):
    """
    Authenticate existing users using phone number or email and password.
    """

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    # def post(self, request, *args, **kwargs):
    #     # Get serializer instance
    #     serializer = self.get_serializer(data=request.data)
        
    #     # Check if the data is valid
    #     if serializer.is_valid():
    #         # If valid, perform login
    #         # return self.form_valid(serializer)
    #         pass
    #     else:
    #         # If not valid, handle errors
    #         errors = serializer.errors
    #         print(errors)
    #         # return self.form_invalid(serializer)

        



class SendOrResendSMSAPIView(GenericAPIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """

    serializer_class = PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Send OTP
            phone_number = str(serializer.validated_data["phone_number"])

            user = User.objects.filter(phone__phone_number=phone_number).first()

            sms_verification = PhoneNumber.objects.filter(
                user=user, is_verified=False
            ).first()

            sms_verification.send_confirmation()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneNumberAPIView(GenericAPIView):
    """
    Check if submitted phone number and OTP matches and verify the user.
    """

    serializer_class = VerifyPhoneNumberSerialzier

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            message = {"detail": _("Phone number successfully verified.")}
            return Response(message, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    """
    Social authentication with Google
    """

    adapter_class = GoogleOAuth2Adapter
    callback_url = "call_back_url"
    client_class = OAuth2Client


# class ProfileAPIView(RetrieveUpdateAPIView):
#     """
#     Get, Update user profile
#     """

#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = (IsUserProfileOwner,)

#     def get_object(self):
#         return self.request.user.profile


class UserAPIView(RetrieveAPIView):
    """
    Get user details
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AddressViewSet(ReadOnlyModelViewSet):
    """
    List and Retrieve user addresses
    """

    queryset = Address.objects.all()
    serializer_class = AddressReadOnlySerializer
    permission_classes = (IsUserAddressOwner,)

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(user=user)

class UserLogoutAPIView(APIView):
    """
    Log out a user by blacklisting the refresh token.
    """

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Failed to log out."}, status=status.HTTP_400_BAD_REQUEST)