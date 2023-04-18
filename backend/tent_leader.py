"""implementations of the class TentLeader"""


from person import Person


class TentLeader(Person):
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

        super().__init__(arg_lastname, arg_firstname, arg_street,
                         arg_zipcode, arg_village, arg_birthdate, arg_phone, arg_mail)

        self.handy = arg_handy

        self.tent = arg_tent
        self.team = arg_team
        self.comment = arg_comment

    def __str__(self):
        ret_str = super().__str__()
        return ret_str
