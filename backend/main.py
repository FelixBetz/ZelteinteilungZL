"""main file of ZelteinteilungZL"""


import csv
from datetime import datetime
import inspect

from flask import Flask, jsonify, request
from flask_cors import CORS

from participant import Participant


INPUT_FILE = r"..\input.csv"
participants = []

app = Flask(__name__)
cors = CORS(app)


def parse_input_csv():
    """parses zeltlager participants from input csv file"""
    with open(INPUT_FILE, newline="") as csvfile:

        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        id = 0
        for i, row in enumerate(spamreader):

            if 1 <= i < 6:

                loc_lastname = row[3]
                loc_firstname = row[4]
                try:
                    loc_zipcode = int(row[6])
                except:
                    print(
                        "failed to parse zip coce: i: ",
                        i,
                        loc_firstname,
                        " ",
                        loc_lastname,
                    )
                    raise
                loc_village = row[7]
                try:
                    loc_birthdate = (datetime.strptime(row[10], "%d.%m.%Y").date(),)
                except:
                    print(
                        "failed to parse birthdate: i: ",
                        i,
                        loc_firstname,
                        " ",
                        loc_lastname,
                    )
                    raise
                loc_friends = []

                loc_participant = Participant(
                    id,
                    loc_lastname,
                    loc_firstname,
                    loc_zipcode,
                    loc_village,
                    loc_birthdate,
                )
                id += 1

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


@app.route("/api/participant", methods=["GET"])
def get_participant():
    """returns participant by given id as json"""
    ret = {}
    try:
        loc_id = int(request.args.get("id"))
        ret = props(participants[loc_id])

    except:
        print("ERROR: could not parse id")

    return jsonify(ret)


if __name__ == "__main__":
    # create this node as publisher

    parse_input_csv()

    for index, participant in enumerate(participants):
        print("[", index, "] ", participant)

    app.run(host="0.0.0.0", port=8080, debug=True)
