"""main file of ZelteinteilungZL"""

import time
import csv

from datetime import datetime
import inspect
import json
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
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
INPUT_TENT_LEADER_FILE_NAME = "2022_leitungsteam_anfrage.csv"
INPUT_REVISION_FILE_NAME = "edit.txt"
INPUT_TENTT_NUMBERS_FILE_NAME = "tent_numbers.txt"

INPUT_PARICIPANT_PATH = INPUT_FILE_PATH + INPUT_FILE_NAME
INPUT_TENT_LEADER_PATH = INPUT_FILE_PATH + INPUT_TENT_LEADER_FILE_NAME
INPUT_REVISION_PATH = INPUT_FILE_PATH + INPUT_REVISION_FILE_NAME
INPUT_TENT_NUMBERS_PATH = INPUT_FILE_PATH + INPUT_TENTT_NUMBERS_FILE_NAME

tent_leaders = []
participants_d = []

app = Flask(__name__)
cors = CORS(app)

app.config["MAPS_OUTPUT"] = "output_maps"


def strip_row(arg_row):
    """strip_row"""
    for i, col in enumerate(arg_row):
        arg_row[i] = col.replace("\"", "").strip()


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


def parse_tent_numbers(arg_participants):
    """parse tent numbers"""
    with open(INPUT_TENT_NUMBERS_PATH, encoding="utf8") as tent_numbers_file:
        for row in tent_numbers_file:
            splitted_row = row.split(";")
            loc_id = int(splitted_row[0].strip())
            loc_tent_number = int(splitted_row[1].strip())

            loc_participant = get_paticipant_by_id(arg_participants, loc_id)
            if loc_participant is None:
                print("ERROR: participant not found")
                # todo
            else:
                loc_participant.tent = loc_tent_number
    return arg_participants


def parse_participants(arg_file_name):
    """parses zeltlager participants from input csv file"""
    loc_participants = []

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
                    print("ERROR: failed to parse zip coce: i: ",
                          i, loc_firstname, " ", loc_lastname, )
                    raise

                try:
                    loc_time_string = datetime.strptime(
                        row[IDX_PARP_BIRTHDATE], "%Y-%m-%d").date()
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
                    is_paided("false"),  # todo
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
                    parse_yes_no(row[IDX_PARP_VEGETARIAN]),  # todo
                    parse_yes_no(row[IDX_PARP_NEWSLETTER]),  # todo
                    row[IDX_PARP_OTHER],
                    9999,  # will be overwritten by parse_tent_numbers()
                )

                loc_participant.set_friends(
                    [row[IDX_PARP_FRIEND1],
                     row[IDX_PARP_FRIEND2]]
                )

                loc_participants.append(loc_participant)

        print("parsed input file: ", arg_file_name)
        loc_participants = parse_tent_numbers(loc_participants)
    return loc_participants


def parse_tent_leader(arg_file_name):
    """parses zeltlager tent leader from input csv file"""

    loc_tent_leaders = []

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
                    print("ERROR: failed to parse zip code: i: ",
                          i, loc_firstname, " ", loc_lastname,)
                    raise

                # parse tent number
                if row[IDX_LEAD_TENT] == "":
                    loc_tent = 9999
                else:
                    try:
                        loc_tent = int(row[IDX_LEAD_TENT])
                    except:
                        print("ERROR: failed to parse tent number: ",
                              row[IDX_LEAD_TENT], "row: ", row)
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
                    row[IDX_LEAD_BIRTHDATE],
                    loc_tent,
                    row[IDX_LEAD_TEAM],
                    row[IDX_LEAD_COMMENT]
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


def particpant_object_to_class(arg_participant, arg_object):
    """converts dict object to participant object"""
    arg_participant.identifier = arg_object["identifier"]
    arg_participant.paid = arg_object["paid"]
    arg_participant.lastname = arg_object["lastname"]
    arg_participant.firstname = arg_object["firstname"]
    arg_participant.birthdate = arg_object["birthdate"]
    arg_participant.street = arg_object["street"]
    arg_participant.zipcode = arg_object["zipcode"]
    arg_participant.village = arg_object["village"]
    arg_participant.phone = arg_object["phone"]
    arg_participant.mail = arg_object["mail"]
    arg_participant.emergency_contact = arg_object["emergency_contact"]
    arg_participant.emergency_phone = arg_object["emergency_phone"]
    arg_participant.is_afe = arg_object["is_afe"]
    arg_participant.is_reduced = arg_object["is_reduced"]
    arg_participant.is_event_mail = arg_object["is_event_mail"]
    arg_participant.friends = arg_object["friends"]
    arg_participant.is_photo_allowed = arg_object["is_photo_allowed"]
    arg_participant.other = arg_object["other"]
    arg_participant.tent = arg_object["tent"]


def get_paticipant_by_id(arg_participants, arg_id):
    """ retunrs participant by given id"""
    for loc_participant in arg_participants:
        if loc_participant.identifier == arg_id:
            return loc_participant
    return None


@app.route("/api/participants", methods=["GET", "POST"])
def get_participants():
    """returns all participants as json"""
    global participants_d
    if request.method == "POST":

        req = request.form.get("participants")
        req = json.loads(req)

        for loc_object in req:
            loc_particpant = get_paticipant_by_id(
                participants_d, int(loc_object["identifier"]))
            particpant_object_to_class(loc_particpant, loc_object)

        # todosave_participants_to_csv()

        # save tent numbers
        tent_numbers = [{"id": p.identifier, "tent": p.tent}
                        for p in participants_d]
        with open(INPUT_TENT_NUMBERS_PATH, "w", encoding="utf-8") as tent_number_file:
            for number in tent_numbers:
                if number["tent"] != 9999:
                    tent_number_file.write(
                        str(number["id"]) + ";" + str(number["tent"]) + "\n")

        # reparse participants
        participants_d = parse_participants(INPUT_PARICIPANT_PATH)
    ret = []
    for loc_participant in participants_d:
        ret.append(props(loc_participant))
    return jsonify(ret)


@app.route("/api/participant", methods=["GET", "POST"])
def get_participant():
    """returns participant by given id as json"""
    ret = {}
    try:
        if request.method == "POST":

            req = request.form.get("participant")
            req = json.loads(req)
            loc_id = req["identifier"]
            # todo particpant_object_to_class(req, loc_id)

            # todo save_participants_to_csv()
            # todo parse_participants()

            # todo ret = props(participants_d[loc_id])
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


@app.route("/api/tentleaders", methods=["GET"])
def get_tent_leaders():
    """returns all tent_leaders as json"""
    ret = []
    for loc_tent_leader in tent_leaders:
        ret.append(props(loc_tent_leader))
    return jsonify(ret)


@app.route("/api/maps", methods=["POST"])
def get_maps():
    """generate maps by given zipcode an location"""
    zip_codes = []
    req = request.form.get("zipCodes")
    for zip_code in json.loads(req):
        zip_codes.append((zip_code["zipCode"], zip_code["location"]))

    generate_maps(zip_codes)
    return jsonify("ok")


@app.route("/api/maps/<path:filename>")
def download_file(filename):
    """returns map file by filename"""
    return send_from_directory(app.config["MAPS_OUTPUT"], filename)


@app.route("/api/tmp", methods=["GET"])
def get_temp():
    """get_temp"""
    loc_stuebis = []

    for participant in participants_d:  # todo
        loc_stuebis.append(
            {"name": participant.get_fullname(), "friends": participant.friends})

    return jsonify(loc_stuebis)


if __name__ == "__main__":

    participants_d = parse_participants(INPUT_PARICIPANT_PATH)
    tent_leaders = parse_tent_leader(INPUT_TENT_LEADER_PATH)

    app.run(host="0.0.0.0", port=8080, debug=True)
