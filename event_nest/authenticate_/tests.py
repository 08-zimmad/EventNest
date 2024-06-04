# from django.test import TestCase
# from django.urls import reverse
# from unittest.mock import patch
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class OAuthTests(TestCase):
#     def setUp(self):
#         self.client = self.client_class()

#     @patch('allauth.socialaccount.providers.google.views.GoogleOAuth2Adapter.complete_login')
#     @patch('allauth.socialaccount.providers.google.views.requests')
#     def test_google_login(self, mock_requests, mock_complete_login):
#         # Mock the response from Google
#         mock_response = mock_requests.get.return_value
#         mock_response.json.return_value = {
#             'id': '1234567890',
#             'email': 'testuser@example.com',
#             'verified_email': True,
#             'name': 'Test User',
#             'given_name': 'Test',
#             'family_name': 'User',
#             'picture': 'https://example.com/profile.jpg',
#         }
        
#         # Mock the complete_login method
#         mock_complete_login.return_value = None
        
#         # Simulate a login via Google
#         response = self.client.get(reverse('socialaccount_login', kwargs={'provider': 'google'}))
        
#         self.assertEqual(response.status_code, 302)  # Redirect to OAuth provider

#         # Mock the callback from Google
#         response = self.client.get(reverse('google_callback'), data={'code': 'test-code'})
        
#         self.assertEqual(response.status_code, 302)  # Redirect after successful login
        
#         # Check if the user is created and logged in
#         user = User.objects.get(email='testuser@example.com')
#         self.assertIsNotNone(user)
#         self.assertTrue(user.is_authenticated)

#     @patch('allauth.socialaccount.providers.github.views.GitHubOAuth2Adapter.complete_login')
#     @patch('allauth.socialaccount.providers.github.views.requests')
#     def test_github_login(self, mock_requests, mock_complete_login):
#         # Mock the response from GitHub
#         mock_response = mock_requests.get.return_value
#         mock_response.json.return_value = {
#             'id': '987654321',
#             'login': 'testuser',
#             'email': 'testuser@example.com',
#             'name': 'Test User',
#             'avatar_url': 'https://example.com/avatar.jpg',
#         }
        
#         # Mock the complete_login method
#         mock_complete_login.return_value = None
        
#         # Simulate a login via GitHub
#         response = self.client.get(reverse('socialaccount_login', kwargs={'provider': 'github'}))
        
#         self.assertEqual(response.status_code, 302)  # Redirect to OAuth provider

#         # Mock the callback from GitHub
#         response = self.client.get(reverse('github_callback'), data={'code': 'test-code'})
        
#         self.assertEqual(response.status_code, 302)  # Redirect after successful login
        
#         # Check if the user is created and logged in
#         user = User.objects.get(email='testuser@example.com')
#         self.assertIsNotNone(user)
#         self.assertTrue(user.is_authenticated)
