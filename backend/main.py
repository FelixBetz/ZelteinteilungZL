"""main file of ZelteinteilungZL"""
import json
import os
import csv
import time
from datetime import datetime
from flask_cors import CORS
from flask import Flask, abort, jsonify, request, send_from_directory
import file_indices as IDX
from helpers import parse_yes_no, strip_row, is_paided, props
from tent_leader import TentLeader
from participant import Participant, particpant_object_to_class
from maps import generate_maps
from config import Config
from mailing.mailing import mailing_routes

INPUT_FILE_PATH = r"..\\input\\"
INPUT_FILE_NAME = "2023_teilnehmer_input.csv"
INPUT_TENT_LEADER_FILE_NAME = "2023_leitungsteam_anfrage.csv"
INPUT_REVISION_FILE_NAME = "revisions.txt"
INPUT_TENT_NUMBERS_FILE_NAME = "tent_numbers.txt"
INPUT_PAID_FILE_NAME = "paid.txt"
INPUT_CONFIG_FILE_NAME = "config.txt"
INPUT_LAST_YEAR_FILE_NAME = "2022_zl_tn_out.csv"

INPUT_PARICIPANT_PATH = INPUT_FILE_PATH + INPUT_FILE_NAME
INPUT_TENT_LEADER_PATH = INPUT_FILE_PATH + INPUT_TENT_LEADER_FILE_NAME
INPUT_REVISION_PATH = INPUT_FILE_PATH + INPUT_REVISION_FILE_NAME
INPUT_TENT_NUMBERS_PATH = INPUT_FILE_PATH + INPUT_TENT_NUMBERS_FILE_NAME
INPUT_PAID_PATH = INPUT_FILE_PATH + INPUT_PAID_FILE_NAME
INPUT_CONFIG_PATH = INPUT_FILE_PATH + INPUT_CONFIG_FILE_NAME
INPUT_LAST_YEAR_PATH = INPUT_FILE_PATH + INPUT_LAST_YEAR_FILE_NAME

tent_leaders = []
participants_d = []
configs_d = Config(INPUT_CONFIG_PATH)

error_logs = []
revison_logs = []

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(mailing_routes)

app.config["MAPS_OUTPUT"] = "output_maps"


def check_if_participant_file_valid(arg_input_file):
    """check_if_participant_file_valid"""
    # check number of semicolons
    with open(arg_input_file, newline="", encoding="utf-8") as csvfile:
        for check_row in csvfile:
            cnt_semicolon = check_row.count(";")
            if cnt_semicolon != IDX.ROWS_PARP:
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


def parse_participants_last_year(arg_file_name):
    """parses zeltlager participants from input csv file"""

    loc_participants = []

    if not os.path.isfile(arg_file_name):
        error_logs.append("ERROR: " + arg_file_name + " existiert nicht")
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
    compare_friends = [p.get_fullname() for p in participants_d]
    for participant in loc_participants:
        if participant not in compare_friends:
            ret.append(participant)

    return ret


def parse_participants(arg_file_name):
    """parses zeltlager participants from input csv file"""
    global error_logs, configs_d

    error_logs.clear()
    for error in configs_d.errors:
        print("!:", error)
        error_logs.append(error)
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
                    loc_time_string = datetime.strptime(
                        row[IDX.PARP_BIRTHDATE], "%Y-%m-%d"
                    ).date()
                    loc_tuple = loc_time_string.timetuple()
                    timestamp = time.mktime(loc_tuple)
                    loc_birthdate = timestamp

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

                loc_lastname = row[IDX.LEAD_LAST_NAME]
                loc_firstname = row[IDX.LEAD_FIRST_NAME]

                # parse zip code
                try:
                    loc_zipcode = int(row[IDX.LEAD_ZIP_CODE])
                except:
                    print("ERROR: failed to parse zip code: i: ",
                          i, loc_firstname, " ", loc_lastname,)
                    raise

                # parse tent number
                if row[IDX.LEAD_TENT] == "":
                    loc_tent = 9999
                else:
                    try:
                        loc_tent = int(row[IDX.LEAD_TENT])
                    except:
                        print("ERROR: failed to parse tent number: ",
                              row[IDX.LEAD_TENT], "row: ", row,)
                        raise
                loc_birthdate = ""
                try:
                    loc_time_string = datetime.strptime(
                        row[IDX.LEAD_BIRTHDATE], "%d.%m.%Y"
                    ).date()
                    _ = loc_time_string.timetuple()
                    loc_birthdate = str(loc_time_string)

                except:
                    print("failed to parse birthdate: i: ",
                          i, loc_firstname, " ", loc_lastname, loc_birthdate)
                    raise

                loc_tent_leader = TentLeader(
                    loc_id,
                    row[IDX.LEAD_JOB],
                    loc_lastname,
                    loc_firstname,
                    row[IDX.LEAD_STREET],
                    loc_zipcode,
                    row[IDX.LEAD_VILLAGE],
                    row[IDX.LEAD_PHONE],
                    row[IDX.LEAD_HANDY],
                    row[IDX.LEAD_MAIL],
                    loc_birthdate,
                    loc_tent,
                    row[IDX.LEAD_TEAM],
                    row[IDX.LEAD_COMMENT],
                )
                loc_id += 1

                loc_tent_leaders.append(loc_tent_leader)

        print("parsed input file: ", arg_file_name)
    return loc_tent_leaders


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
    warnings = []
    req = request.form.get("zipCodes")
    for zip_code in json.loads(req):
        zip_codes.append(
            (zip_code["zipCode"], zip_code["location"],
             zip_code["addressString"], zip_code["name"]))
    if len(zip_codes) > 0:
        warnings = generate_maps(zip_codes)
    return jsonify(warnings)


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


@ app.route("/api/configs", methods=["GET", "POST"])
def get_configs():
    """returns logs"""
    if request.method == "POST":
        req = request.get_json()
        configs_d.num_tents = req["numTents"]
        configs_d.zl_start = req["zlStart"]
        configs_d.calender_url = req["calenderUrl"]
        configs_d.save()
    return jsonify(configs_d.get_dict())


@ app.route("/api/participants/last-year", methods=["GET"])
def get_participants_last_year():
    """returns all participants as json"""
    return jsonify(participants_last_year)


if __name__ == "__main__":
    configs_d.load()

    participants_d = parse_participants(INPUT_PARICIPANT_PATH)
    tent_leaders = parse_tent_leader(INPUT_TENT_LEADER_PATH)
    participants_last_year = parse_participants_last_year(INPUT_LAST_YEAR_PATH)

    app.run(host="0.0.0.0", port=8080, debug=True)
