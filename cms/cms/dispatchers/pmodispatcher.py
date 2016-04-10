"""
    Module that sends email to Prime Minister's Office
"""
import pdfkit
from ..pushapis.email_api import EmailAPI
from time import strftime
import datetime


class PMODispatcher:

    """
        Generates PDF report and constructs email message to send to PMO using email API
    """
    PMO_EMAIL = 'ghosh.soham@gmail.com'

    def get_email_content(self):
        """
            Return email message content
        """
        return 'To PMO, \
            Please find attached the half hourly report update with this email. \
            \
            Sincerely, CZ3003 CMS'

    def get_emergency_email_content(self, crisis_dic):
        crisis_string = ', '.join(
            ['%s (Level %d)' % (c[0], c[1]) for c in crisis_dic.items()])
        return 'To PMO, \
        There are new crises developing in the following areas:    \
        %s \
        Sincerely,\
        CZ3003 CMS' % crisis_string

    def generate_PDF(self):
        """
            Generate PDF from html
        """
        pdfkit.from_url('http://localhost:8000/report', 'report.pdf')

    def dispatch(self):
        """
            Dispatch email to PMO using email API
        """
        self.generate_PDF()
        subject = 'Crisis Management System Report (%s)' % (
            datetime.datetime.now().strftime('%m/%d %H:%M'))
        EmailAPI().push_update(
            self.PMO_EMAIL, subject, self.get_email_content(), attachment='report.pdf')

    def emergency_dispatch(self, crisis_dic):
        """
            Dispatch email to PMO using email API when system suggests that crisis level should be raised
            Input: crisis_dic, a dictionary of district names and corresponding suggested crisis level
        """
        EmailAPI().push_update(
            self.PMO_EMAIL, 'Crisis Management System Alert', self.get_emergency_email_content(crisis_dic))
