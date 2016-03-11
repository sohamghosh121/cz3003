"""
    SendGrid API
"""

import sendgrid


class EmailAPI:
    API_KEY = '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'
    client = sendgrid.SendGridClient(API_KEY)

    def pushUpdate(self, subject, message):
        message = sendgrid.Mail()
        message.add_to("ghosh.soham@gmail.com")
        message.set_from("barkatthetree@gmail.com")
        message.set_subject(subject)
        message.set_html(message)
        self.client.send(message)
