"""main file of ZelteinteilungZL"""

import time
import csv
import os

from datetime import datetime
import inspect
import json
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from config import Config
from maps import generate_maps
from participant import Participant
from tent_leader import TentLeader

from file_indices import IDX_PARP_FIRST_NAME, IDX_PARP_LAST_NAME, IDX_PARP_STREET,\
    IDX_PARP_ZIP_CODE, IDX_PARP_VILLAGE,   IDX_PARP_MAIL, IDX_PARP_BIRTHDATE,\
    IDX_PARP_PHONE, IDX_PARP_EMERCENCY_CONTACT, IDX_PARP_EMERCENCY_PHONE,\
    IDX_PARP_REDUCED, IDX_PARP_VEGETARIAN, IDX_PARP_NEWSLETTER, IDX_PARP_FRIEND1,\
    IDX_PARP_FRIEND2, IDX_PARP_OTHER, IDX_PARP_PHOTO_ALLOWED, IDX_PARP_ID, \
    IDX_LEAD_JOB, IDX_LEAD_LAST_NAME, IDX_LEAD_FIRST_NAME, IDX_LEAD_STREET,\
    IDX_LEAD_ZIP_CODE, IDX_LEAD_VILLAGE, IDX_LEAD_PHONE, IDX_LEAD_HANDY,\
    IDX_LEAD_MAIL, IDX_LEAD_BIRTHDATE, IDX_LEAD_TENT, IDX_LEAD_TEAM, IDX_LEAD_COMMENT

INPUT_FILE_PATH = r"..\\input\\"
INPUT_FILE_NAME = "2023_teilnehmer_input.csv"
INPUT_TENT_LEADER_FILE_NAME = "2023_leitungsteam_anfrage.csv"
INPUT_REVISION_FILE_NAME = "revisions.txt"
INPUT_TENT_NUMBERS_FILE_NAME = "tent_numbers.txt"
INPUT_PAID_FILE_NAME = "paid.txt"
INPUT_CONFIG_FILE_NAME = "config.txt"

INPUT_PARICIPANT_PATH = INPUT_FILE_PATH + INPUT_FILE_NAME
INPUT_TENT_LEADER_PATH = INPUT_FILE_PATH + INPUT_TENT_LEADER_FILE_NAME
INPUT_REVISION_PATH = INPUT_FILE_PATH + INPUT_REVISION_FILE_NAME
INPUT_TENT_NUMBERS_PATH = INPUT_FILE_PATH + INPUT_TENT_NUMBERS_FILE_NAME
INPUT_PAID_PATH = INPUT_FILE_PATH + INPUT_PAID_FILE_NAME
INPUT_CONFIG_PATH = INPUT_FILE_PATH + INPUT_CONFIG_FILE_NAME

tent_leaders = []
participants_d = []
configs_d = Config(INPUT_CONFIG_PATH)

error_logs = []
revison_logs = []

app = Flask(__name__)
cors = CORS(app)

app.config["MAPS_OUTPUT"] = "output_maps"


def strip_row(arg_row):
    """strip_row"""
    for i, col in enumerate(arg_row):
        arg_row[i] = col.replace('"', "").strip()


def parse_yes_no(arg_string):
    """parses formular ja/zugestimmt to boolean"""
    arg_string = arg_string.strip().lower()
    if arg_string in ("ja", "zugestimmt", "vegetarisch", "ermäßigt", "erlaubt"):
        return True
    return False


def bool_to_tex_yes_no(arg_bool):
    """parse bool to 'ja' or 'nein' string"""
    if arg_bool:
        return "ja"
    return "nein"


def bool_to_text_zugestimmt(arg_bool):
    """parse bool to 'zugestimmt' or 'nein' nicht zugestimmt"""
    if arg_bool:
        return "zugestimmt"
    return "nicht zugestimmt"


def is_paided(arg_paided):
    """is paided"""
    if arg_paided in ["true", "True"]:
        return True
    return False


def check_if_participant_file_valid(arg_input_file):
    """check_if_participant_file_valid"""
    # check number of semicolons
    with open(arg_input_file, newline="", encoding="utf-8") as csvfile:
        for check_row in csvfile:
            cnt_semicolon = check_row.count(";")
            if cnt_semicolon != 24:
                raise Exception("ERROR at row:" + str(check_row))


def save_data(arg_participants, arg_tent_leaders, arg_revisions):
    """save participants tent numbers, revisions, paid"""
    # save tent numbers
    tent_numbers = [{"id": p.identifier, "tent": p.tent}
                    for p in arg_participants]
    with open(INPUT_TENT_NUMBERS_PATH, "w", encoding="utf-8") as tent_number_file:
        for number in tent_numbers:
            if number["tent"] != 9999:
                tent_number_file.write(
                    str(number["id"]) + ";" + str(number["tent"]) + "\n"
                )

    # save paid
    paid_obj = [{"id": p.identifier, "paid": p.paid} for p in arg_participants]

    with open(INPUT_PAID_PATH, "w", encoding="utf-8") as paid_file:
        for obj in paid_obj:
            if obj["paid"] is True:
                paid_file.write(str(obj["id"]) + ";" + str(obj["paid"]) + "\n")

    # save revisions todo

    with open(INPUT_REVISION_PATH, "a", encoding="utf-8") as revision_file:
        for revision in arg_revisions:
            revision_file.write(revision + "\n")

    arg_participants = parse_participants(INPUT_PARICIPANT_PATH)
    arg_tent_leaders = parse_tent_leader(INPUT_TENT_LEADER_PATH)

    return arg_participants, arg_tent_leaders


def parse_tent_numbers(arg_participants):
    """parse tent numbers"""
    if not os.path.isfile(INPUT_TENT_NUMBERS_PATH):
        return arg_participants

    with open(INPUT_TENT_NUMBERS_PATH, encoding="utf8") as tent_numbers_file:
        for row in tent_numbers_file:
            splitted_row = row.split(";")
            loc_id = int(splitted_row[0].strip())
            loc_tent_number = int(splitted_row[1].strip())

            loc_participant = get_paticipant_by_id(arg_participants, loc_id)
            if loc_participant is None:
                print("ERROR parse tent number: participant not found")
                error_logs.append(
                    'Teilnehmer mit Id "'
                    + str(loc_id)
                    + '" wurde nicht gefunden. Zeltnummer "'
                    + str(loc_tent_number)
                    + '" konnte nicht zugewiesen werden!'
                )
            else:
                loc_participant.tent = loc_tent_number
    return arg_participants


def parse_paid(arg_participants):
    """parse paid participants"""
    if not os.path.isfile(INPUT_PAID_PATH):
        return arg_participants

    with open(INPUT_PAID_PATH, encoding="utf8") as paid_file:
        for row in paid_file:
            splitted_row = row.split(";")
            loc_id = int(splitted_row[0].strip())
            loc_is_paid = splitted_row[1].strip()

            loc_participant = get_paticipant_by_id(arg_participants, loc_id)
            if loc_participant is None:
                print("ERROR parse paid: participant not found")
                error_logs.append(
                    'Teilnehmer mit Id "'
                    + str(loc_id)
                    + '" wurde nicht gefunden. Bezahlt konnte nicht angehackt werden!'
                )
            else:
                loc_participant.paid = is_paided(loc_is_paid)
    return arg_participants


def parse_participants(arg_file_name):
    """parses zeltlager participants from input csv file"""

    error_logs.clear()
    loc_participants = []

    if not os.path.isfile(arg_file_name):
        error_logs.append("ERROR: " + arg_file_name + " existiert nicht")
        print("ERROR: " + arg_file_name + " existiert nicht")
        return loc_participants

    check_if_participant_file_valid(arg_file_name)

    with open(arg_file_name, newline="", encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")

        for i, row in enumerate(spamreader):
            if i >= 1:
                strip_row(row)

                loc_lastname = row[IDX_PARP_LAST_NAME]
                loc_firstname = row[IDX_PARP_FIRST_NAME]

                # parse zip code
                try:
                    loc_zipcode = int(row[IDX_PARP_ZIP_CODE])
                except:
                    print(
                        "ERROR: failed to parse zip coce: i: ",
                        i,
                        loc_firstname,
                        " ",
                        loc_lastname,
                    )
                    raise

                try:
                    loc_time_string = datetime.strptime(
                        row[IDX_PARP_BIRTHDATE], "%Y-%m-%d"
                    ).date()
                    loc_tuple = loc_time_string.timetuple()
                    timestamp = time.mktime(loc_tuple)
                    loc_birthdate = timestamp

                except:
                    print(
                        "failed to parse birthdate: i: ",
                        i,
                        loc_firstname,
                        " ",
                        loc_lastname,
                    )
                    raise
                loc_birthdate = row[IDX_PARP_BIRTHDATE]

                loc_participant = Participant(
                    int(row[IDX_PARP_ID]),
                    # will be overwritten by parse_paid()
                    is_paided("false"),
                    loc_lastname,
                    loc_firstname,
                    row[IDX_PARP_STREET],
                    loc_zipcode,
                    row[IDX_PARP_VILLAGE],
                    loc_birthdate,
                    row[IDX_PARP_PHONE],
                    row[IDX_PARP_MAIL],
                    row[IDX_PARP_EMERCENCY_CONTACT],
                    row[IDX_PARP_EMERCENCY_PHONE],
                    parse_yes_no(row[IDX_PARP_REDUCED]),
                    parse_yes_no(row[IDX_PARP_PHOTO_ALLOWED]),
                    parse_yes_no(row[IDX_PARP_VEGETARIAN]),
                    parse_yes_no(row[IDX_PARP_NEWSLETTER]),
                    row[IDX_PARP_OTHER],
                    9999,  # will be overwritten by parse_tent_numbers()
                )

                loc_participant.set_friends(
                    [row[IDX_PARP_FRIEND1], row[IDX_PARP_FRIEND2]]
                )

                loc_participants.append(loc_participant)

        print("parsed input file: ", arg_file_name)
        loc_participants = apply_participants_revisons(loc_participants)
        loc_participants = parse_tent_numbers(loc_participants)
        loc_participants = parse_paid(loc_participants)

    return loc_participants


def parse_tent_leader(arg_file_name):
    """parses zeltlager tent leader from input csv file"""

    loc_tent_leaders = []

    if not os.path.isfile(INPUT_TENT_LEADER_PATH):
        error_logs.append(
            "ERROR: " + INPUT_TENT_LEADER_PATH + " existiert nicht")
        print("ERROR: " + INPUT_TENT_LEADER_PATH + " existiert nicht")
        return loc_tent_leaders

    with open(arg_file_name, newline="", encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        loc_id = 0
        for i, row in enumerate(spamreader):
            if i >= 1:
                strip_row(row)

                loc_lastname = row[IDX_LEAD_LAST_NAME]
                loc_firstname = row[IDX_LEAD_FIRST_NAME]

                # parse zip code
                try:
                    loc_zipcode = int(row[IDX_LEAD_ZIP_CODE])
                except:
                    print(
                        "ERROR: failed to parse zip code: i: ",
                        i,
                        loc_firstname,
                        " ",
                        loc_lastname,
                    )
                    raise

                # parse tent number
                if row[IDX_LEAD_TENT] == "":
                    loc_tent = 9999
                else:
                    try:
                        loc_tent = int(row[IDX_LEAD_TENT])
                    except:
                        print(
                            "ERROR: failed to parse tent number: ",
                            row[IDX_LEAD_TENT],
                            "row: ",
                            row,
                        )
                        raise
                loc_birthdate = ""
                try:
                    loc_time_string = datetime.strptime(
                        row[IDX_LEAD_BIRTHDATE], "%d.%m.%Y"
                    ).date()
                    _ = loc_time_string.timetuple()
                    loc_birthdate = str(loc_time_string)

                except:
                    print(
                        "failed to parse birthdate: i: ",
                        i,
                        loc_firstname,
                        " ",
                        loc_lastname,
                        loc_birthdate
                    )
                    raise

                loc_tent_leader = TentLeader(
                    loc_id,
                    row[IDX_LEAD_JOB],
                    loc_lastname,
                    loc_firstname,
                    row[IDX_LEAD_STREET],
                    loc_zipcode,
                    row[IDX_LEAD_VILLAGE],
                    row[IDX_LEAD_PHONE],
                    row[IDX_LEAD_HANDY],
                    row[IDX_LEAD_MAIL],
                    loc_birthdate,
                    loc_tent,
                    row[IDX_LEAD_TEAM],
                    row[IDX_LEAD_COMMENT],
                )
                loc_id += 1

                loc_tent_leaders.append(loc_tent_leader)

        print("parsed input file: ", arg_file_name)
    return loc_tent_leaders


def props(obj):
    """converts class object into an dictonary"""
    props_dict = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith("__") and not inspect.ismethod(value):
            props_dict[name] = value
    return props_dict


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
    arg_p.tent = arg_o["tent"]

    revisions = list(filter(lambda x: x != "", revisions))
    return revisions


def get_paticipant_by_id(arg_participants, arg_id):
    """returns participant by given id"""
    for loc_participant in arg_participants:
        if loc_participant.identifier == arg_id:
            return loc_participant
    return None


def apply_participants_revisons(arg_participants):
    """apply_participants_revisons"""

    revison_logs.clear()

    if not os.path.isfile(INPUT_REVISION_PATH):
        error_logs.append("ERROR: " + INPUT_REVISION_PATH + " existiert nicht")
        print("ERROR: " + INPUT_REVISION_PATH + " existiert nicht")
        return arg_participants

    with open(INPUT_REVISION_PATH, encoding="utf8") as revision_file:
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

                revison_logs.append(loc_revision)

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

                revison_logs.append(loc_revision)

    return arg_participants


@ app.route("/api/participants", methods=["GET", "POST"])
def get_participants():
    """returns all participants as json"""
    global participants_d, tent_leaders
    if request.method == "POST":
        req = request.form.get("participants")
        req = json.loads(req)

        loc_revisions = []
        for loc_object in req:
            loc_particpant = get_paticipant_by_id(
                participants_d, int(loc_object["identifier"])
            )
            loc_revisions += particpant_object_to_class(
                loc_particpant, loc_object)

        participants_d, tent_leaders = save_data(
            participants_d, tent_leaders, loc_revisions)

    ret = []
    for loc_participant in participants_d:
        ret.append(props(loc_participant))
    return jsonify(ret)


@ app.route("/api/participant", methods=["GET", "POST"])
def get_participant():
    """returns participant by given id as json"""
    global participants_d, tent_leaders
    ret = {}
    try:
        if request.method == "POST":
            req = request.form.get("participant")
            req = json.loads(req)

            loc_id = int(req["identifier"])
            loc_participant = get_paticipant_by_id(participants_d, loc_id)
            if loc_participant is None:
                raise Exception

            loc_revisions = particpant_object_to_class(loc_participant, req)

            participants_d, tent_leaders = save_data(
                participants_d, tent_leaders, loc_revisions)
            loc_participant = get_paticipant_by_id(participants_d, loc_id)
            ret = props(loc_participant)

        else:
            loc_id = int(request.args.get("id"))
            loc_participant = get_paticipant_by_id(participants_d, loc_id)

            if loc_participant is None:
                raise Exception
            ret = props(loc_participant)

    except ValueError:
        print("ERROR: could not parse id")
        abort(404)

    return jsonify(ret)


@ app.route("/api/tentleaders", methods=["GET"])
def get_tent_leaders():
    """returns all tent_leaders as json"""
    ret = []
    for loc_tent_leader in tent_leaders:
        ret.append(props(loc_tent_leader))
    return jsonify(ret)


@ app.route("/api/maps", methods=["POST"])
def get_maps():
    """generate maps by given zipcode an location"""
    zip_codes = []
    req = request.form.get("zipCodes")
    for zip_code in json.loads(req):
        zip_codes.append((zip_code["zipCode"], zip_code["location"]))
    if len(zip_codes) > 0:
        generate_maps(zip_codes)
    return jsonify("ok")


@ app.route("/api/maps/<path:filename>")
def download_file(filename):
    """returns map file by filename"""
    return send_from_directory(app.config["MAPS_OUTPUT"], filename)


@ app.route("/api/graph", methods=["GET"])
def get_graph():
    """get_graph"""
    loc_stuebis = []
    compare_friends = [p.get_fullname() for p in participants_d]

    for participant in participants_d:
        loc_friends = []

        for loc_friend in participant.friends:
            if loc_friend in compare_friends:
                loc_friends.append(loc_friend)
            else:
                pass  # todo nicht angemeldet

        loc_stuebis.append(
            {"name": participant.get_fullname(), "friends": loc_friends})

    return jsonify(loc_stuebis)


@ app.route("/api/logs", methods=["GET"])
def get_logs():
    """returns logs"""
    ret = {}
    ret["errors"] = error_logs
    ret["revisions"] = revison_logs
    return jsonify(ret)


@ app.route("/api/configs", methods=["GET"])
def get_configs():
    """returns logs"""
    return jsonify(configs_d.get_dict())


if __name__ == "__main__":
    participants_d = parse_participants(INPUT_PARICIPANT_PATH)
    tent_leaders = parse_tent_leader(INPUT_TENT_LEADER_PATH)
    configs_d.load()

    app.run(host="0.0.0.0", port=8080, debug=True)
