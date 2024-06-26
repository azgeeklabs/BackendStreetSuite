from rest_framework import status , generics
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from UserApp.models import Profile
from UserApp.api.serializers import UserSerializer, ProfileSerializer ,ResetForgetPasswordSerializer, VerificationForgetPasswordSerializer ,VerificationSerializer , RegistrationSerializer , ForgetPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.contrib.auth.models import User
#### auth ####
from django.conf import settings
from django.shortcuts import redirect 
from django.views.generic.base import View
from django.contrib.auth import authenticate

### endpoint for resgisteration ###
class SignUpView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(    
            {"message": "The verification code has been sent to your email."},
            status=status.HTTP_201_CREATED
        )

## end point for verification on sign up ##
class VerificationView(generics.CreateAPIView):
    serializer_class = VerificationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "User created successfully."},
                status=status.HTTP_201_CREATED
            )
        except :
            return Response(
                {"message": "please enter the valid verification code "},
                status=status.HTTP_400_BAD_REQUEST
            )

### endpoint to log in via google account ###
class GoogleRedirectURIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Extract the authorization code from the request URL
        code = request.GET.get('code')
        print(f"Authorization code: {code}")
        
        if code:
            print("Received authorization code")
            
            # Prepare the request parameters to exchange the authorization code for an access token
            token_endpoint = 'https://oauth2.googleapis.com/token'
            token_params = {
                'code': code,
                'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                'redirect_uri': 'http://127.0.0.1:8000/accounts/google/login/callback/',  # Must match the callback URL configured in your Google API credentials
                'grant_type': 'authorization_code',
            }
            
            # Make a POST request to exchange the authorization code for an access token
            response = requests.post(token_endpoint, data=token_params)
            print('POST request sent to token endpoint')
            
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                
                if access_token:
                    print(f'Received access token:{access_token}')
                    
                    # Make a request to fetch the user's profile information
                    profile_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
                    headers = {'Authorization': f'Bearer {access_token}'}
                    profile_response = requests.get(profile_endpoint, headers=headers)
                    
                    if profile_response.status_code == 200:
                        print("Received profile information")
                        data = {}
                        profile_data = profile_response.json()
                        
                        # Extract user data from the profile
                        email = profile_data["email"]
                        print(email)
                        first_name = profile_data["given_name"]
                        print(first_name)
                        last_name = profile_data.get("family_name", "")
                        print(last_name)
                        
                        # Try to get an existing user by email, or create a new one
                        ## if user already exists ##
                        try:
                            user = User.objects.get(email=email)
                            print('welcome')
                        except User.DoesNotExist:
                            print('new')
                            user = User.objects.create(
                                email=email,
                                first_name=first_name,
                                last_name=last_name
                            )
                            user.username = f"{first_name}{user.id}"
                            user.save()
                        # Generate tokens for the user
                        finally:
                            refresh = RefreshToken.for_user(user)
                            data['access'] = str(refresh.access_token)
                            data['refresh'] = str(refresh)
                            data['Token'] = str(Token.objects.get(user = user.id))
                            print(data['access'])
                            print(data['refresh'])
                            print(data['Token'])
                            return Response(data,status=status.HTTP_200_OK)
        
        return Response({"message": "sorry ! sign up process have some issues"}, status=status.HTTP_400_BAD_REQUEST)
class GoogleLogIn(View):
    permission_classes = [AllowAny]

    def get(self, request):
        redirect_uri = 'http://127.0.0.1:8000/accounts/google/login/callback/'  # Update with your actual redirect URI
        scope = 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY

        # Constructing the authentication URL with prompt=select_account
        redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&scope={scope}&access_type=offline&redirect_uri={redirect_uri}&prompt=select_account"

        return redirect(redirect_url)    
# class GoogleLogin(SocialLoginView): 
#     serializer_class = LoginSerializer   
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = 'http://127.0.0.1:8000/accounts/google/login/callback/'
#     client_class = OAuth2Client

### endpoint for forget password ###
class ForgetPassword(generics.CreateAPIView):
    serializer_class = ForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            token = getattr(serializer, 'token' , None)
            print(f'the token: {token}')
            return Response({"message":"the verification code has been sent to your email!","token":token})
        else:
            return Response(
                {"message": "the email yo have sent is not in the system please sign up first!"},
                status=status.HTTP_400_BAD_REQUEST
            )

### verify forget password verification code ###
class VerifyForgetPasswordView(generics.CreateAPIView):
    serializer_class = VerificationForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            token = token.split(' ')[1]
            print('token2'+token)
        serializer = self.get_serializer(data=request.data, context={'request': request, 'token': token})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "correct verification code"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "please enter the valid verification code !"},
                status=status.HTTP_400_BAD_REQUEST)

### reset password for user forgot password ###
class ResetPasswordView(generics.CreateAPIView):
    serializer_class = ResetForgetPasswordSerializer

    def create(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            token = token.split(' ')[1]
            print(f'the tokeny:{token}')
        serializer = self.get_serializer(data=request.data, context={'request': request, 'token': token})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "password reset process done!"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST',])
def RegistrationView(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        data = request.data.copy()
        email = data['email']
        username , tail = email.split("@")
        data['username'] = username



        serializer = UserSerializer(data=data)  
        data = {}

        if serializer.is_valid():
            account = serializer.save()
        #     data['response'] = "successfully registered"
        #     data['username'] = account.username
        #     data['email'] = account.email
        #     data['first_name'] = account.first_name
        #     data['last_name'] = account.last_name
        #     token = Token.objects.get(user=account).key
        #     data['token'] = token
        else:
            data = serializer.errors
        
        return Response(data)

@api_view(['POST',])
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response({'Response' : 'logout successfully'})
    
@api_view(['GET', 'PATCH',])
@permission_classes([IsAuthenticated])
def ProfileView(request, pk):
    profile = Profile.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    if request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400)
        
@api_view(['POST'])
def log_in(request):
    data = request.data.copy()
    email = data['email']
    print(email)
    password = data['password']
    try:
        user = User.objects.get(email=email)
        username = user.username
        print(username)
        user2 = authenticate(username=username , password=password)
        if user2:
            token = Token.objects.get(user=user)
            return Response({"message":"loged in successfully!","token":token.key},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message':'wrong password'},status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message":"your email not exists in the website"},status=status.HTTP_404_NOT_FOUND)
    
# @api_view(['POST'])
# def sign_up(request):
#     serializer = SignupSerializer(data=request.data)
#     if serializer.is_valid(request):
#         return Response({"message":"cool"} , status=status.HTTP_200_OK)