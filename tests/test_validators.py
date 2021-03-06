from __future__ import unicode_literals

from django.core.validators import ValidationError
from django.test import TestCase

from oauth2_provider.settings import oauth2_settings
from oauth2_provider.validators import validate_uris


class TestValidators(TestCase):
    def test_validate_good_uris(self):
        good_uris = "http://example.com/ http://example.org/?key=val http://example"
        # Check ValidationError not thrown
        validate_uris(good_uris)

    def test_validate_custom_uri_scheme(self):
        oauth2_settings.ALLOWED_REDIRECT_URI_SCHEMES = ["my-scheme", "http"]
        good_uris = "my-scheme://example.com http://example.com"
        # Check ValidationError not thrown
        validate_uris(good_uris)

    def test_validate_whitespace_separators(self):
        # Check that whitespace can be used as a separator
        good_uris = "http://example\r\nhttp://example\thttp://example"
        # Check ValidationError not thrown
        validate_uris(good_uris)

    def test_validate_bad_uris(self):
        bad_uri = "http://example.com/#fragment"
        self.assertRaises(ValidationError, validate_uris, bad_uri)
        bad_uri = "http:/example.com"
        self.assertRaises(ValidationError, validate_uris, bad_uri)
        # Bad IPv6 URL, urlparse behaves differently for these
        bad_uri = "https://[\"><script>alert()</script>"
        self.assertRaises(ValidationError, validate_uris, bad_uri)
        bad_uri = "my-scheme://example.com"
        self.assertRaises(ValidationError, validate_uris, bad_uri)
        bad_uri = "sdklfsjlfjljdflksjlkfjsdkl"
        self.assertRaises(ValidationError, validate_uris, bad_uri)
        bad_uri = "     "
        self.assertRaises(ValidationError, validate_uris, bad_uri)
        bad_uri = ""
        self.assertRaises(ValidationError, validate_uris, bad_uri)
