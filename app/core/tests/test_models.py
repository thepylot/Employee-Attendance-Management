from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from core import models

def sample_user(email='test@reversepython.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'test@coderasha.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@CODERASHA.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        
        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'pass123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@coderasha.com',
            'Testpass123'
            
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_create_user_with_extrafields(self):
            """Test creating a new user with extra fields"""
            email='test@coderasha.com'
            password='testpass123'
            name='Test User'
            user = get_user_model().objects.create_user(
                email=email,
                password=password,
                name=name,
            )
            self.assertEqual(user.email, email)
            self.assertEqual(user.name, name)
    
    def test_create_leave_successfull(self):
        """Test creating a new leave is successful with string representation"""
        leave = models.Leave.objects.create(
            user=sample_user(),
            leave_type='Holiday',
            leave_start_date='2020-04-20',
            leave_end_date='2020-04-21',
            leave_start_time='12:30',
            leave_end_time='12:30',
            leave_reason='Test reason',
        )

        self.assertEqual(str(leave), leave.leave_type)
    
    def test_date_format_invalid(self):
        """Test creating a new leave with wrong date format"""
        with self.assertRaises(ValidationError):
            leave = models.Leave.objects.create(
                user=sample_user(),
                leave_type='Holiday',
                leave_start_date='2020/04/20',
                leave_end_date='2020/04/21',
                leave_start_time='12:30',
                leave_end_time='12:30',
                leave_reason='Test reason',
            )

    def test_profile_picture_created_succesful(self):
        """Testing profile picture created succesfull when user created"""
        user = sample_user()
        profilepic = models.ProfilePic.objects.filter(
            user=user
        ).exists()
        self.assertTrue(profilepic)

