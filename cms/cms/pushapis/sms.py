"""
    SMS API
"""
from twilio.rest import TwilioRestClient

class TwilioAPI:
	def sendMessage(self, message):
		ACCOUNT_SID = "AC70d34cdf60361f90def6d53941f7e50b"
		AUTH_TOKEN = "7d7c563de4b9c7eb0faf618dddd74e49"
		client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
		client.messages.create(
			to = "+6597741853",
			from_ = "+15403393178",
			body = message
		)

if __name__ == '__main__':
	tw = TwilioAPI()
	tw.sendMessage('Test')

