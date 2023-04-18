"""implementations of the class TentLeader"""


class TentLeader:
    """represents data of a zeltlager tentLeader"""

    def __init__(
        self,
        arg_id,
        arg_job,
        arg_lastname,
        arg_firstname,
        arg_street,
        arg_zipcode,
        arg_village,
        arg_phone,
        arg_handy,
        arg_mail,
        arg_birthdate,
        arg_tent,
        arg_team,
        arg_comment,
    ):
        self.identifier = arg_id

        self.job = arg_job

        self.lastname = arg_lastname
        self.firstname = arg_firstname
        self.birthdate = arg_birthdate

        self.street = arg_street
        self.zipcode = arg_zipcode
        self.village = arg_village

        self.phone = arg_phone
        self.handy = arg_handy
        self.mail = arg_mail

        self.tent = arg_tent
        self.team = arg_team
        self.comment = arg_comment

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

    def get_fullname(self):
        """return first + lastname"""
        return self.firstname + " "+self.lastname
