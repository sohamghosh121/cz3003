from ..pushapis.fb import FacebookAPI
from ..pushapis.twitter import TwitterAPI


class SocialMediaDispatcher:

    """
        Dispatcher for public information to Social Media platforms
    """

    def __init__(self, crisisUpdate):
        """
            Initiate class with crisis update log object
        """
        self.update = crisisUpdate

    def constructMessage(self):
        """
            Construct message to update public based on crisis update
        """
        return 'Crisis level in %s has been changed to Level %d. Please take care.' % (self.update.district, self.update.new_crisis)

    def dispatch(self):
        """
                Construct update message and dispatch to social media platforms
        """
        message = constructMessage()
        FacebookAPI().pushUpdate(message)
        TwitterAPI().pushUpdate(message)
        pass
