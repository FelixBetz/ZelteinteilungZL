"""main file of ZelteinteilungZL"""
import json

from flask_cors import CORS
from flask import Flask, abort, jsonify, request, send_from_directory
from helpers import props
from participants.participants import get_paticipant_by_id, parse_participants,\
    parse_participants_last_year
from participants.participant_c import particpant_object_to_class

from maps import generate_maps
from config import Config
from mailing.mailing import mailing_routes
from tent_leaders.tent_leaders import parse_tent_leader

INPUT_FILE_PATH = r"..\\input\\"
INPUT_FILE_NAME = "2023_teilnehmer_input.csv"
INPUT_TENT_LEADER_FILE_NAME = "2023_leitungsteam_anfrage.csv"
INPUT_REVISION_FILE_NAME = "revisions.txt"
INPUT_TENT_NUMBERS_FILE_NAME = "tent_numbers.txt"
INPUT_PAID_FILE_NAME = "paid.txt"
INPUT_CONFIG_FILE_NAME = "config.txt"
INPUT_LAST_YEAR_FILE_NAME = "2022_zl_tn_out.csv"

I_PARICIPANT = INPUT_FILE_PATH + INPUT_FILE_NAME
I_TENT_LEADER = INPUT_FILE_PATH + INPUT_TENT_LEADER_FILE_NAME
I_REVISION = INPUT_FILE_PATH + INPUT_REVISION_FILE_NAME
I_TENT_NUMBERS = INPUT_FILE_PATH + INPUT_TENT_NUMBERS_FILE_NAME
I_PAID = INPUT_FILE_PATH + INPUT_PAID_FILE_NAME
I_CONFIG = INPUT_FILE_PATH + INPUT_CONFIG_FILE_NAME
I_LAST_YEAR = INPUT_FILE_PATH + INPUT_LAST_YEAR_FILE_NAME

tent_leaders = []
participants_d = []
configs_d = Config(I_CONFIG)

error_logs = []
revison_logs = []

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(mailing_routes)

app.config["MAPS_OUTPUT"] = "output_maps"


def save_data(arg_participants, arg_leaders, arg_revisions, arg_errors):
    """save participants tent numbers, revisions, paid"""
    # save tent numbers
    tent_numbers = [{"id": p.identifier, "tent": p.tent}
                    for p in arg_participants]
    with open(I_TENT_NUMBERS, "w", encoding="utf-8") as tent_number_file:
        for number in tent_numbers:
            if number["tent"] != 9999:
                tent_number_file.write(
                    str(number["id"]) + ";" + str(number["tent"]) + "\n"
                )

    # save paid
    paid_obj = [{"id": p.identifier, "paid": p.paid} for p in arg_participants]

    with open(I_PAID, "w", encoding="utf-8") as paid_file:
        for obj in paid_obj:
            if obj["paid"] is True:
                paid_file.write(str(obj["id"]) + ";" + str(obj["paid"]) + "\n")

    # save revisions todo

    with open(I_REVISION, "a", encoding="utf-8") as revision_file:
        for revision in arg_revisions:
            revision_file.write(revision + "\n")

    arg_errors.clear()
    arg_participants, arg_revisions = parse_participants(
        I_PARICIPANT, I_TENT_NUMBERS, I_REVISION, I_PAID, arg_errors)
    arg_leaders = parse_tent_leader(I_TENT_LEADER, arg_errors)

    return arg_participants, arg_leaders


@ app.route("/api/participants", methods=["GET", "POST"])
def get_participants():
    """returns all participants as json"""
    global participants_d, tent_leaders, error_logs
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
            participants_d, tent_leaders, loc_revisions, error_logs)

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
                participants_d, tent_leaders, loc_revisions, error_logs)
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
    ret["errors"] = error_logs + configs_d.errors
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
    error_logs.clear()

    configs_d.load()
    participants_d, revison_logs = parse_participants(
        I_PARICIPANT, I_TENT_NUMBERS,
        I_REVISION, I_PAID, error_logs)
    tent_leaders = parse_tent_leader(I_TENT_LEADER, error_logs)
    participants_last_year = parse_participants_last_year(
        I_LAST_YEAR, participants_d, error_logs)

    app.run(host="0.0.0.0", port=8080, debug=True)
