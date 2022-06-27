"""implementations of the class Participant"""


class Participant:
    """represents data of a zeltlager participant"""

    def __init__(
        self,
        arg_id,
        arg_lastname,
        arg_firstname,
        arg_zipcode,
        arg_village,
        arg_birthdate,
    ):
        self.identifier = arg_id
        self.firstname = arg_firstname
        self.lastname = arg_lastname
        self.birthdate = arg_birthdate

        self.address = "todo street"
        self.zipcode = arg_zipcode
        self.village = arg_village

        self.mail = "test@web.de"
        self.phone = "07392/17792"

        self.emergency_contact = "Max Mustermann"
        self.emergency_phone = "todo"

        self.friends = []

        self.is_reduced = False
        self.is_photo_allowed = False
        self.is_afe = False
        self.is_event_mail = False

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
