import sys, os
import json

JSON2JSON = "j2j"
HTML2JSON = "h2j"
JSON2HTML = "j2h"
ALL_TYPES = {JSON2JSON, JSON2HTML, HTML2JSON}

convert_type = JSON2HTML
path = "file.json"
if len(sys.argv) > 1:
    path = sys.argv[1]
    if len(sys.argv) == 3:
        convert_type = sys.argv[2]
        if convert_type not in ALL_TYPES:
            raise Exception(f"Тип форматирования '{convert_type}' не верен, выберете один из списка {ALL_TYPES} ")

global res_f
cnt_list = 0
cnt_dict = 0


def ver_filename(fn, ext):
    i = 1
    res = fn + "_" + str(i).rjust(3, "0") + "." + ext
    while os.path.isfile(res):
        i += 1
        res = fn + "_" + str(i).rjust(3, "0") + "." + ext
    return res


def format_val(s):
    if type(s) is str:
        print("\n" in s)
        return '"' + s + '"'
    else:
        return str(s)


def rec(s):
    global cnt_dict, cnt_list, res_f
    if type(s) is dict:
        typ = "dict"
        res_f.write("{")
        cnt_dict += 1
        i = cnt_dict
        first = True
        for key, value in s.items():
            if first:
                first = False
            else:
                res_f.write(",")
            res_f.write(format_val(key) + ':')
            rec(value)
        res_f.write("}")
    elif type(s) is list:
        typ = "list"
        res_f.write("[")
        cnt_list += 1
        i = cnt_list
        first = True
        for value in s:
            if first:
                first = False
            else:
                res_f.write(",")
            rec(value)
        res_f.write("]")
    else:
        res_f.write(format_val(s))


def rec_json2json(s):
    global cnt_dict, cnt_list, res_f
    if type(s) is dict:
        res = {}
        for key, value in s.items():
            res[key] = value
    elif type(s) is list:
        res = []
        for value in s:
            res.append(value)
    else:
        res = s
    return res


def rec_to_html(s):
    if type(s) is dict:
        typ = "dict"
        res_f.write("{")
        cnt_dict += 1
        i = cnt_dict
        first = True
        for key, value in s.items():
            if first:
                first = False
            else:
                res_f.write(",")
            res_f.write(format_val(key) + ':')
            rec(value)
        res_f.write("}")
    elif type(s) is list:
        typ = "list"
        res_f.write("[")
        cnt_list += 1
        i = cnt_list
        first = True
        for value in s:
            if first:
                first = False
            else:
                res_f.write(",")
            rec(value)
        res_f.write("]")
    else:
        res_f.write(format_val(s))


def export_json2json(data, res_path):
    with open(res_path, "w", encoding="utf-8") as res_f:
        res = rec_json2json(data)
        print(res)
        # https://ru.stackoverflow.com/questions/584129/%d0%9a%d0%b0%d0%ba-%d0%be%d1%82%d0%ba%d0%bb%d1%8e%d1%87%d0%b8%d1%82%d1%8c-%d0%b7%d0%b0%d0%bc%d0%b5%d0%bd%d1%83-%d0%ba%d0%b8%d1%80%d0%b8%d0%bb%d0%bb%d0%b8%d1%86%d1%8b-%d0%bd%d0%b0-uxxxx-%d0%b2-%d1%81%d1%82%d1%80%d0%be%d0%ba%d0%b0%d1%85-%d0%bf%d1%80%d0%b8-%d0%ba%d0%be%d0%bd%d0%b2%d0%b5%d1%80%d1%82%d0%b0%d1%86%d0%b8%d0%b8-%d0%b2-json
        res_str = json.dumps(res, ensure_ascii=False, separators=(',', ':'))
        res_f.write(res_str)


if __name__ == '__main__':
    res_path = ver_filename(path[:-5], "json")
    with open(path, "r", encoding='utf-8') as json_f:
        data = json.load(json_f)
    with open(res_path, "w", encoding='utf-8') as res_f:
        rec(data)

    print(res_path)
