"""implementations of the class Participant"""
from src.lib.person import Person


def particpant_object_to_class(arg_p, arg_o):
    """converts dict object to participant object"""

    revisions = []

    revisions.append(arg_p.set_firstname(arg_o["firstname"]))
    arg_p.paid = arg_o["paid"]
    revisions.append(arg_p.set_lastname(arg_o["lastname"]))
    revisions.append(arg_p.set_birthdate(arg_o["birthdate"]))
    revisions.append(arg_p.set_street(arg_o["street"]))
    revisions.append(arg_p.set_zipcode(arg_o["zipcode"]))
    revisions.append(arg_p.set_village(arg_o["village"]))
    revisions.append(arg_p.set_phone(arg_o["phone"]))
    revisions.append(arg_p.set_mail(arg_o["mail"]))
    revisions.append(arg_p.set_emergency_contact(arg_o["emergency_contact"]))
    revisions.append(arg_p.set_emergency_phone(arg_o["emergency_phone"]))
    revisions.append(arg_p.set_is_vegetarian(arg_o["is_vegetarian"]))
    revisions.append(arg_p.set_is_reduced(arg_o["is_reduced"]))
    revisions.append(arg_p.set_is_event_mail(arg_o["is_event_mail"]))
    revisions.append(arg_p.set_friend1(arg_o["friends"][0]))
    revisions.append(arg_p.set_friend2(arg_o["friends"][1]))
    revisions.append(arg_p.set_is_photo_allowed(arg_o["is_photo_allowed"]))
    revisions.append(arg_p.set_other(arg_o["other"]))
    revisions.append(arg_p.set_registered(arg_o["registered"]))
    arg_p.tent = arg_o["tent"]

    revisions = list(filter(lambda x: x != "", revisions))
    return revisions


class Participant(Person):
    """represents data of a zeltlager participant"""
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-public-methods

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
        arg_registered
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
        self.registered = arg_registered

    def __str__(self):
        friends_str = ""
        for friend in self.friends:
            friends_str += friend + ", "

        ret_str = super().__str__()
        if friends_str != "":
            ret_str += ", Zelt: " + friends_str
        return ret_str

    def __string_to_bool(self, arg_val):
        """parse string to bool"""
        return arg_val.lower() in ["true", "1"]

    def set_friends(self, arg_friends):
        """set the frieds of the participant"""
        self.friends = arg_friends

    def get_friend_string(self, index):
        """return friend string by index"""
        if index > 1 or (index + 1) > len(self.friends):
            return ""
        return self.friends[index]

    def set_by_string_prop(self, arg_prop, arg_val):
        """sets property by given property string and returns old value"""
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements

        # name
        if arg_prop == "firstname":
            old_value = self.firstname
            self.firstname = arg_val
        elif arg_prop == "lastname":
            old_value = self.lastname
            self.lastname = arg_val

         # location
        elif arg_prop == "street":
            old_value = self.street
            self.street = arg_val
        elif arg_prop == "zipcode":
            old_value = self.zipcode
            try:
                self.zipcode = int(arg_val)
            except ValueError:
                old_value = "ERROR"
        elif arg_prop == "village":
            old_value = self.village
            self.village = arg_val

        # birthdate
        elif arg_prop == "birthdate":
            old_value = self.birthdate
            self.birthdate = arg_val
        # phone
        elif arg_prop == "phone":
            old_value = self.phone
            self.phone = arg_val
        # mail
        elif arg_prop == "mail":
            old_value = self.mail
            self.mail = arg_val

        # emercency contact
        elif arg_prop == "emergency_contact":
            old_value = self.emergency_contact
            self.emergency_contact = arg_val
        elif arg_prop == "emergency_phone":
            old_value = self.emergency_phone
            self.emergency_phone = arg_val

        # checkboxes
        elif arg_prop == "is_reduced":
            old_value = self.is_reduced
            self.is_reduced = self.__string_to_bool(arg_val)
        elif arg_prop == "is_photo_allowed":
            old_value = self.is_photo_allowed
            self.is_photo_allowed = self.__string_to_bool(arg_val)
        elif arg_prop == "is_vegetarian":
            old_value = self.is_vegetarian
            self.is_vegetarian = self.__string_to_bool(arg_val)
        elif arg_prop == "is_event_mail":
            old_value = self.is_event_mail
            self.is_event_mail = self.__string_to_bool(arg_val)

        # other
        elif arg_prop == "other":
            old_value = self.other
            self.other = arg_val

        # friends
        elif arg_prop == "friend1":
            old_value = self.friends[0]
            self.friends[0] = arg_val
        elif arg_prop == "friend2":
            old_value = self.friends[1]
            self.friends[1] = arg_val

        # registered
        elif arg_prop == "registered":
            old_value = self.registered
            self.registered = arg_val

        else:
            old_value = None

        return old_value

    def set_firstname(self, arg_val):
        """set firstname and return revision string"""
        if self.firstname != arg_val:
            self.firstname = arg_val
            return str(self.identifier) + ";firstname;"+str(self.firstname)
        return ""

    def set_lastname(self, arg_val):
        """set lastname and return revision string"""
        if self.lastname != arg_val:
            self.lastname = arg_val
            return str(self.identifier) + ";lastname;"+str(self.lastname)
        return ""

    def set_birthdate(self, arg_val):
        """set birthdate and return revision string"""
        if self.birthdate != arg_val:
            self.birthdate = arg_val
            return str(self.identifier) + ";birthdate;"+str(self.birthdate)
        return ""

    def set_street(self, arg_val):
        """set street and return revision string"""
        if self.street != arg_val:
            self.street = arg_val
            return str(self.identifier) + ";street;"+str(self.street)
        return ""

    def set_zipcode(self, arg_val):
        """set zipcode and return revision string"""
        if self.zipcode != arg_val:
            self.zipcode = arg_val
            return str(self.identifier) + ";zipcode;"+str(self.zipcode)
        return ""

    def set_village(self, arg_val):
        """set village and return revision string"""
        if self.village != arg_val:
            self.village = arg_val
            return str(self.identifier) + ";village;"+str(self.village)
        return ""

    def set_phone(self, arg_val):
        """set phone and return revision string"""
        if self.phone != arg_val:
            self.phone = arg_val
            return str(self.identifier) + ";phone;"+str(self.phone)
        return ""

    def set_mail(self, arg_val):
        """set mail and return revision string"""
        if self.mail != arg_val:
            self.mail = arg_val
            return str(self.identifier) + ";mail;"+str(self.mail)
        return ""

    def set_emergency_contact(self, arg_val):
        """set emergency_contact and return revision string"""
        if self.emergency_contact != arg_val:
            self.emergency_contact = arg_val
            return str(self.identifier) + ";emergency_contact;"+str(self.emergency_contact)
        return ""

    def set_emergency_phone(self, arg_val):
        """set emergency_phone and return revision string"""
        if self.emergency_phone != arg_val:
            self.emergency_phone = arg_val
            return str(self.identifier) + ";emergency_phone;"+str(self.emergency_phone)
        return ""

    def set_is_vegetarian(self, arg_val):
        """set is_vegetarian and return revision string"""
        if self.is_vegetarian != arg_val:
            self.is_vegetarian = arg_val
            return str(self.identifier) + ";is_vegetarian;"+str(self.is_vegetarian)
        return ""

    def set_is_reduced(self, arg_val):
        """set is_reduced and return revision string"""
        if self.is_reduced != arg_val:
            self.is_reduced = arg_val
            return str(self.identifier) + ";is_reduced;"+str(self.is_reduced)
        return ""

    def set_is_event_mail(self, arg_val):
        """set is_event_mail and return revision string"""
        if self.is_event_mail != arg_val:
            self.is_event_mail = arg_val
            return str(self.identifier) + ";is_event_mail;"+str(self.is_event_mail)
        return ""

    def set_friend1(self, arg_val):
        """set friend1 and return revision string"""
        if self.friends[0] != arg_val:
            self.friends[0] = arg_val
            return str(self.identifier) + ";friend1;"+str(self.friends[0])
        return ""

    def set_friend2(self, arg_val):
        """set friend2 and return revision string"""
        if self.friends[1] != arg_val:
            self.friends[1] = arg_val
            return str(self.identifier) + ";friend2;"+str(self.friends[1])
        return ""

    def set_is_photo_allowed(self, arg_val):
        """set is_photo_allowed and return revision string"""
        if self.is_photo_allowed != arg_val:
            self.is_photo_allowed = arg_val
            return str(self.identifier) + ";is_photo_allowed;"+str(self.is_photo_allowed)
        return ""

    def set_other(self, arg_val):
        """set other and return revision string"""
        if self.other != arg_val:
            self.other = arg_val
            return str(self.identifier) + ";other;"+str(self.other)
        return ""

    def set_registered(self, arg_val):
        """set registered and return revision string"""
        if self.registered != arg_val:
            self.registered = arg_val
            return str(self.identifier) + ";registered;"+str(self.registered)
        return ""
