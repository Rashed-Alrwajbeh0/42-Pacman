from read import read_the_json_file
from conf import confing
conf_dict = {
        "highscore_filename": None,
        "lives": None,
        "pacgum": None,
        "points_per_pacgum": None,
        "points_per_super_pacgum": None,
        "points_per_ghost": None,
        "level_max_time": None,
        "levels": None
        }
read_the_json_file("conf.json", conf_dict)
configuration = confing(**conf_dict)
print(configuration.highscore_filename)
print(configuration.lives)
print(configuration.pacgum)
print(configuration.points_per_pacgum)
print(configuration.points_per_super_pacgum)
print(configuration.points_per_ghost)
print(configuration.level_max_time)
print(configuration.levels)
