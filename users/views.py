from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Address
from .serializers import UserSerializer, UserRegistrationSerializer, AddressSerializer
from lib.email_utils import send_welcome_email

class RegisterView(generics.CreateAPIView):
    """İstifadəçi qeydiyyatı"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Xoş gəlmə emaili göndəririk
        try:
            send_welcome_email(user)
        except Exception as e:
            print(f"⚠️ Email göndərilmədi: {str(e)}")
            # Email göndərilməsə də qeydiyyat uğurlu olur
        
        # JWT token yaradırıq
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Qeydiyyat uğurla tamamlandı! Xoş gəlmə emaili göndərildi.'
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """İstifadəçi girişi"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'İstifadəçi adı və şifrə tələb olunur!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    else:
        return Response({
            'error': 'İstifadəçi adı və ya şifrə yanlışdır!'
        }, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(generics.RetrieveUpdateAPIView):
    """İstifadəçi profili"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class AddressListCreateView(generics.ListCreateAPIView):
    """İstifadəçi ünvanları siyahısı və yaratma"""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user, is_active=True)

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Ünvan detalları"""
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        # Ünvanı silmək əvəzinə deaktiv edirik
        instance.is_active = False
        instance.save()
