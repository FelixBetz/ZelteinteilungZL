"""implementations of the class Config"""
import json


class Config:
    """represents data of a zeltlager participant"""

    def __init__(self, arg_filepath):
        self.filepath = arg_filepath
        self.num_tents = 15
        self.zl_start = "2021-08-01"
        self.errors = []

    def __str__(self):
        ret_str = (
            "---------------------------\n" +
            "Configs: \n"
            "  num_tents: " + str(self.num_tents) + "\n" +
            "  zl_start: " + str(self.zl_start) + "\n" +
            "---------------------------"
        )
        return ret_str

    def get_dict(self):
        """get configs as dictonary"""
        loc_dict = {}
        loc_dict["numTents"] = self.num_tents
        loc_dict["zlStart"] = self.zl_start

        return loc_dict

    def save(self):
        """save to file"""
        with open(self.filepath, "w", encoding="utf-8") as config_file:
            json.dump(self.get_dict(), config_file, indent=2)

    def load(self):
        """load configs from file"""
        with open(self.filepath, newline="", encoding="utf-8") as config_file:
            loc_config = json.load(config_file)

            # parse numTents
            try:
                self.num_tents = int(loc_config["numTents"])
            except KeyError:
                self.errors.append("Config ERROR: \"numTents\" nicht gefunden")
            except ValueError:
                self.errors.append(
                    "Config ERROR: \"numTents\" => \"" + loc_config["numTents"] +
                    "\" ist keine Zahl")
            # parse ZL start
            try:
                self.zl_start = loc_config["zlStart"]
            except KeyError:
                self.errors.append("Config ERROR: \"zlStart\" nicht gefunden")
