"""functions related to tent_leaders"""
import os
import csv
from datetime import datetime
from helpers import strip_row
import file_indices as IDX
from .tent_leader_c import TentLeader


def parse_tent_leader(arg_file_name):
    """parses zeltlager tent leader from input csv file"""

    loc_tent_leaders = []
    loc_errors = []

    if not os.path.isfile(arg_file_name):
        loc_errors.append(
            "ERROR: " + arg_file_name + " existiert nicht")
        print("ERROR: " + arg_file_name + " existiert nicht")
        return loc_tent_leaders

    with open(arg_file_name, newline="", encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        loc_id = 0
        for i, row in enumerate(spamreader):
            if i >= 1:
                strip_row(row)

                loc_lastname = row[IDX.LEAD_LAST_NAME]
                loc_firstname = row[IDX.LEAD_FIRST_NAME]

                # parse zip code
                try:
                    loc_zipcode = int(row[IDX.LEAD_ZIP_CODE])
                except:
                    print("ERROR: failed to parse zip code: i: ",
                          i, loc_firstname, " ", loc_lastname,)
                    raise

                # parse tent number
                if row[IDX.LEAD_TENT] == "":
                    loc_tent = 9999
                else:
                    try:
                        loc_tent = int(row[IDX.LEAD_TENT])
                    except:
                        print("ERROR: failed to parse tent number: ",
                              row[IDX.LEAD_TENT], "row: ", row,)
                        raise
                loc_birthdate = ""
                try:
                    loc_time_string = datetime.strptime(
                        row[IDX.LEAD_BIRTHDATE], "%d.%m.%Y"
                    ).date()
                    _ = loc_time_string.timetuple()
                    loc_birthdate = str(loc_time_string)

                except:
                    print("failed to parse birthdate: i: ",
                          i, loc_firstname, " ", loc_lastname, loc_birthdate)
                    raise

                loc_tent_leader = TentLeader(
                    loc_id,
                    row[IDX.LEAD_JOB],
                    loc_lastname,
                    loc_firstname,
                    row[IDX.LEAD_STREET],
                    loc_zipcode,
                    row[IDX.LEAD_VILLAGE],
                    row[IDX.LEAD_PHONE],
                    row[IDX.LEAD_HANDY],
                    row[IDX.LEAD_MAIL],
                    loc_birthdate,
                    loc_tent,
                    row[IDX.LEAD_TEAM],
                    row[IDX.LEAD_COMMENT],
                )
                loc_id += 1

                loc_tent_leaders.append(loc_tent_leader)

        print("parsed input file: ", arg_file_name)
    return loc_tent_leaders, loc_errors
