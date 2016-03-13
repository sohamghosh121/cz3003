import pdfkit
from ..pushapis.email_api import EmailAPI


class PMODispatcher:

    """
        Generates PDF report and constructs email message to send to PMO using email API
    """
    PMO_EMAIL = 'ghosh.soham@gmail.com'

    def getEmailContent(self):
        """
            Return email message content
        """
        return 'To PMO, \
            Please find attached the half hourly report update with this email. \
            \
            Sincerely, CZ3003 CMS'

    def getEmergencyEmailContent(self, crisis_dic):
        crisisString = ', '.join(
            ['%s (Level %d)' % (c[0], c[1]) for c in crisis_dic.items()])
        return 'To PMO, \
        There are new crises developing in the following areas:    \
        %s \
        Sincerely,\
        CZ3003 CMS' % crisisString

    def generatePDF(self):
        """
            Generate PDF from html
        """
        pdfkit.from_url('http://localhost:8000/report', 'out.pdf')

    def dispatch(self):
        """
            Dispatch email to PMO using email API
        """
        self.generatePDF()
        EmailAPI().pushUpdate(
            self.PMO_EMAIL, 'Crisis Management System Report', getEmailContent(), attachment='out.pdf')

    def emergencyDispatch(self, crisis_dic):
        """
            Dispatch email to PMO using email API when system suggests that crisis level should be raised
            Input: crisis_dic, a dictionary of district names and corresponding suggested crisis level
        """
        EmailAPI().pushUpdate(
            PMO_EMAIL, 'Crisis Management System Report', getEmergencyEmailContent(crisis_dic))

