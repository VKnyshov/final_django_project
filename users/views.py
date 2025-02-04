from django.utils.timezone import now
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserUpdateSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from .serializers import UserListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .models import CustomUser

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserLoginView(APIView):
    def post(self, request):
        email = request.query_params.get('email') or request.data.get('email')
        password = request.query_params.get('password') or request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email і пароль обов’язкові!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserLoginSerializer(data={"email": email, "password": password})
        if serializer.is_valid():
            user = User.objects.get(email=email)
            user.last_login = now()
            user.save()

            return Response(
                {
                    "message": "Успішна авторизація",
                    "tokens": serializer.validated_data["tokens"],
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.last_logout = now()
        user.save()

        return Response({"message": "Користувач вийшов"}, status=status.HTTP_200_OK)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({
            'message': 'Користувач успішно видалений'
        }, status=status.HTTP_204_NO_CONTENT)


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user


class UserFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr='exact')
    email = filters.CharFilter(field_name="email", lookup_expr='icontains')
    full_name = filters.CharFilter(field_name="full_name", lookup_expr='icontains')
    last_login = filters.DateTimeFilter(field_name="last_login", lookup_expr='exact')

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'last_login']


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get("id")
        email = request.query_params.get("email")

        if not user_id and not email:
            return Response({"error": "Необхідно вказати id або email"}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        if user_id:
            user = User.objects.filter(id=user_id).first()
        elif email:
            user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "Користувача не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserListSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFilterView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
