import array, argparse, re,time, pickle,sys, copy

def build_huffman(terms):
    result = {}
    def iterate(code, tree):
        if isinstance(tree,str):
            result[tree] = code
            return
        iterate(code+'0',tree['0'])
        iterate(code+'1',tree['1'])

    while (len(terms) !=10) :
        min1 = terms[0]
        min2 = terms[1]
        i = 0
        new_term = ({'0':copy.deepcopy(min1[0]),'1':copy.deepcopy(min2[0])}, min1[1]+min2[1])
        for t in terms:
            if new_term[1] < t[1]:
                terms.insert(i,new_term)
                break
            i+=1
        terms.remove(min1)
        terms.remove(min2)
    # there is a little problem about using insert and remove at same time when the length is lower than 10
    # so I separately write the method when the length lower than 10
    while (len(terms) !=1) :
        min1 = terms[0]
        min2 = terms[1]
        del terms[0]
        del terms[0]
        new_term = ({'0':copy.deepcopy(min1[0]),'1':copy.deepcopy(min2[0])}, min1[1]+min2[1])
        terms.append(new_term)
        terms = sorted(terms, key=lambda x:x[1])
    iterate('',terms[0][0])
    return result, terms[0][0]

def insert_term(terms, insert):
    terms_ = terms
    for i in range(len(terms_)):
        if terms_[i][1] >= insert[1]:
            terms_.insert(i, insert)
            break
    return terms_

def convert_binary(huff_str):
    data = array.array('B')
    c_b = '00000000'
    length = len(huff_str)
    huff_str += c_b[:(8-len(huff_str)%8)]
    for i in range(0,len(huff_str), 8):
        bytes = int(huff_str[i:i+8],2)
        data.append(bytes)
    return data,length


def store(huff_str, model):
    data, length = convert_binary(huff_str)
    with open(bin_path,"wb") as f:
        data.tofile(f)
    with open(plk_path, "wb") as f:
        model['length'] = length
        pickle.dump(model,f)
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
start = time.clock()
parser = argparse.ArgumentParser()
parser.add_argument('-s', type=str, help='Symbol')
parser.add_argument('input', type=str, help="Input file")
args = parser.parse_args()

if "s" in args and "input" in args:
    symbol = args.s if args.s else 'word'
    file_path  = args.input if args.input else 'infile.txt'
    bin_path = file_path[:file_path.find('.')] + '.bin'
    plk_path = file_path[:file_path.find('.')] + '-symbol-model.pkl'
    text = ""
else:
        sys.exit()

with open(file_path) as f:
    text = f.read()
term_array = None
# read content
if symbol == "char":
    term_array = format_data(text)
if symbol == 'word':
    word_pattern = re.compile(r'([a-z]+)', re.I)
    symbol_pattern = re.compile(r'[^a-z]{1}',re.I)
    word_r = word_pattern.findall(text)     #   find all word
    symbol_r = symbol_pattern.findall(text)     # find all the symbol include the invisible character
    term_array = format_data(word_r+symbol_r)
# term_array is the frequency of each term in the text
term_array = sorted(term_array.items(), key=lambda c: c[1])
terms_huffman, huffman_model = build_huffman(term_array)

print("Cost of building model:  %.2fs" %  (time.clock()-start))
start = time.clock()

huff_str = ""
if symbol == "char":
    for c in text:
        huff_str+=terms_huffman[c]
# it is easy for character
if symbol == "word":
    term = ''
    word_pattern = re.compile(r'([a-z])', re.I)
    for c in text:      # char by char reading the text
        if word_pattern.match(c):
            term+=c
        else:
            if len(term)!=0:       # if the term has the punctuation or invisible character
                huff_str+=(terms_huffman[term]+terms_huffman[c])
                term = ''
            else:
                huff_str += terms_huffman[c]
print('Cost of encoding: %.2fs'%(time.clock()-start))
store( huff_str, huffman_model)
