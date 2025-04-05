from django.test import TestCase
from django.urls import reverse
import json

class LiveNewsTests(TestCase):
    
    def test_valid_query(self):
        """Test that a valid query returns an answer."""
        response = self.client.post(reverse('query'), json.dumps({"query": "news"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn("answer", data)
    
    def test_no_query(self):
        """Test that a missing query returns an error."""
        response = self.client.post(reverse('query'), json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)
    
    def test_no_results(self):
        """Test that no results return an error."""
        response = self.client.post(reverse('query'), json.dumps({"query": "non-existent news"}), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertIn("error", data)
