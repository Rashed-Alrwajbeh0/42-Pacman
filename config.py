from enum import Enum
import json
from typing import Any, cast

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
    "This class contain the default values of the configurations"
    Highscore_filename = "output"
    Lives = 3
    Pacgum = 50
    Points_per_pacgum = 10
    Points_per_super_pacgum = 50
    Points_per_ghost = 200
    Level_max_time = 120
    Levels = {"height": 25, "width": 25}


def error_value_warning(var: str, data: Any, default: Any) -> None:
    "This function just print the warning when the value on "
    "any configuration like the time is invalid in the json file"
    print(
        f'Warning: The {var}\'s value that you enter witch is :"{data}" '
        f"is invalid !! So the default value of {var} "
        f'which is:"{default}" will be used'
    )


def non_existing_warning(var: str, default: Any) -> None:
    "This function just print the warning when the value on "
    "any configuration like the time is not exist invalid in the json file"
    print(
        f"Warning: You are not enter any value of {var} !!"
        f" So the default value of {var} "
        f'which is: "{default}" will be used'
    )


def validate_int(
        var: str,
        data: Any,
        default: defaults,
        min_num: int = 0) -> tuple[int, int]:
    "This function validate the int and check if it has a "
    "valid value and more than the min_num in the parameter"
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
    "This is the class wicth is controls all the configurations valus"
    highscore_filename: str = Field(default=defaults.Highscore_filename.value)
    lives: int = Field(default=defaults.Lives.value)
    pacgum: int = Field(default=defaults.Pacgum.value)
    points_per_pacgum: int = Field(default=defaults.Points_per_pacgum.value)
    points_per_super_pacgum: int = Field(
        default=defaults.Points_per_super_pacgum.value
    )
    points_per_ghost: int = Field(default=defaults.Points_per_ghost.value)
    level_max_time: int = Field(default=defaults.Level_max_time.value)
    levels: dict[str, int] = defaults.Levels.value

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def highscore_filename_validate(cls, data: Any) -> str:
        "This functions validate the highscore_filename"
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
            return cast(str, data)
        non_existing_warning(
            "highscore_filename", defaults.Highscore_filename.value
        )
        return defaults.Highscore_filename.value

    @field_validator("lives", mode="before")
    @staticmethod
    def lives_validator(data: Any) -> int:
        "This function validate the lives of the pacman, if "
        "it is more than zero or numaric value ...etc"
        return validate_int("lives", data, defaults.Lives)[0]

    @field_validator("pacgum", mode="before")
    @staticmethod
    def pacgum_validator(data: Any) -> int:
        "This function validate the pacgum number, if "
        "it is more than zero or numaric value ...etc"
        return validate_int("pacgum", data, defaults.Pacgum, 3)[0]

    @field_validator("points_per_pacgum", mode="before")
    @staticmethod
    def points_per_pacgum_validate(data: Any) -> int:
        "This function validate the points_per_pacgum number, if "
        "it is more than zero or numaric value ...etc"
        return validate_int(
            "points_per_pacgum", data, defaults.Points_per_pacgum
        )[0]

    @field_validator("points_per_super_pacgum", mode="before")
    @staticmethod
    def points_per_super_pacgum_validator(data: Any) -> int:
        "This function validate the points_per_super_pacgum number, if "
        "it is more than zero or numaric value ...etc"
        return validate_int(
            "points_per_super_pacgum",
            data,
            defaults.Points_per_super_pacgum,
        )[0]

    @field_validator("points_per_ghost", mode="before")
    @staticmethod
    def points_per_ghost_validator(data: Any) -> int:
        "This function validate the points_per_ghost number, if "
        "it is more than zero or numaric value ...etc"
        return validate_int(
            "points_per_ghost", data, defaults.Points_per_ghost
        )[0]

    @field_validator("level_max_time", mode="before")
    @staticmethod
    def level_max_time_validator(data: Any) -> int:
        "This function validate the level_max_time, if "
        "it is more than zero or numaric value ...etc"
        return validate_int(
            "level_max_time", data, defaults.Level_max_time
        )[0]


def read_json(FileName: str) -> confing:
    "This function open the json file that contain the configurations and "
    "make an object of the confing class witch validata all the values"
    try:
        with open(FileName, "r") as file:
            lines = [ln for ln in file
                     if not ln.strip().startswith(("#", "//"))]
            data = json.loads("".join(lines))
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
