from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    This class generates tokens for user account activation.

    It extends PasswordResetTokenGenerator to create tokens that can be used
    to activate user accounts. Tokens are based on the user's primary key,
    the current timestamp, and the user's active status.
    """

    def _make_hash_value(self, user: User, timestamp: int) -> str:
        """
        Creates a hash value for the token.

        Args:
            user (User): The user for whom the token is being generated.
            timestamp (int): The current time in seconds since the epoch.

        Returns:
            str: A string used to create the token hash.
        """
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()
