"""main file of ZelteinteilungZL"""
import json
import os

from flask_cors import CORS
from flask import Flask, abort, jsonify, request, send_from_directory
from mailmerge import MailMerge
from docx2pdf import convert
from src.lib.helpers import props
from src.participants.participants import get_paticipant_by_id, parse_participants,\
    parse_participants_last_year, save_data
from src.participants.participant_c import particpant_object_to_class

from src.maps import generate_maps
from src.config import Config
from src.mailing import mailing_routes
from src.tent_leaders.tent_leaders import parse_tent_leader
import pathes as PATH


tent_leaders = []
participants_d = []
configs_d = Config(PATH.CONFIG)

particpant_errors = []
tent_leader_errors = []
last_year_errors = []
revison_logs = []

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(mailing_routes)
app.config["MAPS_OUTPUT"] = "../output/output_maps"


@ app.route("/api/participants", methods=["GET", "POST"])
def get_participants():
    """returns all participants as json"""
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

        save_data(participants_d,  loc_revisions, particpant_errors)

    ret = []
    for loc_participant in participants_d:
        ret.append(props(loc_participant))
    return jsonify(ret)


@ app.route("/api/participant", methods=["GET", "POST"])
def get_participant():
    """returns participant by given id as json"""
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

            save_data(participants_d,  loc_revisions, particpant_errors)
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
            {"name": participant.get_fullname(), "friends": loc_friends, "tent": participant.tent})

    return jsonify(loc_stuebis)


@ app.route("/api/logs", methods=["GET"])
def get_logs():
    """returns logs"""
    ret = {}
    ret["errors"] = particpant_errors + configs_d.errors + \
        tent_leader_errors + last_year_errors
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


def create_list_output_if_not_exist():
    """create templatesl lists output dir"""
    if not os.path.exists(PATH.OUTPUT_DIR_LISTS):
        os.makedirs(PATH.OUTPUT_DIR_LISTS)


@ app.route("/api/lists/overall", methods=["GET"])
def generate_overall_list():
    """generate overall list"""
    with app.app_context():
        create_list_output_if_not_exist()

        output_name = "2023_zeltlager_gesamtliste"
        output_docx = output_name + ".docx"
        document = MailMerge(PATH.LIST_TEMPLATE_DIR + "gesamtliste.docx")

        merge_rows = []

        loc_sorted_participants = sorted(
            participants_d, key=lambda x: x.lastname, reverse=False)

        for part in loc_sorted_participants:
            loc_row = {'tent': str(part.tent),
                       'lastname': part.lastname, 'firstname': part.firstname,
                       'birthdate': part.birthdate,
                       'street': part.street,
                       'zipcode': str(part.zipcode), 'village': part.village,
                       'emergencyContact': part.emergency_contact,
                       'emergencyNumber': part.emergency_phone,
                       'other': part.other}
            merge_rows.append(loc_row)

        for leader in tent_leaders:
            loc_row = {'tent': str(leader.job),
                       'lastname': leader.lastname, 'firstname': leader.firstname,
                       'birthdate': leader.birthdate,
                       'street': leader.street,
                       'zipcode': str(leader.zipcode), 'village': leader.village,
                       'emergencyContact': "", 'emergencyNumber': "", 'other': leader.comment}
            merge_rows.append(loc_row)
        document.merge_rows('tent', merge_rows)

        document.write(PATH.OUTPUT_DIR_LISTS + output_docx)
        convert(PATH.OUTPUT_DIR_LISTS + output_docx)

        # generate addresslist csv

        csv_rows = []
        csv_header = ["#", "Zelt", "Name", "Vorname", "Straße", "PLZ", "Ort"]
        csv_rows.append(";".join(csv_header)+"\n")
        for i, part in enumerate(loc_sorted_participants):
            p_row = [str(i+1), str(part.tent), str(part.lastname),
                     str(part.firstname), str(part.street), str(part.zipcode), str(part.village)]
            csv_rows.append(";".join(p_row) + "\n")

        csv_path = PATH.OUTPUT_DIR_LISTS + output_docx.replace("docx", "csv")
        with open(csv_path, encoding="utf-8" "w") as outfile:
            outfile.writelines(csv_rows)

    return jsonify("ok")


if __name__ == "__main__":
    configs_d.load()
    participants_d, revison_logs = parse_participants(particpant_errors)
    tent_leaders = parse_tent_leader(tent_leader_errors)
    participants_last_year = parse_participants_last_year(
        participants_d, last_year_errors)

    app.run(host="0.0.0.0", port=8080, debug=True)
