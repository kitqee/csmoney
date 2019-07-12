from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.utils import generate_code
from core.validators import PhoneUniqueValidator, PhoneValidator, validate_code

User = get_user_model()


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[PhoneValidator()])


class SMSSendCodeSerializer(PhoneSerializer):

    def validate_phone(self, phone):
        code = generate_code(6)
        # TODO: Send sms
        # sms_body = f'Your authorization code: {code}'
        cache.set(phone, code, timeout=900)
        if settings.DEBUG:
            return code
        return phone


class SMSLoginSerializer(PhoneSerializer, CodeSerializer):

    def validate(self, attrs):
        attrs = super().validate(attrs)
        phone = attrs.get('phone')
        code = attrs.get('code')
        validate_code(code, phone)
        user = User.objects.filter(phone=phone).first()

        if not user:
            raise serializers.ValidationError('User is not exist')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled')

        return {'user': user}


class RegisterSerializer(CodeSerializer):
    phone = serializers.CharField(validators=[PhoneUniqueValidator()])

    def validate(self, attrs):
        attrs = super().validate(attrs)
        phone = attrs.get('phone')
        code = attrs.pop('code')
        validate_code(code, phone)

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(validated_data.pop('phone'))

    def to_representation(self, instance):
        serializer = UserSerializer(instance, context=self.context)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'phone',
            'last_login',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'birthday',
            'about_me'
        ]
        read_only_fields = ['id', 'phone', 'last_login', 'is_active']

    def update(self, instance, validated_data):
        birthday = validated_data.get('birthday')
        if birthday and instance.birthday != birthday:
            if instance.number_bd_changes >= settings.NUMBER_BD_CHANGES:
                raise ValidationError(
                    f"You can't change birthdate more "
                    f'than {settings.NUMBER_BD_CHANGES} times'
                )
            instance.number_bd_changes += 1
        return super().update(instance, validated_data)
