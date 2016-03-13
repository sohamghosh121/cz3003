"""
    SendGrid API
"""

import sendgrid


class EmailAPI:
    API_KEY = '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'
    client = sendgrid.SendGridClient(API_KEY)

    def pushUpdate(self, email, subject, content, attachment=None):
        try:
            message = sendgrid.Mail()
            message.add_to(email)
            message.set_from('cz3003cms@ntu.edu.sg')
            message.set_subject(subject)
            message.set_html(content)
            if attachment:
                message.add_attachment(attachment, attachment)
            self.client.send(message)
            return True
        except Exception, e:
            print e
            return False
