"""implementations of the class Participant"""


class Person:
    """represents data of a zeltlager participant"""
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments

    def __init__(
        self,
        arg_lastname,
        arg_firstname,
        arg_street,
        arg_zipcode,
        arg_village,
        arg_birthdate,
        arg_phone,
        arg_mail,
    ):
        self.lastname = arg_lastname
        self.firstname = arg_firstname
        self.birthdate = arg_birthdate

        self.street = arg_street
        self.zipcode = arg_zipcode
        self.village = arg_village

        self.phone = arg_phone
        self.mail = arg_mail

    def __str__(self):

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

        return ret_str

    def get_name(self):
        """returns lastname and firstname"""
        return self.lastname, self.firstname

    def get_fullname(self):
        """return first + lastname"""
        return self.firstname + " "+self.lastname
