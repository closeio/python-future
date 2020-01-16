# -*- coding: utf-8 -*-
"""Tests for email generation."""

from __future__ import unicode_literals

from future.backports.email.charset import BASE64, QP, add_charset
from future.backports.email.header import Header
from future.backports.email.mime.multipart import MIMEMultipart
from future.backports.email.mime.text import MIMEText
from future.backports.email.utils import formatdate
from future.tests.base import unittest


class EmailGenerationTests(unittest.TestCase):
    def test_email_with_unicode_in_b64(self):
        add_charset('utf-8', BASE64, BASE64, 'utf-8')

        msg = MIMEMultipart()
        alternative = MIMEMultipart('alternative')
        alternative.attach(MIMEText('Plain content with Únicødê with х', _subtype='plain', _charset='utf-8'))
        alternative.attach(MIMEText('HTML content with Únicødê with х', _subtype='html', _charset='utf-8'))
        msg.attach(alternative)

        msg['Subject'] = Header('Subject with Únicødê with х', 'utf-8')
        msg['From'] = 'sender@test.com'
        msg['To'] = 'recipient@test.com'
        msg['Date'] = formatdate(None, localtime=True)
        msg['Message-ID'] = Header('anIdWithÚnicødêForThisEmail', 'utf-8')

        msg_lines = msg.as_string().split('\n')
        self.assertEqual(msg_lines[2], 'Subject: =?utf-8?b?U3ViamVjdCB3aXRoIMOabmljw7hkw6ogd2l0aCDRhQ==?=')
        self.assertEqual(msg_lines[6], 'Message-ID: =?utf-8?b?YW5JZFdpdGjDmm5pY8O4ZMOqRm9yVGhpc0VtYWls?=')
        self.assertEqual(msg_lines[17], 'UGxhaW4gY29udGVudCB3aXRoIMOabmljw7hkw6ogd2l0aCDRhQ==')
        self.assertEqual(msg_lines[24], 'SFRNTCBjb250ZW50IHdpdGggw5puaWPDuGTDqiB3aXRoINGF')

    def test_email_with_unicode_in_qp(self):
        add_charset('utf-8', QP, QP, 'utf-8')

        msg = MIMEMultipart()
        alternative = MIMEMultipart('alternative')
        alternative.attach(MIMEText('Plain content with Únicødê with х', _subtype='plain', _charset='utf-8'))
        alternative.attach(MIMEText('HTML content with Únicødê with х', _subtype='html', _charset='utf-8'))
        msg.attach(alternative)

        msg['Subject'] = Header('Subject with Únicødê with х', 'utf-8')
        msg['From'] = 'sender@test.com'
        msg['To'] = 'recipient@test.com'
        msg['Date'] = formatdate(None, localtime=True)
        msg['Message-ID'] = Header('anIdWithÚnicødêForThisEmail', 'utf-8')

        msg_lines = msg.as_string().split('\n')
        self.assertEqual(msg_lines[2], 'Subject: =?utf-8?q?Subject_with_=C3=9Anic=C3=B8d=C3=AA_with_=D1=85?=')
        self.assertEqual(msg_lines[6], 'Message-ID: =?utf-8?q?anIdWith=C3=9Anic=C3=B8d=C3=AAForThisEmail?=')
        self.assertEqual(msg_lines[17], 'Plain content with =C3=9Anic=C3=B8d=C3=AA with =D1=85')
        self.assertEqual(msg_lines[23], 'HTML content with =C3=9Anic=C3=B8d=C3=AA with =D1=85')
