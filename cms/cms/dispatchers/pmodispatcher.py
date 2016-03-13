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
            PMO_EMAIL, 'Crisis Management System Report', getEmailContent())
