# -*- coding: utf-8 -*-
"""Tests for multipart emails."""

from __future__ import unicode_literals

from future.tests.base import unittest
import future.backports.email as email
import future.backports.email.mime.multipart
import future.backports.email.parser as parser
from future.builtins import list

class EmailMultiPartTests(unittest.TestCase):
    """Tests for handling multipart email Messages."""

    def test_multipart_serialize_without_boundary(self):
        """Tests that serializing an empty multipart email does not fail."""
        multipart_message = email.mime.multipart.MIMEMultipart()
        self.assertIsNot(multipart_message.as_string(), None)

    def test_multipart_set_boundary_does_not_change_header_type(self):
        """
        Tests that Message.set_boundary() does not cause Python2 errors.
        
        In particular, tests that set_boundary does not cause the type of the
        message headers list to be changed from the future built-in list.
        """
        multipart_message = email.mime.multipart.MIMEMultipart()
        headers_type = type(multipart_message._headers)
        self.assertEqual(headers_type, type(list()))

        boundary = '===============6387699881409002085=='
        multipart_message.set_boundary(boundary)
        headers_type = type(multipart_message._headers)
        self.assertEqual(headers_type, type(list()))

    def test_multipart_newline_boundary(self):
        p = parser.Parser()
        msg = '''MIME-Version: 1.0
Content-Type: multipart/alternative; boundary="ALTERNATIVE_BOUNDARY"
--ALTERNATIVE_BOUNDARY
Content-Type: text/plain

hello
--ALTERNATIVE_BOUNDARY--
'''
        msgobj = p.parsestr(msg)
        assert msgobj.get_payload(0).get_payload() == 'hello'
