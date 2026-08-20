from enum import Enum
from pydantic import BaseModel, Field, field_validator


class defaults(Enum):
    Highscore_filename = "output"
    Lives = 3
    Pacgum = 50
    Points_per_pacgum = 10
    Points_per_super_pacgum = 50
    Points_per_ghost = 200
    Level_max_time = 120
    Levels = [
        {"level_number": i, "height": 10 * i, "width": 10 * i}
        for i in range(1, 11)
    ]


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


def validate_int(var, data, default):
    if data is not None and data != "":
        try:
            temp = int(data)
            if temp <= 0:
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
    levels: list[dict[str, int]] | None = Field(default=defaults.Levels.value)

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
    @classmethod
    def lives_validator(cls, data):
        return validate_int("lives", data, defaults.Lives)[0]

    @field_validator("pacgum", mode="before")
    @classmethod
    def pacgum_validator(cls, data):
        return validate_int("pacgum", data, defaults.Pacgum)[0]

    @field_validator("points_per_pacgum", mode="before")
    @classmethod
    def points_per_pacgum_validate(cls, data):
        return validate_int(
            "points_per_pacgum", data, defaults.Points_per_pacgum
        )[0]

    @field_validator("points_per_super_pacgum", mode="before")
    @classmethod
    def points_per_super_pacgum_validator(cls, data):
        return validate_int(
            "points_per_super_pacgum",
            data,
            defaults.Points_per_super_pacgum,
        )[0]

    @field_validator("points_per_ghost", mode="before")
    @classmethod
    def points_per_ghost_validator(cls, data):
        return validate_int(
            "points_per_ghost", data, defaults.Points_per_ghost
        )[0]

    @field_validator("level_max_time", mode="before")
    @classmethod
    def level_max_time_validator(cls, data):
        return validate_int(
            "level_max_time", data, defaults.Level_max_time
        )[0]

    @field_validator("levels", mode="before")
    @classmethod
    def levels_validator(cls, data):
        if data:
            levels_list = list()
            for level in data:
                level_dict = dict()
                temp1, temp2 = validate_int(
                        "levels", level["level_number"], defaults.Levels
                        )
                if not temp2:
                    return defaults.Levels.value
                else:
                    level_dict["level_number"] = temp1

                temp1, temp2 = validate_int(
                        "levels", level["height"], defaults.Levels
                        )
                if not temp2:
                    return defaults.Levels.value
                else:
                    level_dict["height"] = temp1

                temp1, temp2 = validate_int(
                        "levels", level["width"], defaults.Levels
                        )
                if not temp2:
                    return defaults.Levels.value
                else:
                    level_dict["width"] = temp1

                levels_list.append(level_dict)
            return levels_list
