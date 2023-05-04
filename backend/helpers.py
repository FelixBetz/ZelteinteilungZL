"""collections of useful stuff"""
import inspect
from enum import Enum


class MailType(Enum):
    """ENUM for all mail types"""
    MASS_MAIL = 0
    PERSONALIZED_MAIL = 1
    TEMPLATE_MAIL = 2


def strip_row(arg_row):
    """strip_row"""
    for i, col in enumerate(arg_row):
        arg_row[i] = col.replace('"', "").strip()


def parse_yes_no(arg_string):
    """parses formular ja/zugestimmt to boolean"""
    arg_string = arg_string.strip().lower()
    if arg_string in ("ja", "zugestimmt", "vegetarisch", "ermäßigt", "erlaubt"):
        return True
    return False


def bool_to_tex_yes_no(arg_bool):
    """parse bool to 'ja' or 'nein' string"""
    if arg_bool:
        return "ja"
    return "nein"


def bool_to_text_zugestimmt(arg_bool):
    """parse bool to 'zugestimmt' or 'nein' nicht zugestimmt"""
    if arg_bool:
        return "zugestimmt"
    return "nicht zugestimmt"


def is_paided(arg_paided):
    """is paided"""
    if arg_paided in ["true", "True"]:
        return True
    return False


def props(obj):
    """converts class object into an dictonary"""
    props_dict = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith("__") and not inspect.ismethod(value):
            props_dict[name] = value
    return props_dict
