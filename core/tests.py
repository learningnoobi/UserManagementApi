from django.test import TestCase
from .models import User

class UserTest(TestCase):

    def test_new_superuser(self):
        new_superuser = User.objects.create_superuser(
            email = 'first@gmail.com', first_name='firstname',
            last_name='lastname',password= 'password'
        )

        self.assertEqual(new_superuser.email,'first@gmail.com')
        self.assertEqual(new_superuser.first_name,'firstname')
        self.assertEqual(new_superuser.last_name,'lastname')

        self.assertTrue(new_superuser.is_staff)
        self.assertTrue(new_superuser.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='testuser@super.com', last_name='username1', first_name='first_name', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='testuser@super.com', last_name='username1', first_name='first_name', password='password', is_staff=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='', last_name='username1', first_name='first_name', password='password', is_superuser=True)

    def test_new_user(self):
        user = User.objects.create_user(
             email = 'first@gmail.com', first_name='firstname',
            last_name='lastname',password= 'password'
            )
        self.assertEqual(user.email, 'first@gmail.com')
        self.assertEqual(user.last_name, 'lastname')
        self.assertEqual(user.first_name, 'firstname')

        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='a@gmail.com', last_name='', first_name='first_name', password='password')
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='a@gmail.com', last_name='', first_name='first_name', password='password')
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='a@gmail.com', last_name='sdf', first_name='', password='password')
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='a@gmail.com', last_name='ds', first_name='first_name', password='')