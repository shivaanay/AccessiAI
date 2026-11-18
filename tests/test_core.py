import unittest
from app.recommendations import explain_violation
from app.scanner import validate_public_url

class RecommendationTests(unittest.TestCase):
    def test_known_rule_has_specific_guidance(self):
        result = explain_violation({'id': 'image-alt'})
        self.assertIn('alternative text', result['title'].lower())
        self.assertTrue(result['recommendation'])

    def test_unknown_rule_has_fallback_guidance(self):
        result = explain_violation({'id': 'new-rule', 'help': 'Review this item'})
        self.assertEqual(result['title'], 'Review this accessibility issue')

class URLValidationTests(unittest.TestCase):
    def test_localhost_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_public_url('http://localhost:5000')

    def test_private_ipv4_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_public_url('http://192.168.1.10')

    def test_credentials_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_public_url('https://user:pass@example.com')

    def test_unsupported_scheme_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_public_url('file:///etc/passwd')

if __name__ == '__main__':
    unittest.main()
