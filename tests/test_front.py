import unittest 
from base import BaseTestCase 
from app import app,db 

class TestFrontPage(BaseTestCase):

	def test_index_loads(self):
		response = self.client.get("/", follow_redirects=True)
		assert response.status_code == 200
		assert "Technologies I know how to use" in response.data