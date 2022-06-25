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
from typedefs import MailType


INPUT_FILE = r"..\input.csv"
THUNDERBIRD_PATH = "C:\\Program Files (x86)\\Mozilla Thunderbird\\thunderbird.exe"
participants = []

app = Flask(__name__)
cors = CORS(app)


def parse_input_csv():
    """parses zeltlager participants from input csv file"""
    with open(INPUT_FILE, newline="", ) as csv_file:

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
                    loc_birthdate = (datetime.strptime(
                        row[10], "%d.%m.%Y").date(),)
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


def send_mail(arg_mails, arg_mail_mode, arg_subject, arg_content, arg_attachments):

    execute_thunderbird = (
        THUNDERBIRD_PATH
        + " -compose "
        + arg_mail_mode
        + "='"
        + ",".join(arg_mails)
        + "',"
        + "subject='"
        + arg_subject
        + "',"
        + "body='"
        + arg_content
        + "',"
        # + "attachment='"
        # + anhang
        # + "'"
    )

    subprocess.Popen(execute_thunderbird)


def send_massmail(arg_mails, arg_mail_mode, arg_subject, arg_content, arg_attachments):
    """send massmail"""
    send_mail(arg_mails, arg_mail_mode, arg_subject,
              arg_content, arg_attachments)


def send_personalized_mail(arg_csv_file, arg_mails,  arg_subject, arg_content, arg_attachments):
    """send personalized mail"""
    csv_cols = arg_csv_file[0].split(";")
    for mail_index, mail in enumerate(arg_mails):
        tmp_content = arg_content
        for col_index, col in enumerate(csv_cols):

            tmp_content = tmp_content.replace(
                "[$$$"+col+"$$$]", arg_csv_file[mail_index+1].split(";")[col_index])

        send_mail([mail], "to", arg_subject, tmp_content, arg_attachments)


def send_template_mail(arg_csv_file, arg_mails,  arg_subject, arg_content, arg_attachments):
    """send mail based on a word template"""
    csv_cols = arg_csv_file[0].split(";")
    for mail_index, mail in enumerate(arg_mails):
        TEMPLATE_FILE = r"..\template.docx"

        output_dir = "..\\"
        output_name = str(mail_index)+"test"
        output_docx = output_name + ".docx"
        output_pdf = output_name + ".pdf"

        document = MailMerge(TEMPLATE_FILE)

        for col_index, col in enumerate(csv_cols):
            splitted_row = arg_csv_file[mail_index+1].split(";")
            document.merge_templates(
                [{col: splitted_row[col_index]}], separator='page_break')

        document.write(output_dir + output_docx)
        convert(output_dir + output_docx)
        anhang = os.getcwd() + "\\..\\" + output_pdf
        send_personalized_mail(arg_csv_file, arg_mails,
                               arg_subject, arg_content, arg_attachments)


@ app.route("/api/test", methods=["POST"])
def merge_docx():
    """returns all participants as json"""

    mail_type = MailType(int(request.form.get("mailType")))
    subject = request.form.get("subject")
    content = request.form.get("content")

    csv_filehandle = request.files["csvFile"]

    csv_file = csv_filehandle.read().decode("utf8").split("\r\n")
    mail_index = csv_file[0].split(";").index("mail")
    mails = []
    for i, row in enumerate(csv_file):
        if i > 0 and row is not None and row != "":
            mail = row.split(";")[mail_index]
            mails.append(mail)

    if mail_type == MailType.MASS_MAIL:
        mail_mode = "bcc"
        if request.form.get("isBcc") is None:
            mail_mode = "to"
        send_massmail(mails, mail_mode, subject, content, [])
    elif mail_type == MailType.PERSONALIZED_MAIL:
        send_personalized_mail(csv_file, mails,  subject, content, [])
    elif mail_type == MailType.TEMPLATE_MAIL:
        send_template_mail(csv_file, mails,  subject, content, [])

    return jsonify("ok")


if __name__ == "__main__":
    # create this node as publisher

    parse_input_csv()

    for index, participant in enumerate(participants):
        print("[", index, "] ", participant)

    app.run(host="0.0.0.0", port=8080, debug=True)
