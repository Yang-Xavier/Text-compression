import argparse
import array
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-s', type=str, help='Symbol')
parser.add_argument('input', type=str, help="Input file")
args = parser.parse_args()

def build_huff(terms):
    result = {}
    def iterate(code, tree):
        if isinstance(tree,str):
            result[tree] = code
            return
        iterate(code+'0',tree['0'])
        iterate(code+'1',tree['1'])

    while (len(terms) != 1) :
        min1 = terms[0]
        min2 = terms[1]
        terms.append(({'0':min1[0],'1':min2[0]}, min1[1]+min2[1]))
        del terms[0]
        del terms[0]
        terms = sorted(terms, key=lambda x:x[1])
    iterate('',terms[0][0])
    return result

def convert_binary(huff_str):
    data = array.array('B')
    for i in range(0,len(huff_str), 8):
        data.append(int(huff_str[i:i+8],2))
    return data

def store(file_path,huff_str):
    data = convert_binary(huff_str)
    with open(file_path+".test","wb") as f:
             data.tofile(f)

    return

def format_data(init_data):
    term_array = {}
    for c in init_data:
        if c not in term_array:
            term_array[c] = 1
        else:
            term_array[c] += 1
    return term_array


# ________main__________

if "s" in args and "input" in args:
    symbol = args.s
    file_path  = args.input
    text = ""

    with open(file_path) as f:
        text = f.read()
    if symbol == "char":
        term_array = format_data(text)
    if symbol == 'word':
        word_pattern = re.compile(r'([a-z]+)', re.I)
        symbol_pattern = re.compile(r'[^a-z]{1}',re.I)
        word_r = word_pattern.findall(text)
        symbol_r = symbol_pattern.findall(text)
        word_r.extend(symbol_r)
        term_array = format_data(word_r)

    term_array = sorted(term_array.items(), key=lambda c: c[1])
    terms_huff=build_huff(term_array)

    huff_str = ""
    if symbol == "char":
        for c in text:
            huff_str+=terms_huff[c]
    store(file_path,huff_str)
    # print(terms_huff)
    # compress(args.s,args.input)
    # terms, text = init_data(symbol ,file_path)
    # terms_huff = build_huff(terms)
    # huff_str = ""
    # for c in text:
    #     huff_str+=terms_huff[c]
    # store(file_path,huff_str)
else:
    sys.exit()