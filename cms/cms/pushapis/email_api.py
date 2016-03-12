"""
    SendGrid API
"""

import sendgrid
import pdfkit

class EmailAPI:
    API_KEY = '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'
    client = sendgrid.SendGridClient(API_KEY)

    def generatePDF(self):
        pdfkit.from_url('http://localhost:3000/report/report.html', 'out.pdf')

    def pushUpdate(self, subject, message):
        self.generatePDF()
        message = sendgrid.Mail()
        message.add_to("phamvutuan10@gmail.com")
        message.set_from("barkatthetree@gmail.com")
        message.set_subject(subject)
        message.set_html(message)
        message.add_attachment('out.pdf','out.pdf')
        self.client.send(message)

# if __name__ == '__main__':
email = EmailAPI()
email.pushUpdate("Test pdf","Hello World!")

    

