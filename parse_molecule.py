import re

def mult_dict(thisdict, value):
    thisdict.update((x, y*value) for x, y in thisdict.items())
    return thisdict

def sum_dict(dict1, dict2):
    for key in set(dict1):
        if key in dict2:
            dict1[key] += dict2[key]
    for key in set(dict2):
        if key not in dict1:
            dict1[key] = dict2[key]
    return dict1

def parse_string(string):
    #comment line depending how we want to deal with unknow chara
    #return re.findall('[A-Z][a-z]?|\d+|[\{\(\[\]\)\}]', string)
    return re.findall('[A-Z][a-z]?|\d+|.', string)

def parse_molecule(string):
    level = 0
    symbol_stack = []
    tmp = [{}]
    last = 0
    tokens = parse_string(string)
    for token in tokens:
        if not token.isdecimal() and type(last) == dict:
            tmp[level] = sum_dict(tmp[level], last)
            last = 0

        #check if the string correspond an atome
        if len(token) <= 2 and token.istitle():
            #add to the coresponding level of tmp
            if token in tmp[level]:
                last = token
                tmp[level][token] += 1
                value = 1
            else:
                #create new atoms if does not exist
                last = token
                value = 1
                tmp[level][token] = 1
        #if the decimal followed a closing brackets mult all the value inside the bracket
        elif token.isdecimal():
            if type(last) is dict:
                last = mult_dict(last, int(token))
                tmp[level] = sum_dict(tmp[level], last)
                last = 0
            else:
                if not last:
                    raise Exception('quantifier without atom')
                else:
                    value = value * int(token) - 1
                    tmp[level][last] += value

        #symbol stack prevent the misuse of brackets
        elif token in '{[(':
            symbol_stack.append(token)
            level += 1
            tmp.append({})
        elif token in '}])':
            if (token == '}'  and symbol_stack[-1] == '{') or (token ==')' and symbol_stack[-1] =='(') or token == ']' and symbol_stack[-1] == '[':
                symbol_stack.pop()
                last = tmp.pop() 
                level -= 1
            else:
                raise Exception('Unbalanced Symbol')
        else:
            raise Exception('Unexpected character')
    
    #no quantifier or atom after bracket safety
    if type(last) == dict:
        tmp[level] = sum_dict(tmp[level], last)
        last = 0

    return tmp[0] 

