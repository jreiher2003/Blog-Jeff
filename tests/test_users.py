import unittest 
from base import BaseTestCase 
from app import app,db 
from app.models import User
from flask.ext.login import current_user

class TestLogin(BaseTestCase):
     # Ensure that Flask was set up correctly
    # def test_index(self):
    #     response = self.client.get('/login', content_type='html/text')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Sign In', response.data)

    # Ensure login behaves correctly with correct credentials
    # def test_correct_login(self):
    #     response = self.client.post('/login', data=dict(username="Testname", password="password"), follow_redirects=True)
    #     self.assertIn(b'You Were Signin in. Yea!', response.data)

     # Ensure login behaves correctly with incorrect credentials
    # def test_incorrect_login(self):
    #     response = self.client.post('/login', data=dict(username="wrong", password="wrong"), follow_redirects=True)
    #     self.assertIn(b'<strong>Invalid Credentials.</strong> Please try again.', response.data)

     # # Ensure logout behaves correctly
    # def test_logout(self):
    #     response = self.client.post('/login', data=dict(username="Testname", password="password"), follow_redirects=True)
    #     response1 = self.client.get("/logout", headers={"Referer": "/"}, follow_redirects=True)
    #     self.assertIn(b'You were logged out', response1.data)

    # def test_logout_pre(self):
    #     response = self.client.get("/logout", follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Sign In', response.data)

    def test_user_registeration(self):
        with self.client:
            response = self.client.post('/register', data=dict(username='Testname', email='test@test.com', password='password', confirm='password'), follow_redirects=True)
            self.assertIn(b'Congrats on your new account!', response.data)
            self.assertTrue(current_user.name == "Testname")
            self.assertTrue(current_user.is_active())
            user = User.query.filter_by(email='test@test.com').first()
            self.assertTrue(str(user) == '<name> Testname')

    # Ensure errors are thrown during an incorrect user registration
    def test_incorrect_user_registeration(self):
        with self.client:
            response = self.client.post('/register', data=dict(username='M', email='mi',password='pyth', confirm='python'), follow_redirects=True)
            self.assertIn(b'Field must be between 3 and 25 characters long.', response.data)
            self.assertIn(b'Invalid email address.', response.data)
            self.assertIn(b'Field must be between 6 and 40 characters long.', response.data)
            self.assertIn(b'Field must be between 6 and 25 characters long.', response.data)
            self.assertIn(b'Passwords must match.', response.data)


        
