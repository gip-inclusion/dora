from unittest import TestCase

from django.core.exceptions import ValidationError
from django.utils.html import escape

from dora.core.emails import sanitize_user_input_injected_in_email


class EmailSanitizerTest(TestCase):
    def test_safe_content_passes(self):
        safe_inputs = [
            "Hello world!",
            "Visit us at #SERVICE_ADDRESS#",
            "Contact support@example.com",
            "Price: €50 < €100",
            "I love onigiri and ongoing projects",
            "Temperature: 20°C",
        ]

        for safe_input in safe_inputs:
            result = sanitize_user_input_injected_in_email(safe_input)
            expected = escape(safe_input)
            self.assertEqual(result, expected)

    def test_template_injection_blocked(self):
        dangerous_inputs = [
            "{{settings.SECRET_KEY}}",
            "{{ settings.DEBUG }}",
            "{ { settings.SECRET_KEY } }",
            "{%load static%}",
            "{% for item in settings %}{{item}}{% endfor %}",
        ]

        for dangerous_input in dangerous_inputs:
            with self.assertRaises(ValidationError) as cm:
                sanitize_user_input_injected_in_email(dangerous_input)
                self.assertTrue(
                    any(
                        dangerous_part in str(cm.exception)
                        for dangerous_part in [
                            dangerous_input,
                            "{{item}}",
                            "{{ item }}",
                        ]
                    ),
                    f"Expected dangerous content detection for: {dangerous_input}, got: {str(cm.exception)}",
                )

    def test_xss_attempts_blocked(self):
        xss_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('test')",
            "onclick=alert('xss')",
            "onload=steal()",
            "${alert('xss')}",
            "data:text/html,<script>alert('xss')</script>",
        ]

        for xss_input in xss_inputs:
            with self.assertRaises(ValidationError):
                sanitize_user_input_injected_in_email(xss_input)

    def test_length_validation(self):
        normal_text = "a" * 999
        result = sanitize_user_input_injected_in_email(normal_text)
        self.assertEqual(result, normal_text)

        too_long = "a" * 1001
        with self.assertRaises(ValidationError) as cm:
            sanitize_user_input_injected_in_email(too_long)
        self.assertIn("Message trop long", str(cm.exception))

    def test_empty_input(self):
        self.assertEqual(sanitize_user_input_injected_in_email(""), "")
        self.assertEqual(sanitize_user_input_injected_in_email(None), "")

    def test_html_escaping(self):
        html_input = "Hello <b>world</b> & friends"
        expected = "Hello &lt;b&gt;world&lt;/b&gt; &amp; friends"
        result = sanitize_user_input_injected_in_email(html_input)
        self.assertEqual(result, expected)

    def test_mixed_legitimate_and_dangerous(self):
        mixed_inputs = [
            "Hello! Visit us at {{settings.SECRET_KEY}} #SERVICE_ADDRESS#",
            "Welcome <script>alert('xss')</script> to our platform!",
            "Normal text ${document.cookie} more text",
        ]

        for mixed_input in mixed_inputs:
            with self.assertRaises(ValidationError):
                sanitize_user_input_injected_in_email(mixed_input)
