from django.test import TestCase
from django.test.client import Client


class ViewTest(TestCase):
  fixtures = ['test_data.json']

  def setUp(self):
    self.client = Client()

  def test_register_page(self):
    data = {
      'username': 'test_user',
      'email': 'test_user@example.com',
      'password1': '1',
      'password2': '1'
    }
    response = self.client.post('/register/', data)
    self.assertEqual(response.status_code, 302)

  def test_bookmark_save(self):
    response = self.client.login('/save/', 'ayman', '1')
    self.assertTrue(response)

    data = {
      'url': 'http://www.example.com/',
      'title': 'Test URL',
      'tags': 'test-tag'
    }
    response = self.client.post('/save/', data)
    self.assertEqual(response.status_code, 302)

    response = self.client.get('/user/ayman/')
    self.assertTrue('http://www.example.com/' in response.content)
    self.assertTrue('Test URL' in response.content)
    self.assertTrue('test-tag' in response.content)

