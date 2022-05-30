"""implementations of the class Participant"""


class Participant:
    """represents data of a zeltlager participant"""

    def __init__(
        self,
        arg_lastname,
        arg_firstname,
        arg_zipcode,
        arg_village,
        arg_birthdate,
    ):
        self.lastname = arg_lastname
        self.firstname = arg_firstname
        self.zipcode = arg_zipcode
        self.village = arg_village
        self.birthdate = arg_birthdate
        self.friends = []

    def __str__(self):
        friends_str = ""
        for friend in self.friends:
            friends_str += friend + ", "

        ret_str = (
            self.firstname
            + " "
            + self.lastname
            + ", "
            + str(self.zipcode)
            + " "
            + self.village
            + ", "
            + str(self.birthdate)
        )

        if friends_str != "":
            ret_str += ", Zelt: " + friends_str
        return ret_str

    def set_friends(self, arg_friends):
        """set the frieds of the participant"""
        self.friends = arg_friends

    def get_name(self):
        """returns lastname and firstname"""
        return self.lastname, self.firstname
