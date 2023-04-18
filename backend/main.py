"""main file of ZelteinteilungZL"""


import time
import csv
import os
from datetime import datetime
import inspect
import json
from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from maps import generate_maps
from participant import Participant
from tent_leader import TentLeader

INPUT_FILE_PATH = r"..\\input\\"
INPUT_FILE_NAME = "input.csv"
INPUT_TENT_LEADER_FILE_NAME = "2022_leitungsteam_anfrage.csv"

input_file = INPUT_FILE_PATH + INPUT_FILE_NAME
input_tent_leader_file = INPUT_FILE_PATH + INPUT_TENT_LEADER_FILE_NAME

tent_leaders = []

participants = []
csv_revison_num = -1

app = Flask(__name__)
cors = CORS(app)

app.config["MAPS_OUTPUT"] = "output_maps"


def parse_yes_no(arg_string):
    """parses formular ja/zugestimmt to boolean"""
    arg_string = arg_string.strip()
    if arg_string in ("ja", "Zugestimmt", "zugestimmt"):
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


def save_participants_to_csv():
    """save participants back to csv file"""
    global csv_revison_num
    loc_row_str = []

    loc_header = ""
    loc_header += "Lfd-Nr;"
    loc_header += "Bezahlt;"
    loc_header += "Zelt;"
    loc_header += "Nachname;"
    loc_header += "Vorname;"
    loc_header += "Straße mit Hausnummer;"
    loc_header += "PLZ;"
    loc_header += "Ort;"
    loc_header += "Alter;"
    loc_header += "Heute;"
    loc_header += "Geburtstag;"
    loc_header += "Telefon;"
    loc_header += "eMail;"
    loc_header += "Ansprechpartner für Notfälle während des Lagers (Name);"
    loc_header += "Telefonnummer Ansprechpartner;"
    loc_header += (
        "Was wir sonst noch wissen sollten (tägliche Medikamente, Allergien o.ä);"
    )
    loc_header += (
        "Unsere Tochter nimmt an der Ferienwoche der Mädchenjugend in Harthausen teil.;"
    )
    loc_header += "Ermäßigter Beitrag;"
    loc_header += "Ich möchte auch über weitere Veranstaltungen der\
          Schönstattjugend per Mail informiert werden;"

    loc_header += "Person 1:;"
    loc_header += "Person 2:;"
    loc_header += "Schadensfreisspruch;"
    loc_header += "Fotografieren;"
    loc_header += (
        "Die Anmeldung ist erst mit der Überweisung des Teilnahmebeitrags wirksam;"
    )
    loc_header += "Personenbezogene Daten;"
    loc_header += "Ich bin damit einverstanden, dass im Falle einer Infektion\
          meine Kontaktdaten an das Gesundheitsamt weitergegeben werden"
    loc_header += "\n"

    loc_row_str.append(loc_header)

    for part in participants:

        loc_row = ""
        loc_row += ";"  # Lfd-Nr
        # paid
        if part.paid:
            loc_row += "True;"
        else:
            loc_row += "False;"
        loc_row += str(part.tent) + ";"  # Zelt
        loc_row += part.lastname + ";"
        loc_row += part.firstname + ";"
        loc_row += part.street + ";"
        loc_row += str(part.zipcode) + ";"
        loc_row += part.village + ";"
        loc_row += ";"  # Alter
        loc_row += ";"  # Heute
        loc_row += part.birthdate + ";"
        loc_row += part.phone + ";"
        loc_row += part.mail + ";"
        loc_row += part.emergency_contact + ";"
        loc_row += part.emergency_phone + ";"
        loc_row += part.other + ";"

        loc_row += bool_to_tex_yes_no(part.is_afe) + ";"
        loc_row += bool_to_tex_yes_no(part.is_reduced) + ";"
        loc_row += bool_to_tex_yes_no(part.is_event_mail) + ";"

        loc_row += part.get_friend_string(0) + ";"
        loc_row += part.get_friend_string(1) + ";"

        loc_row += "Zugestimmt;"  # Schadensfreisspruch

        loc_row += bool_to_text_zugestimmt(part.is_photo_allowed) + ";"
        loc_row += "Zugestimmt;"  # Teilnahmebeitrag mit Überweisung wirksam
        loc_row += "Zugestimmt;"  # Personenbezogene Daten
        loc_row += "Zugestimmt"  # Gesundheitsamt

        loc_row += "\n"
        loc_row_str.append(loc_row)
    with open(
        INPUT_FILE_PATH + INPUT_FILE_NAME + "." +
            str(csv_revison_num + 1).zfill(5), "w"
    ) as outfile:
        outfile.writelines(loc_row_str)


def is_paided(arg_paided):
    """is paided"""
    if arg_paided in ["true", "True"]:
        return True
    return False


def parse_participants():
    """parses zeltlager participants from input csv file"""
    global input_file, csv_revison_num, participants

    participants = []

    # parse csv_revison_num

    loc_rev_filename = ""
    for file in os.listdir(".."):
        if file.startswith(INPUT_FILE_NAME):
            loc_splitted = file.split(".")
            if loc_splitted[-1] != "csv":
                loc_comp_num = int(loc_splitted[-1])
                if loc_comp_num > csv_revison_num:
                    csv_revison_num = loc_comp_num
                    loc_rev_filename = file

    if csv_revison_num >= 0:
        input_file = INPUT_FILE_PATH + loc_rev_filename

    # check number of semicolons
    with open(input_file, newline="") as csvfile:
        for check_row in csvfile:
            cnt_semicolon = check_row.count(";")
            if cnt_semicolon != 25:
                print("ERROR at row:", check_row)

    with open(input_file, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        loc_id = 0
        for i, row in enumerate(spamreader):

            if i >= 1:

                loc_paided = is_paided(row[1].strip())

                # parse tent number
                if row[2] == "":
                    loc_tent = 9999
                else:
                    try:
                        loc_tent = int(row[2].strip())
                    except:
                        print(
                            "ERROR: failed to parse tent number: ", row[2], "row: ", row
                        )
                        raise

                loc_lastname = row[3].strip()
                loc_firstname = row[4].strip()
                loc_street = row[5].strip()

                # parse zip code
                try:
                    loc_zipcode = int(row[6].strip())
                except:
                    print(
                        "ERROR: failed to parse zip coce: i: ",
                        i,
                        loc_firstname,
                        " ",
                        loc_lastname,
                    )
                    raise
                loc_village = row[7].strip()

                try:
                    loc_time_string = datetime.strptime(
                        row[10].strip(), "%d.%m.%Y"
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
                loc_birthdate = row[10].strip()

                loc_phone = row[11].strip()
                loc_mail = row[12].strip()
                loc_emergency_contact = row[13].strip()
                loc_emergency_phone = row[14].strip()

                loc_other = row[15].strip()

                loc_is_afe = parse_yes_no(row[16])
                loc_is_reduced = parse_yes_no(row[17])
                loc_is_event_mail = parse_yes_no(row[18])

                # row[19] = friend1
                # row[20] = friend2

                loc_is_photo_allowed = parse_yes_no(row[22])

                loc_participant = Participant(
                    loc_id,
                    loc_paided,
                    loc_lastname,
                    loc_firstname,
                    loc_street,
                    loc_zipcode,
                    loc_village,
                    loc_birthdate,
                    loc_phone,
                    loc_mail,
                    loc_emergency_contact,
                    loc_emergency_phone,
                    loc_is_reduced,
                    loc_is_photo_allowed,
                    loc_is_afe,
                    loc_is_event_mail,
                    loc_other,
                    loc_tent,
                )
                loc_id += 1

                participants.append(loc_participant)

        # parse freinds
        with open(input_file, newline="") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")

            loc_names = []
            for participant in participants:
                loc_names.append(participant.get_fullname())

            loc_id = 0
            for i, row in enumerate(spamreader):
                if i >= 1:
                    loc_friends = []
                    loc_name = participants[loc_id].get_fullname()
                    for friend in [row[19], row[20]]:
                        splitted = friend.split(",")
                        for friend_str in splitted:
                            friend_str = friend_str.strip()
                            if friend_str != "":
                                if friend_str in loc_names:
                                    loc_friends.append(friend_str)
                                else:
                                    print("cannot find: ", friend_str,
                                          " (", loc_name, ")")
                        participants[loc_id].set_friends(loc_friends)
                    loc_id += 1

        print("parsed input file: ", input_file)


def parse_tent_leader():
    """parses zeltlager tent leader from input csv file"""
    global input_tent_leader_file, tent_leaders

    tent_leaders = []

    with open(input_tent_leader_file, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        loc_id = 0
        for i, row in enumerate(spamreader):

            if i >= 1:

                loc_job = row[0].strip()
                loc_lastname = row[1].strip()
                loc_firstname = row[2].strip()
                loc_street = row[3].strip()

                # parse zip code
                try:
                    loc_zipcode = int(row[4].strip())
                except:
                    print(
                        "ERROR: failed to parse zip coce: i: ",
                        i,
                        loc_firstname,
                        " ",
                        loc_lastname,
                    )
                    raise
                loc_village = row[5].strip()

                loc_phone = row[6].strip()
                loc_handy = row[7].strip()
                loc_mail = row[8].strip()

                loc_birthdate = row[9].strip()

                # parse tent number
                if row[10] == "":
                    loc_tent = 9999
                else:
                    try:
                        loc_tent = int(row[10].strip())
                    except:
                        print(
                            "ERROR: failed to parse tent number: ", row[10], "row: ", row
                        )
                        raise

                loc_team = row[11].strip()
                loc_comment = row[12].strip()

                loc_tent_leader = TentLeader(
                    loc_id,
                    loc_job,
                    loc_lastname,
                    loc_firstname,
                    loc_street,
                    loc_zipcode,
                    loc_village,
                    loc_phone,
                    loc_handy,
                    loc_mail,
                    loc_birthdate,
                    loc_tent,
                    loc_team,
                    loc_comment
                )
                loc_id += 1

                tent_leaders.append(loc_tent_leader)

        print("parsed input file: ", input_file)


def props(obj):
    """converts class object into an dictonary"""
    props_dict = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith("__") and not inspect.ismethod(value):
            props_dict[name] = value
    return props_dict


def particpant_object_to_class(arg_participant, arg_id):
    """converts dict object to participant object"""
    participants[arg_id].identifier = arg_participant["identifier"]
    participants[arg_id].paid = arg_participant["paid"]
    participants[arg_id].lastname = arg_participant["lastname"]
    participants[arg_id].firstname = arg_participant["firstname"]
    participants[arg_id].birthdate = arg_participant["birthdate"]
    participants[arg_id].street = arg_participant["street"]
    participants[arg_id].zipcode = arg_participant["zipcode"]
    participants[arg_id].village = arg_participant["village"]
    participants[arg_id].phone = arg_participant["phone"]
    participants[arg_id].mail = arg_participant["mail"]
    participants[arg_id].emergency_contact = arg_participant["emergency_contact"]
    participants[arg_id].emergency_phone = arg_participant["emergency_phone"]
    participants[arg_id].is_afe = arg_participant["is_afe"]
    participants[arg_id].is_reduced = arg_participant["is_reduced"]
    participants[arg_id].is_event_mail = arg_participant["is_event_mail"]
    participants[arg_id].friends = arg_participant["friends"]
    participants[arg_id].is_photo_allowed = arg_participant["is_photo_allowed"]
    participants[arg_id].other = arg_participant["other"]
    participants[arg_id].tent = arg_participant["tent"]


@app.route("/api/participants", methods=["GET", "POST"])
def get_participants():
    """returns all participants as json"""
    if request.method == "POST":

        req = request.form.get("participants")
        req = json.loads(req)

        for loc_particpant in req:
            loc_id = loc_particpant["identifier"]
            particpant_object_to_class(loc_particpant, loc_id)

        save_participants_to_csv()
        parse_participants()

    ret = []
    for loc_participant in participants:
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
            particpant_object_to_class(req, loc_id)

            save_participants_to_csv()
            parse_participants()

            ret = props(participants[loc_id])
        else:
            loc_id = int(request.args.get("id"))
            ret = props(participants[loc_id])

    except:
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

    for participant in participants:
        loc_stuebis.append(
            {"name": participant.get_fullname(), "friends": participant.friends})

    return jsonify(loc_stuebis)


if __name__ == "__main__":

    parse_participants()
    parse_tent_leader()
    for index, participant in enumerate(participants):
        pass
        # print("[", index, "] ", participant)

    app.run(host="0.0.0.0", port=8080, debug=True)
