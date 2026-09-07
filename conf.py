from enum import Enum
import json
from pydantic import BaseModel, Field, field_validator


ConfigurationKeys = [
    "highscore_filename",
    "lives",
    "pacgum",
    "points_per_pacgum",
    "points_per_super_pacgum",
    "points_per_ghost",
    "level_max_time",
]


class defaults(Enum):
    Highscore_filename = "output"
    Lives = 3
    Pacgum = 50
    Points_per_pacgum = 10
    Points_per_super_pacgum = 50
    Points_per_ghost = 200
    Level_max_time = 120
    Levels = {"height": 25, "width": 25}


def error_value_warning(var, data, default):
    print(
        f'Warning: The {var}\'s value that you enter witch is :"{data}" '
        f"is invalid !! So the default value of {var} "
        f'which is:"{default}" will be used'
    )


def non_existing_warning(var, default):
    print(
        f"Warning: You are not enter any value of {var} !!"
        f" So the default value of {var} "
        f'which is: "{default}" will be used'
    )


def validate_int(var, data, default, min_num = 0):
    if data is not None and data != "":
        try:
            temp = int(float(data))
            if temp <= min_num:
                error_value_warning(
                    var, data, default.value
                )
                return default.value, 0
            return temp, 1
        except (ValueError, TypeError):
            error_value_warning(
                var, data, default.value
            )
            return default.value, 0
    non_existing_warning(
        var, default.value
    )
    return default.value, 0


class confing(BaseModel):
    highscore_filename: str = Field(default=defaults.Highscore_filename.value)
    lives: int = Field(default=defaults.Lives.value)
    pacgum: int = Field(default=defaults.Pacgum.value)
    points_per_pacgum: int = Field(default=defaults.Points_per_pacgum.value)
    points_per_super_pacgum: int = Field(
        default=defaults.Points_per_super_pacgum.value
    )
    points_per_ghost: int = Field(default=defaults.Points_per_ghost.value)
    level_max_time: int = Field(default=defaults.Level_max_time.value)
    levels: list[dict[str, int]] = defaults.Levels.value

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def highscore_filename_validate(cls, data):
        if data is not None:
            temp = str(data).strip()
            data = temp
            if len(data) <= 0:
                error_value_warning(
                    "highscore_filename",
                    data,
                    defaults.Highscore_filename.value,
                )
                return defaults.Highscore_filename.value
            return data
        non_existing_warning(
            "highscore_filename", defaults.Highscore_filename.value
        )
        return defaults.Highscore_filename.value

    @field_validator("lives", mode="before")
    @staticmethod
    def lives_validator(data):
        return validate_int("lives", data, defaults.Lives)[0]

    @field_validator("pacgum", mode="before")
    @staticmethod
    def pacgum_validator(data):
        return validate_int("pacgum", data, defaults.Pacgum, 3)[0]

    @field_validator("points_per_pacgum", mode="before")
    @staticmethod
    def points_per_pacgum_validate(data):
        return validate_int(
            "points_per_pacgum", data, defaults.Points_per_pacgum
        )[0]

    @field_validator("points_per_super_pacgum", mode="before")
    @staticmethod
    def points_per_super_pacgum_validator(data):
        return validate_int(
            "points_per_super_pacgum",
            data,
            defaults.Points_per_super_pacgum,
        )[0]

    @field_validator("points_per_ghost", mode="before")
    @staticmethod
    def points_per_ghost_validator(data):
        return validate_int(
            "points_per_ghost", data, defaults.Points_per_ghost
        )[0]

    @field_validator("level_max_time", mode="before")
    @staticmethod
    def level_max_time_validator(data):
        return validate_int(
            "level_max_time", data, defaults.Level_max_time
        )[0]

    def info(self):
        print(f"highscore_filename : {self.highscore_filename}")
        print(f"lives : {self.lives}")
        print(f"pacgum : {self.pacgum}")
        print(f"points_per_pacgum : {self.points_per_pacgum}")
        print(f"points_per_super_pacgum : {self.points_per_super_pacgum}")
        print(f"points_per_ghost : {self.points_per_ghost}")
        print(f"level_max_time : {self.level_max_time}")
        print(f"levels : {self.levels}")


def read_json(FileName):
    try:
        with open(FileName, "r") as file:
            data = dict()
            data = json.load(file)
            sorted_data = dict()
            for i in data.keys():
                if i.lower() not in ConfigurationKeys:
                    print(f"Warning: The \"{i}\" key is invalid !!")
                    continue
                sorted_data[i.lower()] = data[i]
            return confing(**sorted_data)
        return confing()
    except Exception:
        print(f"Warning: There is invalid values in the {FileName} file"
              ", so the default values will be used !")
        return confing()
