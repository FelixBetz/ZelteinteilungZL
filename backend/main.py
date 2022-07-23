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

INPUT_FILE_PATH = r"..\\"
INPUT_FILE_NAME = "input.csv"

input_file = INPUT_FILE_PATH + INPUT_FILE_NAME

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


def bool_to_tex_zugestimmt(arg_bool):
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
    loc_header += "Ich möchte auch über weitere Veranstaltungen der Schönstattjugend per Mail informiert werden;"

    loc_header += "Person 1:;"
    loc_header += "Person 2:;"
    loc_header += "Schadensfreisspruch;"
    loc_header += "Fotografieren;"
    loc_header += (
        "Die Anmeldung ist erst mit der Überweisung des Teilnahmebeitrags wirksam;"
    )
    loc_header += "Personenbezogene Daten;"
    loc_header += "Ich bin damit einverstanden, dass im Falle einer Infektion meine Kontaktdaten an das Gesundheitsamt weitergegeben werden"
    loc_header += "\n"

    loc_row_str.append(loc_header)

    for part in participants:

        loc_row = ""
        loc_row += ";"  # Lfd-Nr
        loc_row += ";"  # Eingegangen
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

        loc_row += bool_to_tex_zugestimmt(part.is_photo_allowed) + ";"
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
    # parse_input_csv()


def parse_input_csv():
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

                loc_friends = []

                loc_participant = Participant(
                    loc_id,
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

                # parse pesons
                for friend in [row[19], row[20]]:
                    if friend != "":
                        loc_friends.append(friend)
                loc_participant.set_friends(loc_friends)

                participants.append(loc_participant)
        print("parsed input file: ", input_file)


def props(obj):
    """converts class object into an dictonary"""
    props_dict = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith("__") and not inspect.ismethod(value):
            props_dict[name] = value
    return props_dict


@app.route("/api/participants", methods=["GET"])
def get_participants():
    """returns all participants as json"""

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

            participants[loc_id].identifier = req["identifier"]
            participants[loc_id].lastname = req["lastname"]
            participants[loc_id].firstname = req["firstname"]
            participants[loc_id].birthdate = req["birthdate"]
            participants[loc_id].street = req["street"]
            participants[loc_id].zipcode = req["zipcode"]
            participants[loc_id].village = req["village"]
            participants[loc_id].phone = req["phone"]
            participants[loc_id].mail = req["mail"]
            participants[loc_id].emergency_contact = req["emergency_contact"]
            participants[loc_id].emergency_phone = req["emergency_phone"]
            participants[loc_id].is_afe = req["is_afe"]
            participants[loc_id].is_reduced = req["is_reduced"]
            participants[loc_id].is_event_mail = req["is_event_mail"]
            participants[loc_id].friends = req["friends"]
            participants[loc_id].is_photo_allowed = req["is_photo_allowed"]
            participants[loc_id].other = req["other"]
            participants[loc_id].tent = req["tent"]

            save_participants_to_csv()
            parse_input_csv()

            ret = props(participants[loc_id])
        else:
            loc_id = int(request.args.get("id"))
            ret = props(participants[loc_id])

    except:
        print("ERROR: could not parse id")
        abort(404)

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


if __name__ == "__main__":

    parse_input_csv()
    for index, participant in enumerate(participants):
        pass
        # print("[", index, "] ", participant)

    app.run(host="0.0.0.0", port=8080, debug=True)
