from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APISimpleTestCase, APITestCase

User = get_user_model()


class TestSendSMS(APISimpleTestCase):
    def setUp(self):
        self.phone = '88005553535'
        self.url = reverse('send_sms')
        cache.clear()

    def make_request(self, phone):
        payload = {'phone': phone}
        return self.client.post(self.url, payload)

    def test_send_sms_success(self):
        self.assertIsNone(cache.get(self.phone))
        response = self.make_request(self.phone)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cache.get(self.phone))

    def test_send_sms_invalid(self):
        self.assertIsNone(cache.get(self.phone))
        response = self.make_request('invalid_phone')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(cache.get(self.phone))


class TestRegister(APITestCase):
    def setUp(self):
        self.phone = '88005553535'
        self.code = '1984'
        self.url = reverse('register')
        cache.set(self.phone, self.code, timeout=60)

    def make_request(self, phone, code):
        payload = {'phone': phone, 'code': code}
        return self.client.post(self.url, payload)

    def test_register_success(self):
        response = self.make_request(self.phone, self.code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.filter(phone=self.phone).exists()
        self.assertTrue(user)

    def test_register_invalid_code(self):
        response = self.make_request(self.phone, 'invalid')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user = User.objects.filter(phone=self.phone).exists()
        self.assertFalse(user)
