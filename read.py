def super_strip(text):
    if len(text) <= 0:
        return text
    while(not text[0].isalnum()):
        text = text.strip(text[0])
    while(not text[-1].isalnum()):
        text = text.strip(text[-1])
    return text




def check_line(line, index_of_seperator, conf_dict, keys_list, end_list = None, answer = None):
    if line[0] == "#":
        return "#"
    if len(line)-1 == index_of_seperator:
        print(f"Warning: key:{key} without value !!")
        return "-"
    if index_of_seperator != -2:
        key = super_strip(line[:index_of_seperator]).lower()
        value = super_strip(line[index_of_seperator+1:]).lower()
        if key not in keys_list:
            print(f"Warning: Unknown key {key} !!")
            return "-"
        if key == "levels":
            value = super_strip(value)
            value += ","
            return value
        conf_dict[key] = value
        return "-"
    else:
        if end_list:
            if len(line)-1 != end_list:
                print(f"Warning: Unknown value:\n{line}")
                return "-"
            value = super_strip(line)
            answer = list(line.split(","))
            return "-"
        else:
            value = super_strip(line)
            value += ","
            return line




def read_the_json_file(TheFileName: str, conf_dict):
    file = open(TheFileName, "r")
    text = file.read()
    keys_list = list(conf_dict.keys())
    line = ""
    idx = 0
    stop = False
    rest_line = None
    levels_list = []
    end_list_idx = None
    for i in text:
        if i == '\n':
            if rest_line:
                if end_list_idx:
                    temp = check_line(rest_line + line, -2, conf_dict, keys_list, rest_line + end_list_idx, levels_list)
                else:
                    temp = check_line(rest_line + line, -2, conf_dict, keys_list)
            else:
                temp = check_line(line, idx, conf_dict, keys_list)
            if temp == "-":
                line = ""
                rest_line = None
                end_list_idx = None
                stop = False
                idx = 0
                if len(levels_list):
                    conf_dict["levels"] = levels_list
            else:
                rest_line = temp
        if not stop:
            idx += 1
        if i == ":":
            stop = True
        if i == "]":
            end_list_idx = i
        line += i
