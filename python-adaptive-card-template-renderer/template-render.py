import re
import json

def eval(p1,p2,boolean_operator):
    #TODO need to cover more typecases
    try:
        p1 = int(p1)
    except:
        pass
    try:
        p2 = int(p2)
    except:
        pass
    if boolean_operator == "==":
        return p1 == p2
    if boolean_operator == "!=":
        return p1 != p2
    if boolean_operator == ">":
        return p1 > p2
    if boolean_operator == ">=":
        return p1 >= p2
    if boolean_operator == "<":
        return p1 < p2
    if boolean_operator == "<=":
        return p1 <= p2
    if boolean_operator == "&&":
        return p1 and p2
    if boolean_operator == "||":
        return p1 or p2



def pattern_is_array(pattern):
    m = re.search(r'\[([0-9]+)\]',pattern)
    if m is None:
        return False
    return True

def get_value(m,data,logical_operator=None, compare_value = None):
    logic_operators = {"==","!=",">",">=","<","<=","&&","||"}

    #idea: Path to a value x.y.z. If there is a logical operator for example
    # x.y.z == 111
    # we extract the 111 and set m as x.y.z but, set logical_operator as ==, and compare_value as 111
    # so at the end of the recursion, we use compare y return boolean value.
    # if no logical operator, compare_value is set as -1, so we know we dont have to look for logical operators in recursion
    #do the first time, else -1
    if logical_operator is None:
        for lo in logic_operators:
            if lo in m:
                logical_operator = lo
                spl = m.split(lo)
                m = spl[0].strip()
                compare_value = spl[1].strip()
                break

    if logical_operator is None:
        logical_operator = -1


    splt_m = m.split(".")
    if len(splt_m) == 1:
        if pattern_is_array(splt_m[0]):
            arr_name = re.sub(r'\[([0-9]+)\]', "", splt_m[0])
            index = re.search(r'\[([0-9]+)\]', splt_m[0]).group(0)
            index = index.replace("[", "")
            index = index.replace("]", "")
            if logical_operator != -1:
                return eval(data[arr_name][int(index)],compare_value,logical_operator)
            return data[arr_name][int(index)]
        if logical_operator != -1:
            print("logical_operator ", logical_operator )
            print("compare_value ", compare_value)
            return eval(data[splt_m[0]],compare_value,logical_operator)
        return data[splt_m[0]]
    else:
        if pattern_is_array(splt_m[0]):
            arr_name = re.sub(r'\[([0-9]+)\]',"",splt_m[0])
            index = re.search(r'\[([0-9]+)\]',splt_m[0]).group(0)
            index = index.replace("[","")
            index = index.replace("]", "")
            return get_value(m.replace(splt_m[0] + ".", ""), data[arr_name][int(index)],logical_operator=logical_operator,compare_value=compare_value)

        return get_value(m.replace(splt_m[0]+".",""),data[splt_m[0]])

def render(data,template):
    str_template = json.dumps(template)
    matches = re.findall(r'\$\{(.*?)\}',str_template)
    for m in matches:
        # m value we want to remplace in template
        #data extracted from data, given m
        value = str(get_value(m,data))
        #replace value in text and
        str_template = str_template.replace(m,value)
        str_template = str_template.replace("${"+value+"}", value)

    #once text replaced, convert to json and return.
    body = json.loads(str_template)

    return body