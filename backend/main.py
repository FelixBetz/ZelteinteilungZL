"""main file of ZelteinteilungZL"""


import csv
from datetime import datetime
import inspect

import subprocess
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from mailmerge import MailMerge
from docx2pdf import convert
from participant import Participant


INPUT_FILE = r"..\input.csv"
THUNDERBIRD_PATH = "C:\\Program Files (x86)\\Mozilla Thunderbird\\thunderbird.exe"
participants = []

app = Flask(__name__)
cors = CORS(app)


def parse_input_csv():
    """parses zeltlager participants from input csv file"""
    with open(INPUT_FILE, newline="") as csv_file:

        spamreader = csv.reader(csv_file, delimiter=";", quotechar="|")
        participant_id = 0
        for i, row in enumerate(spamreader):

            if i >= 1:

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
                    participant_id,
                    loc_lastname,
                    loc_firstname,
                    loc_zipcode,
                    loc_village,
                    loc_birthdate,
                )
                participant_id += 1

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


@app.route("/api/test", methods=["POST"])
def merge_docx():
    """returns all participants as json"""

    # TEMPLATE_FILE = r"..\template.docx"

    # output_dir = "..\\"
    # output_name = user["name"]
    # output_docx = output_name + ".docx"
    # output_pdf = output_name + ".pdf"

    # document = MailMerge(TEMPLATE_FILE)
    # print(document.get_merge_fields())
    # document.merge(Name=user["name"])
    # document.write(output_dir + output_docx)
    # convert(output_dir + output_docx)
    # anhang = os.getcwd() + "\\..\\" + output_pdf

    subject = request.form.get("subject")
    content = request.form.get("content")

    mail_mode = "bcc"
    if request.form.get("isBcc") is None:
        mail_mode = "to"

    csv_filehandle = request.files["csvFile"]

    csv_file = csv_filehandle.read().decode("utf8").split("\r\n")

    mail_index = csv_file[0].split(";").index("mail")
    mails = []
    for i, row in enumerate(csv_file):
        if i > 0 and row is not None and row != "":
            mail = row.split(";")[mail_index]
            mails.append(mail)

    parameterliste = (
        THUNDERBIRD_PATH
        + " -compose "
        + mail_mode
        + "='"
        + ",".join(mails)
        + "',"
        + "subject='"
        + subject
        + "',"
        + "body='"
        + content
        + "',"
        # + "attachment='"
        # + anhang
        # + "'"
    )

    subprocess.Popen(parameterliste)

    return jsonify("ok")


if __name__ == "__main__":
    # create this node as publisher

    parse_input_csv()

    for index, participant in enumerate(participants):
        print("[", index, "] ", participant)

    app.run(host="0.0.0.0", port=8080, debug=True)
