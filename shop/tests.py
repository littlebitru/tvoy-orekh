from django.test import TestCase
from django.urls import reverse
from .models import Order, Product, User


class ShopFlowTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Миндаль', description='Свежий миндаль', price=390)

    def test_registration_requires_contact_fields(self):
        response = self.client.post(reverse('register'), {
            'username': 'anna', 'first_name': '', 'last_name': '', 'email': '', 'phone': '',
            'password1': 'Strong-pass-123', 'password2': 'Strong-pass-123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='anna').exists())

    def test_customer_can_make_order(self):
        user = User.objects.create_user('anna', email='anna@example.com', phone='123', first_name='Анна', last_name='Иванова', password='Strong-pass-123')
        self.client.force_login(user)
        self.client.post(reverse('add_to_cart', args=[self.product.pk]))
        response = self.client.post(reverse('checkout'))
        self.assertRedirects(response, reverse('account'))
        self.assertEqual(Order.objects.get(user=user).total, self.product.price)
