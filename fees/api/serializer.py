from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Students, FeeStructure, FeePayment, Announcement

class UserSerializer(serializers.ModelSerializer):
    student_profile = serializers.PrimaryKeyRelatedField(
        queryset=Students.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'student_profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class StudentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Students
        fields = ['id', 'user', 'user_id', 'roll_no', 'course', 'semester', 'profile']

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class FeePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment
        fields = '__all__'

class AnnouncementSerialzer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'
