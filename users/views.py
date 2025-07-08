from urllib import request
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from users import models
from users.models import Driver, GasOrder, User
from .serializers import ActiveGasOrderSerializer, DriverSerializer, GasOrderForDriverSerializer, GasOrderHistorySerializer, UserProfileSerializer, UserRegistrationSerializer, siverLoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GasOrderSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "تم إنشاء الحساب بنجاح."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = GasOrder.objects.filter(customer=user).order_by('-order_time')
        serializer = GasOrderHistorySerializer(orders, many=True)
        return Response(serializer.data)
    

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        active_order = GasOrder.objects.filter(
            customer=user,
            status__in=['pending', 'assigned']
        ).order_by('-order_time').first()

        if not active_order:
            return Response({"detail": "لا يوجد طلب نشط حاليا"}, status=200)

        serializer = ActiveGasOrderSerializer(active_order)
        return Response(serializer.data)




class GasOrderCreateView(APIView):
    

    def post(self, request):
        serializer = GasOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class AllGasOrdersView(APIView):
    permission_classes = [IsAuthenticated]  # أو استخدم AllowAny مؤقتًا

    def get(self, request):
        orders = GasOrder.objects.all().order_by('-order_time')
        serializer = GasOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    

class AvailableGasOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            driver = Driver.objects.get(user=request.user)
        except Driver.DoesNotExist:
            return Response({"detail": "السائق غير موجود"}, status=404)

        orders = GasOrder.objects.filter(
            status__in=['pending', 'accepted'],
        ).filter(
            Q(driver__isnull=True) | Q(driver=driver)
        )
        serializer = GasOrderForDriverSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)



class AcceptGasOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = GasOrder.objects.get(id=order_id)

            # تحقق أن الطلب لم يُقبل من قبل
            if order.status != 'pending' or order.driver is not None:
                return Response({"detail": "لا يمكن قبول هذا الطلب"}, status=status.HTTP_400_BAD_REQUEST)

            # قبول الطلب
            driver = Driver.objects.get(user=request.user)
            order.driver = driver
            order.status = 'accepted'
            order.save()

            return Response({"detail": "تم قبول الطلب بنجاح"}, status=status.HTTP_200_OK)
        except GasOrder.DoesNotExist:
            return Response({"detail": "الطلب غير موجود"}, status=status.HTTP_404_NOT_FOUND)



class sriverLoginView(APIView):
    def post(self, request):
        print("Received login data:", request.data)  # طباعة البيانات الواردة
        
        serializer = siverLoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        print(f"Attempting auth for: {username}")  # تأكيد اسم المستخدم
        
        # التحقق من وجود المستخدم أولاً
        try:
            driver = Driver.objects.get(user__username=username)

            print(f"User found: {driver.user.username}")


        except Driver.DoesNotExist:
            print("User does not exist")
            return Response({"error": "المستخدم غير موجود"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # المصادقة مع رسائل تفصيلية
        driver = authenticate(username=username, password=password)
        
        if driver:
            refresh = RefreshToken.for_user(driver)
            return Response({
            "message": "تم تسجيل الدخول بنجاح",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            
            })
        else:
            print("Authentication failed - invalid password")
            return Response({

                "error": "كلمة المرور غير صحيحة"
            }, status=status.HTTP_401_UNAUTHORIZED)
        


class DriverRegisterViewsss(APIView):
    def post(self, request):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "تم إنشاء الحساب بنجاح."}, status=status.HTTP_201_CREATED)
        
        else:
            print(serializer.errors)  # اضف هذا السطر لتعرف الخطأ
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
