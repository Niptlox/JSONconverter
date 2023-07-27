import sys
import json

path ="file.json"

if len(sys.argv) > 1:
    path = sys.argv[1]
res_path = path[:-5] + ".html"

global res_f
cnt_list = 0
cnt_dict = 0


def format_val(s):
    if type(s) is str:
        return '"' + s + '"'
    else:
        return s


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
            res_f.write(format_val(key)+':')
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

    res = f"<div id='{typ}_{i}'>"


if __name__ == '__main__':
    with open(path, encoding='utf-8') as json_f:
        data = json.load(json_f)
    with open(res_path, encoding='utf-8') as res_f:
        rec(data)

