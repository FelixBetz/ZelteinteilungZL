"""implementations of the class Participant"""
from person import Person


class Participant(Person):
    """represents data of a zeltlager participant"""
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments

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
        arg_is_vegetarian,
        arg_is_event_mail,
        arg_other,
        arg_tent,
    ):
        self.identifier = arg_id

        self.paid = arg_paided

        super().__init__(arg_lastname, arg_firstname, arg_street,
                         arg_zipcode, arg_village, arg_birthdate, arg_phone, arg_mail)

        self.emergency_contact = arg_emergency_contact
        self.emergency_phone = arg_emergency_phone

        self.is_vegetarian = arg_is_vegetarian
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

        ret_str = super().__str__()
        if friends_str != "":
            ret_str += ", Zelt: " + friends_str
        return ret_str

    def set_friends(self, arg_friends):
        """set the frieds of the participant"""
        self.friends = arg_friends

    def get_friend_string(self, index):
        """return friend string by index"""
        if index > 1 or (index + 1) > len(self.friends):
            return ""
        return self.friends[index]
