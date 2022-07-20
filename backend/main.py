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


INPUT_FILE = r"..\input.csv"
participants = []

app = Flask(__name__)
cors = CORS(app)

app.config["MAPS_OUTPUT"] = "output_maps"


def parse_yes_no(arg_string):
    """parses formular ja/zugestimmt to boolean"""
    arg_string = arg_string.strip()
    if arg_string in ("ja", "Zugestimmt", "zugestimmt"):
        return True
    return False


def parse_input_csv():
    """parses zeltlager participants from input csv file"""

    # check number of semicolons
    with open(INPUT_FILE, newline="") as csvfile:
        for check_row in csvfile:
            cnt_semicolon = check_row.count(";")
            if cnt_semicolon != 25:
                print("ERROR at row:", check_row)

    with open(INPUT_FILE, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        loc_id = 0
        for i, row in enumerate(spamreader):

            if i >= 1:

                loc_lastname = row[3].strip()
                loc_firstname = row[4].strip()
                loc_street = row[5].strip()
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

                loc_tent = 22

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
            participants[loc_id].tent = 234

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
    # create this node as publisher

    parse_input_csv()

    for index, participant in enumerate(participants):
        pass
        # print("[", index, "] ", participant)

    app.run(host="0.0.0.0", port=8080, debug=True)
