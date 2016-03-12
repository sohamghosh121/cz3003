"""
    SendGrid API
"""

import sendgrid


class EmailAPI:
    API_KEY = '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'
    client = sendgrid.SendGridClient(API_KEY)

    def pushUpdate(self, email, subject, content):
        self.generatePDF()
        message = sendgrid.Mail()
        message.add_to(email)
        message.set_from('cz3003cms@ntu.edu.sg')
        message.set_subject(subject)
        message.set_html(content)
        message.add_attachment('out.pdf', 'out.pdf')
        self.client.send(message)
