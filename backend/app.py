"""main file of ZelteinteilungZL"""
import json
import os
import shutil
from datetime import datetime
from flask_cors import CORS
from flask import Flask, abort, jsonify, request, send_from_directory
from mailmerge import MailMerge
from docx2pdf import convert
import pythoncom
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
app.config["LISTS_OUTPUT"] = PATH.OUTPUT_DIR_LISTS


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


def create_dir_if_not_exist(arg_dir):
    """create dir if not exist"""
    if os.path.exists(arg_dir):
        shutil.rmtree(arg_dir)
    os.makedirs(arg_dir)


def generate_docx_and_pdf(arg_name, arg_path, arg_template_name, arg_rows):
    """write docx, pdf and csv file"""
    output_name = arg_name
    output_docx = output_name + ".docx"
    document = MailMerge(PATH.LIST_TEMPLATE_DIR + arg_template_name)

    document.merge_rows('tent', arg_rows)

    document.write(arg_path + output_docx)
    convert(arg_path + output_docx)


def generate_participants_array(arg_participants):
    """generate participants rows"""
    ret_rows = []

    for part in arg_participants:
        loc_row = {'tent': str(part.tent),
                   'lastname': part.lastname, 'firstname': part.firstname,
                   'birthdate': part.birthdate,
                   'street': part.street,
                   'zipcode': str(part.zipcode), 'village': part.village,
                   'emergencyContact': part.emergency_contact,
                   'emergencyNumber': part.emergency_phone,
                   'other': part.other}
        ret_rows.append(loc_row)

    return ret_rows


def generate_leader_array(arg_leader):
    """generate leader rows"""
    ret_rows = []
    for leader in arg_leader:
        loc_row = {'tent': str(leader.job),
                   'lastname': leader.lastname, 'firstname': leader.firstname,
                   'birthdate': leader.birthdate,
                   'street': leader.street,
                   'zipcode': str(leader.zipcode), 'village': leader.village,
                   'emergencyContact': "", 'emergencyNumber': "", 'other': leader.comment}
        ret_rows.append(loc_row)

    return ret_rows


def generate_csv(arg_name, arg_path, arg_part, arg_leader):
    """generate csv file"""
    # generate addresslist csv
    csv_rows = []
    csv_header = ["#", "Zelt", "Name", "Vorname", "Straße", "PLZ", "Ort"]
    csv_rows.append(";".join(csv_header)+"\n")

    # participants
    cnt_offset = 0
    for i, part in enumerate(arg_part):
        p_row = [str(i+1), str(part.tent), str(part.lastname),
                 str(part.firstname), str(part.street), str(part.zipcode), str(part.village)]
        csv_rows.append(";".join(p_row) + "\n")
        cnt_offset = i

    # leaders
        # participants
    for k, leader in enumerate(arg_leader):
        p_row = [str(k+cnt_offset+2), str(leader.job), str(leader.lastname),
                 str(leader.firstname), str(leader.street),
                 str(leader.zipcode), str(leader.village)]
        csv_rows.append(";".join(p_row) + "\n")

    csv_path = arg_path + arg_name+".csv"
    with open(csv_path, "w", ) as outfile:
        outfile.writelines(csv_rows)


def generate_overall_list():
    """generate overall list"""

    create_dir_if_not_exist(PATH.GESAMT_LISTS)
    # sort by lastname, firstname
    output_name = "2023_zeltlager_gesamtliste_sort_by_name"
    loc_sorted_participants = sorted(
        participants_d, key=lambda x: (x.lastname, x.firstname), reverse=False)
    rows_part = generate_participants_array(loc_sorted_participants)

    loc_sorted_tent_leaders = sorted(
        tent_leaders, key=lambda x: (x.lastname, x.firstname), reverse=False)
    rows_leaders = generate_leader_array(loc_sorted_tent_leaders)

    merge_rows = rows_part + rows_leaders

    generate_docx_and_pdf(output_name, PATH.GESAMT_LISTS,
                          "gesamtliste.docx", merge_rows)
    generate_csv(output_name, PATH.GESAMT_LISTS,
                 loc_sorted_participants, loc_sorted_tent_leaders)

    # sort by tent,lastname, firstname
    output_name = "2023_zeltlager_gesamtliste_sort_by_tent"
    loc_sorted_participants = sorted(
        participants_d, key=lambda x: (x.tent, x.lastname, x.firstname), reverse=False)
    rows_part = generate_participants_array(loc_sorted_participants)

    loc_sorted_tent_leaders = sorted(
        tent_leaders, key=lambda x: (x.job, x.lastname, x.firstname), reverse=False)
    rows_leaders = generate_leader_array(loc_sorted_tent_leaders)

    merge_rows = rows_part + rows_leaders

    generate_docx_and_pdf(output_name, PATH.GESAMT_LISTS,
                          "gesamtliste.docx", merge_rows)
    generate_csv(output_name, PATH.GESAMT_LISTS,
                 loc_sorted_participants, loc_sorted_tent_leaders)

    # generate


def calc_age_by_birthdate(arg_birthdate):
    """calcualte age by given birhtdate"""
    today = datetime.now()

    year, month, day = map(int, arg_birthdate.split('-'))
    birth_date = datetime(year, month, day)
    diff_seconds = (today - birth_date).total_seconds()
    age = diff_seconds / (60 * 60 * 24 * 365)
    return age


def generate_tent_leader_allocation():
    """generate list: tentleader to tent number allication"""

    loc_path = PATH.OUTPUT_DIR_LISTS
    # generate array
    allocation = []
    for i in range(configs_d.num_tents):
        allocation.append({"leaders": [], "age": [], })

    # add participants to tents
    for part in participants_d:
        if part.tent <= configs_d.num_tents:
            loc_age = calc_age_by_birthdate(part.birthdate)
            allocation[part.tent-1]["age"].append(loc_age)

    # calc avg age
    for i in range(len(allocation)):
        loc_sum = 0
        for age in allocation[i]["age"]:
            loc_sum += age
        allocation[i]["avg"] = round(loc_sum / len(allocation[i]["age"]), 2)

    for leader in tent_leaders:
        if leader.tent <= configs_d.num_tents:
            allocation[leader.tent-1]["leaders"].append(leader.get_fullname())

    csv_rows = []
    csv_header = ["Zelt", "Zefü", "Durchschnittsalter", "Haijkbegleiter", ]
    csv_rows.append(";".join(csv_header)+"\n")
    for i, tent in enumerate(allocation):
        p_row = [str(i+1), ",".join(tent["leaders"]), " "+str(tent["avg"]), ""]
        csv_rows.append(";".join(p_row) + "\n")

    csv_path = loc_path + "2023_zeltlager_zeltverteilung"+".csv"
    with open(csv_path, "w", ) as outfile:
        outfile.writelines(csv_rows)


def generate_speacial_lists():
    """generate list for sukus/medic (medicine,food allergy,...)"""

    if os.path.exists(PATH.SPECIAL_LISTS):
        shutil.rmtree(PATH.SPECIAL_LISTS)
    os.makedirs(PATH.SPECIAL_LISTS)

    loc_filterd_participants = filter(
        lambda x: x.other.strip() != "", participants_d)
    loc_sorted_participants = sorted(
        loc_filterd_participants, key=lambda x: (x.tent, x.lastname, x.firstname), reverse=False)

    rows_part = generate_participants_array(loc_sorted_participants)

    output_name = "2023_zeltlager_sani_liste"
    generate_docx_and_pdf(output_name, PATH.SPECIAL_LISTS,
                          "sani.docx", rows_part)
    generate_csv(output_name, PATH.SPECIAL_LISTS,
                 loc_sorted_participants, [])

    output_name = "2023_zeltlager_suku_liste"
    generate_docx_and_pdf(output_name, PATH.SPECIAL_LISTS,
                          "suku.docx", rows_part)
    generate_csv(output_name, PATH.SPECIAL_LISTS,
                 loc_sorted_participants, [])


@ app.route("/api/lists/generate/all", methods=["GET"])
def generate_lists():
    """generate all lists"""
    pythoncom.CoInitialize()
    create_dir_if_not_exist(PATH.OUTPUT_DIR_LISTS)
    generate_overall_list()
    generate_tent_leader_allocation()
    generate_speacial_lists()

    return jsonify("ok")


def get_files_in_directory(directory):
    """get files as list"""
    result = []
    for root, _, files in os.walk(directory):
        relative_root = os.path.relpath(root, directory)
        dir_info = {
            "dir_name": os.path.basename(root),
            "dir_link": "/lists/" + relative_root.replace("\\", "/")+"/",
            # Extract only the file names
            "files": [os.path.basename(file) for file in files]
        }
        result.append(dir_info)
    # Include files in the root directory
    root_files = [os.path.basename(file) for file in os.listdir(
        directory) if os.path.isfile(os.path.join(directory, file))]
    if root_files:
        root_info = {
            "dir_name": os.path.basename(directory),
            "dir_link": ".",
            "files": root_files
        }
        result.insert(0, root_info)
    result.pop(0)
    return result


@ app.route("/api/lists", methods=["GET"])
def get_lists():
    """get lists download lists"""

    files = []
    for root, _, filenames in os.walk(PATH.OUTPUT_DIR_LISTS):
        root_list = []
        for filename in filenames:
            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, PATH.OUTPUT_DIR_LISTS)
            root_list.append({"name": filename, "link": "/lists/" +
                              relative_path.replace(os.path.sep, '/')})
        files.append({"dir": root, "files": root_list})
    ret = get_files_in_directory(PATH.OUTPUT_DIR_LISTS)

    return jsonify(ret)


@ app.route("/api/lists/<path:filename>")
def download_list_file(filename):
    """returns map file by filename"""
    return send_from_directory(app.config["LISTS_OUTPUT"], filename)


if __name__ == "__main__":
    configs_d.load()
    participants_d, revison_logs = parse_participants(particpant_errors)
    tent_leaders = parse_tent_leader(tent_leader_errors)
    participants_last_year = parse_participants_last_year(
        participants_d, last_year_errors)

    app.run(host="0.0.0.0", port=8080, debug=True)
