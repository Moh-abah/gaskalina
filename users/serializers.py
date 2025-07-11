from rest_framework import serializers
from .models import Driver, GasOrder, User
from django.db import transaction

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'fullname',
            'username',
            'password',
            'phone_number',
            'fixed_location_lat',
            'fixed_location_lon',
            'neighborhood',
            'location_notes',
            'email',
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            fullname=validated_data['fullname'],
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            fixed_location_lat=validated_data.get('fixed_location_lat'),
            fixed_location_lon=validated_data.get('fixed_location_lon'),
            neighborhood=validated_data.get('neighborhood'),
            location_notes=validated_data.get('location_notes'),
            email=validated_data['email'],
        )
        return user
    



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'fullname',
            'username',
            'phone_number',
            'neighborhood',
            'location_notes',
            'email',
        ]
        extra_kwargs = {
            'username': {'required': True},
        }



#class DriverSerializer(serializers.ModelSerializer):
  #  password = serializers.CharField(write_only=True)

   # class Meta:
    #    model = Driver
     #   fields = [
      #      'username',
       #     'password',
        #    'phone_number',
         #   'carnumber',
            
#        ]

 #   def create(self, validated_data):
  #      driver = Driver.objects.create_user(
   #         username=validated_data['username'],
    #        password=validated_data['password'],
     #       phone_number=validated_data['phone_number'],
      #      carnumber=validated_data['carnumber'],
       # )
        #return driver


class ActiveGasOrderSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.user.username', read_only=True)
    driver_phone = serializers.CharField(source='driver.user.phone_number', read_only=True)

    class Meta:
        model = GasOrder
        fields = [
            'id',
            'status',
            'order_time',
            'neighborhood',
            'floor_number',
            'apartment_number',
            'driver_name',
            'driver_phone',
        ]




class GasOrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GasOrder
        fields = [
            'id',
            'status',
            'order_time',
            'neighborhood',
            'floor_number',
            'apartment_number',
        ]




    
class DriverSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    carnumber = serializers.CharField()
    email = serializers.CharField()
    Identitynumber = serializers.CharField()


    class Meta:
        model = Driver
        fields = ['fullname','username', 'password', 'phone_number', 'carnumber','email','Identitynumber']

    def create(self, validated_data):
        fullname = validated_data.pop('fullname')
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        phone_number = validated_data.pop('phone_number')
        carnumber = validated_data.pop('carnumber')
        email = validated_data.pop('email')
        Identitynumber = validated_data.pop('Identitynumber')
        # تحقق قبل الإنشاء  
        
        

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("اسم المستخدم موجود بالفعل")
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("رقم الهاتف مستخدم بالفعل")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("البريد الالكتروني مستخدم بالفعل ")
        

        if Driver.objects.filter(carnumber=carnumber).exists():
            raise serializers.ValidationError("رقم السيارة مستخدم بالفعل")
        
        if Driver.objects.filter(Identitynumber=Identitynumber).exists():
            raise serializers.ValidationError("رقم الهويه مستخدم بالفعل")

        try:
            with transaction.atomic():  # ضمان الاتومية
                user = User.objects.create_user(
                    fullname=fullname,
                    username=username,
                    password=password,
                    phone_number=phone_number,
                    email=email
                )
                driver = Driver.objects.create(user=user, carnumber=carnumber,Identitynumber=Identitynumber)
        except Exception as e:
            # لو حدث أي خطأ بعد إنشاء المستخدم، يتم التراجع تلقائياً بسبب atomic
            raise serializers.ValidationError(f"خطأ أثناء إنشاء السائق: {str(e)}")

        return driver   



class GasOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasOrder
        fields = '__all__'
        read_only_fields = ['customer', 'order_time', 'status']


class GasOrderForDriverSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    is_accepted_by_me = serializers.SerializerMethodField()

    def get_is_accepted_by_me(self, obj):
        request = self.context.get('request')
        return obj.driver == request.user


    class Meta:
        model = GasOrder
        fields = [
            'id',
            'customer_username',
            'order_time',
            'location_lat',
            'location_lon',
            'neighborhood',
            'location_notes',
            'floor_number',
            'apartment_number',
            'status',
            'is_accepted_by_me',  # ✅ هذا الحقل الجديد
        ]


class siverLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )