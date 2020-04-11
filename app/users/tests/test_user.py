from django.test import TestCase
from django.contrib.auth import authenticate, get_user_model


def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserTests(TestCase):
    """"Test the user functions (public)"""
    
    def test_login_successful(self):
        """Test user authentication is successful"""
        credentials = {
            'email': 'test@coderasha.com',
            'password': '123pass',
        }
        create_user(**credentials)
        user_login = authenticate(email=credentials['email'], password=credentials['password'])
        self.assertTrue(user_login)

    def test_user_exist(self):
        """Testing if user exist"""
        credentials = {
            'email': 'test@coderasha.com',
            'password': '12',
            }
        user = create_user(**credentials)
        user_exists = get_user_model().objects.filter(
            email=credentials['email']
        ).exists()
        self.assertTrue(user_exists)  
