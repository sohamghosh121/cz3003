import pdfkit
from ..pushapis.email_api import EmailAPI


class PMODispatcher:
    PMO_EMAIL = 'ghosh.soham@gmail.com'

    def getEmailContent(self):
        return 'To PMO, \
            Please find attached the half hourly report update with this email. \
            \
            Sincerely, CZ3003 CMS'

    def generatePDF(self):
        pdfkit.from_url('http://localhost:8000/report/report.html', 'out.pdf')

    def dispatch(self):
        self.generatePDF()
        EmailAPI().pushUpdate(
            PMO_EMAIL, 'Crisis Management System Report', getEmailContent())
