import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserProfile:
    def __init__(self, user_id, name, email, preferences=None):
        """
        Initialize the UserProfile with basic user information.

        :param user_id: Unique user identifier
        :param name: Name of the user
        :param email: Email address of the user
        :param preferences: Dictionary of user preferences (optional)
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.preferences = preferences or {}
        logger.info(f"UserProfile initialized for user {self.name} ({self.user_id})")

    def update_profile(self, name=None, email=None, preferences=None):
        """
        Update the user's profile information.

        :param name: New name of the user (optional)
        :param email: New email address of the user (optional)
        :param preferences: New dictionary of user preferences (optional)
        """
        if name:
            self.name = name
            logger.info(f"Updated name to {name}")
        if email:
            self.email = email
            logger.info(f"Updated email to {email}")
        if preferences:
            self.preferences.update(preferences)
            logger.info(f"Updated preferences: {preferences}")

    def get_profile(self):
        """
        Get the user's profile information.

        :return: Dictionary containing the user's profile information
        """
        profile_info = {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'preferences': self.preferences
        }
        logger.info(f"Retrieved profile information for user {self.user_id}")
        return profile_info
