"""functions related to participants"""
import os
import csv
import time
from datetime import datetime
import file_indices as IDX
from helpers import is_paided, parse_yes_no, strip_row
from participants.participant_c import Participant
import pathes as PATH


def check_if_participant_file_valid(arg_input_file):
    """check_if_participant_file_valid"""
    # check number of semicolons
    with open(arg_input_file, newline="", encoding="utf-8") as csvfile:
        for check_row in csvfile:
            cnt_semicolon = check_row.count(";")
            if cnt_semicolon != IDX.ROWS_PARP:
                raise Exception("ERROR at row:" + str(check_row))


def get_paticipant_by_id(arg_participants, arg_id):
    """returns participant by given id"""
    for loc_participant in arg_participants:
        if loc_participant.identifier == arg_id:
            return loc_participant
    return None


def parse_participants_last_year(arg_participants, arg_errors):
    """parses zeltlager participants from input csv file"""
    loc_participants = []

    if not os.path.isfile(PATH.LAST_YEAR):
        arg_errors.append("ERROR: " + PATH.LAST_YEAR + " existiert nicht")
        print("ERROR: " + PATH.LAST_YEAR + " existiert nicht")
        return loc_participants

    with open(PATH.LAST_YEAR, newline="", encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")

        for i, row in enumerate(spamreader):
            if i >= 1:
                strip_row(row)

                loc_lastname = row[1]
                loc_firstname = row[0]

                loc_participants.append(loc_firstname + " " + loc_lastname)

    ret = []
    compare_friends = [p.get_fullname() for p in arg_participants]
    for participant in loc_participants:
        if participant not in compare_friends:
            ret.append(participant)

    return ret


def parse_paid(arg_participants, arg_errors):
    """parse paid participants"""
    if not os.path.isfile(PATH.PAID):
        return arg_participants

    with open(PATH.PAID, encoding="utf8") as paid_file:
        for row in paid_file:
            splitted_row = row.split(";")
            loc_id = int(splitted_row[0].strip())
            loc_is_paid = splitted_row[1].strip()

            loc_participant = get_paticipant_by_id(arg_participants, loc_id)
            if loc_participant is None:
                print("ERROR parse paid: participant not found")
                arg_errors.append(
                    'Teilnehmer mit Id "'
                    + str(loc_id)
                    + '" wurde nicht gefunden. Bezahlt konnte nicht angehackt werden!'
                )
            else:
                loc_participant.paid = is_paided(loc_is_paid)
    return arg_participants


def apply_participants_revisons(arg_participants,  arg_errors):
    """apply_participants_revisons"""
    loc_revisions = []

    if not os.path.isfile(PATH.REVISION):
        arg_errors.append("ERROR: " + PATH.REVISION + " existiert nicht")
        print("ERROR: " + PATH.REVISION + " existiert nicht")
        return arg_participants

    with open(PATH.REVISION, encoding="utf8") as revision_file:
        for row in revision_file:
            if row.strip() == "":
                continue
            splitted_row = row.split(";")

            loc_id = int(splitted_row[0].strip())
            loc_property = splitted_row[1].strip()
            loc_value = splitted_row[2].strip()

            loc_participant = get_paticipant_by_id(arg_participants, loc_id)

            loc_revision = {}
            loc_revision["id"] = loc_id
            loc_revision["property"] = loc_property
            loc_revision["newValue"] = loc_value

            # participant not found
            if loc_participant is None:
                # cereate log string
                loc_revision["isError"] = True
                loc_revision["fullname"] = ""
                loc_revision["oldValue"] = ""
                loc_revision["errorMessage"] = "ID not found"

                loc_revisions.append(loc_revision)

            else:

                loc_old_value = loc_participant.set_by_string_prop(
                    loc_property, loc_value)
                # failed to find property
                if loc_old_value is None:
                    loc_revision["isError"] = True
                    loc_revision["fullname"] = loc_participant.get_fullname()
                    loc_revision["oldValue"] = ""
                    loc_revision["errorMessage"] = "Eigenschaft \"" + \
                        loc_property + "\"existiert nicht"
                # failed to parse property
                elif loc_old_value == "ERROR":
                    loc_revision["isError"] = True
                    loc_revision["fullname"] = loc_participant.get_fullname()
                    loc_revision["oldValue"] = ""
                    loc_revision["errorMessage"] = "Wert \"" + \
                        loc_value + "\"konnte nicht geparsed werden"

                 # revision was sucessfull
                else:
                    loc_revision["isError"] = False
                    loc_revision["fullname"] = loc_participant.get_fullname()
                    loc_revision["oldValue"] = loc_old_value
                    loc_revision["errorMessage"] = loc_value

                loc_revisions.append(loc_revision)

    return arg_participants, loc_revisions


def parse_tent_numbers(arg_participants, arg_errors):
    """parse tent numbers"""
    if not os.path.isfile(PATH.TENT_NUMBERS):
        return arg_participants

    with open(PATH.TENT_NUMBERS, encoding="utf8") as tent_numbers_file:
        for row in tent_numbers_file:
            splitted_row = row.split(";")
            loc_id = int(splitted_row[0].strip())
            loc_tent_number = int(splitted_row[1].strip())

            loc_participant = get_paticipant_by_id(arg_participants, loc_id)
            if loc_participant is None:
                print("ERROR parse tent number: participant not found")
                arg_errors.append(
                    'Teilnehmer mit Id "'
                    + str(loc_id)
                    + '" wurde nicht gefunden. Zeltnummer "'
                    + str(loc_tent_number)
                    + '" konnte nicht zugewiesen werden!'
                )
            else:
                loc_participant.tent = loc_tent_number
    return arg_participants


def parse_participants(arg_errors):
    """parses zeltlager participants from input csv file"""
    loc_participants = []

    if not os.path.isfile(PATH.PARICIPANT):
        arg_errors.append("ERROR: " + PATH.PARICIPANT + " existiert nicht")
        print("ERROR: " + PATH.PARICIPANT + " existiert nicht")
        return loc_participants

    check_if_participant_file_valid(PATH.PARICIPANT)

    with open(PATH.PARICIPANT, newline="", encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")

        for i, row in enumerate(spamreader):
            if i >= 1:
                strip_row(row)

                loc_lastname = row[IDX.PARP_LAST_NAME]
                loc_firstname = row[IDX.PARP_FIRST_NAME]

                # parse zip code
                try:
                    loc_zipcode = int(row[IDX.PARP_ZIP_CODE])
                except:
                    print("ERROR: failed to parse zip coce: i: ", i,
                          loc_firstname, " ", loc_lastname,)
                    raise

                try:
                    # check if birthdate is valid
                    time.mktime(
                        datetime.strptime(row[IDX.PARP_BIRTHDATE], "%Y-%m-%d")
                        .date()
                        .timetuple())

                except:
                    print("failed to parse birthdate: i: ",
                          i, loc_firstname, " ", loc_lastname)
                    raise
                loc_birthdate = row[IDX.PARP_BIRTHDATE]

                loc_participant = Participant(
                    int(row[IDX.PARP_ID]),
                    # will be overwritten by parse_paid()
                    is_paided("false"),
                    loc_lastname,
                    loc_firstname,
                    row[IDX.PARP_STREET],
                    loc_zipcode,
                    row[IDX.PARP_VILLAGE],
                    loc_birthdate,
                    row[IDX.PARP_PHONE],
                    row[IDX.PARP_MAIL],
                    row[IDX.PARP_EMERCENCY_CONTACT],
                    row[IDX.PARP_EMERCENCY_PHONE],
                    parse_yes_no(row[IDX.PARP_REDUCED]),
                    parse_yes_no(row[IDX.PARP_PHOTO_ALLOWED]),
                    parse_yes_no(row[IDX.PARP_VEGETARIAN]),
                    parse_yes_no(row[IDX.PARP_NEWSLETTER]),
                    row[IDX.PARP_OTHER],
                    9999,  # will be overwritten by parse_tent_numbers()
                    row[IDX.PARP_REGISTER_DATE]
                )

                loc_participant.set_friends(
                    [row[IDX.PARP_FRIEND1], row[IDX.PARP_FRIEND2]]
                )

                loc_participants.append(loc_participant)

        print("parsed input file: ", PATH.PARICIPANT)
        loc_participants, loc_revisions = apply_participants_revisons(
            loc_participants,   arg_errors)

        loc_participants = parse_tent_numbers(loc_participants,  arg_errors)
        loc_participants = parse_paid(loc_participants,  arg_errors)

    return loc_participants, loc_revisions
