"""functions related to participants"""
import file_indices as IDX


def check_if_participant_file_valid(arg_input_file):
    """check_if_participant_file_valid"""
    # check number of semicolons
    with open(arg_input_file, newline="", encoding="utf-8") as csvfile:
        for check_row in csvfile:
            cnt_semicolon = check_row.count(";")
            if cnt_semicolon != IDX.ROWS_PARP:
                raise Exception("ERROR at row:" + str(check_row))


def get_paticipant_by_id(arg_participants, arg_id):
    """returns participant by given id"""
    for loc_participant in arg_participants:
        if loc_participant.identifier == arg_id:
            return loc_participant
    return None
