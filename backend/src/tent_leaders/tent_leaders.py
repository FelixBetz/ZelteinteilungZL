"""functions related to tent_leaders"""

import os
import csv
from datetime import datetime
from src.lib.helpers import strip_row
import pathes as PATH
import file_indices as IDX
from .tent_leader_c import TentLeader
import pandas as pd


def parse_tent_leader(arg_errors):
    """parses zeltlager tent leader from input csv file"""
    loc_tent_leaders = []

    if not os.path.isfile(PATH.TENT_LEADER):
        arg_errors.append("ERROR: " + PATH.TENT_LEADER + " existiert nicht")
        print("ERROR: " + PATH.TENT_LEADER + " existiert nicht")
        return loc_tent_leaders

    data = pd.read_excel(PATH.TENT_LEADER, sheet_name="Team_Lager")

    data.fillna("", inplace=True)
    loc_id = 0
    for index, row in data.iterrows():
        loc_lastname = row[IDX.LEAD_LAST_NAME].strip()
        loc_firstname = row[IDX.LEAD_FIRST_NAME].strip()

        # parse zip code
        try:
            loc_zipcode = int(row[IDX.LEAD_ZIP_CODE])
        except:
            print(
                "ERROR: failed to parse zip code: ",
                index,
                loc_firstname,
                " ",
                loc_lastname,
            )
            raise

        # parse tent number
        if row[IDX.LEAD_TENT] == "":
            loc_tent = 9999
        else:
            try:
                loc_tent = int(row[IDX.LEAD_TENT])
            except:
                print(
                    "ERROR: failed to parse tent number: ",
                    row[IDX.LEAD_TENT],
                    "row: ",
                    row,
                )
                raise
        loc_birthdate = ""
        try:
            loc_birthdate = str(row[IDX.LEAD_BIRTHDATE].strftime("%Y-%m-%d"))

        except:
            print(
                "failed to parse birthdate: i: ",
                index,
                loc_firstname,
                " ",
                loc_lastname,
                loc_birthdate,
            )
            raise

        try:
            if row[IDX.LEAD_HAIJK] == "":
                loc_haijk = 9999
            else:
                loc_haijk = int(row[IDX.LEAD_HAIJK])
        except:
            print(
                "ERROR: failed to parse Haijk tent number: ",
                row[IDX.LEAD_HAIJK],
                "row: ",
                row,
            )
            raise

        loc_tent_leader = TentLeader(
            loc_id,
            row[IDX.LEAD_JOB],
            loc_lastname,
            loc_firstname,
            row[IDX.LEAD_STREET],
            loc_zipcode,
            row[IDX.LEAD_VILLAGE],
            "",  # phone: not used anymore
            row[IDX.LEAD_HANDY],
            row[IDX.LEAD_MAIL],
            loc_birthdate,
            loc_tent,
            row[IDX.LEAD_TEAM],
            loc_haijk,
            row[IDX.LEAD_COMMENT],
        )
        loc_id += 1

        loc_tent_leaders.append(loc_tent_leader)
    return loc_tent_leaders
