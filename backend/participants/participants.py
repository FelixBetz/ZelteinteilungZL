"""functions related to participants"""
import os
import csv
import file_indices as IDX
from helpers import is_paided, strip_row


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


def parse_participants_last_year(arg_file_name, arg_participants):
    """parses zeltlager participants from input csv file"""

    loc_participants = []
    loc_errors = []

    if not os.path.isfile(arg_file_name):
        loc_errors.append("ERROR: " + arg_file_name + " existiert nicht")
        print("ERROR: " + arg_file_name + " existiert nicht")
        return loc_participants

    with open(arg_file_name, newline="", encoding="utf-8") as csvfile:
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

    return ret, loc_errors


def parse_paid(arg_participants, arg_path):
    """parse paid participants"""
    loc_errors = []

    if not os.path.isfile(arg_path):
        return arg_participants

    with open(arg_path, encoding="utf8") as paid_file:
        for row in paid_file:
            splitted_row = row.split(";")
            loc_id = int(splitted_row[0].strip())
            loc_is_paid = splitted_row[1].strip()

            loc_participant = get_paticipant_by_id(arg_participants, loc_id)
            if loc_participant is None:
                print("ERROR parse paid: participant not found")
                loc_errors.append(
                    'Teilnehmer mit Id "'
                    + str(loc_id)
                    + '" wurde nicht gefunden. Bezahlt konnte nicht angehackt werden!'
                )
            else:
                loc_participant.paid = is_paided(loc_is_paid)
    return arg_participants, loc_errors
