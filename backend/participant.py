"""implementations of the class Participant"""


class Participant:
    """represents data of a zeltlager participant"""

    def __init__(
        self,
        arg_id,
        arg_paided,
        arg_lastname,
        arg_firstname,
        arg_street,
        arg_zipcode,
        arg_village,
        arg_birthdate,
        arg_phone,
        arg_mail,
        arg_emergency_contact,
        arg_emergency_phone,
        arg_is_reduced,
        arg_is_photo_allowed,
        arg_is_afe,
        arg_is_event_mail,
        arg_other,
        arg_tent,
    ):
        self.identifier = arg_id

        self.paid = arg_paided

        self.lastname = arg_lastname
        self.firstname = arg_firstname
        self.birthdate = arg_birthdate

        self.street = arg_street
        self.zipcode = arg_zipcode
        self.village = arg_village

        self.phone = arg_phone
        self.mail = arg_mail

        self.emergency_contact = arg_emergency_contact
        self.emergency_phone = arg_emergency_phone

        self.is_afe = arg_is_afe
        self.is_reduced = arg_is_reduced
        self.is_event_mail = arg_is_event_mail

        self.friends = []

        self.is_photo_allowed = arg_is_photo_allowed

        self.other = arg_other
        self.tent = arg_tent

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

    def get_fullname(self):
        """return first + lastname"""
        return self.firstname + " "+self.lastname

    def get_friend_string(self, index):
        """return friend string by index"""
        if index > 1 or (index + 1) > len(self.friends):
            return ""
        return self.friends[index]
