from random import randrange
import random
import string
import names


class Generator:

    def __init__(self):
        pass



    def get_email(self):
        """
        returns a random email adress.
        This email adress is bogus and cannot be accessed.
        """
        if hasattr(self, 'email'):
            return self.email

        tlds = [".com", ".co.uk", ".eu", ".ch", ".org"]
        self.email = self.get_random_alphabetical_string(randrange(3, 10)) + "@" + self.get_random_alphabetical_string(
            randrange(3, 10)) + tlds[randrange(0, len(tlds))]
	return self.email
