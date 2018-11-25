
import array, argparse, re,time, pickle

start = time.clock()

class huffman_tree:
    def __init__(self, root):
        self.root = root
        self.code_table = {}
        self.dict_model = {}
        self.length = 0

    def iterate(self, root, code):
        if isinstance(root,str):
            self.code_table[root] = code
            return
        if root.has_children():
            self.iterate(root.l, code+'0')
            self.iterate(root.r, code+'1')

    def get_huff_table(self):
        self.iterate(self.root, '')
        return self.code_table

class huffman_node:
    def __init__(self,l=None, r=None):
        self.l = l
        self.r = r

    def has_children(self):
        if self.r is None and self.l is None:
            return False
        else:
            return True

def build_huffman(tuple_terms):
    while (len(tuple_terms) != 1):
        min1 = tuple_terms[0]
        min2 = tuple_terms[1]
        node = huffman_node(min1[0], min2[0])
        del tuple_terms[0]
        del tuple_terms[0]
        tuple_terms.insert(0, (node, min1[1] + min2[1]))

        tuple_terms = sorted(tuple_terms, key=lambda x: x[1])
    huffman_model = huffman_tree(tuple_terms[0][0])
    return huffman_model.get_huff_table(), huffman_model
#
# def build_huffman(terms):
#     result = {}
#     def iterate(code, tree):
#         if isinstance(tree,str):
#             result[tree] = code
#             return
#         iterate(code+'0',tree['0'])
#         iterate(code+'1',tree['1'])
#     while (len(terms) != 1):
#         while (len(terms) != 1) :
#             min1 = terms[0]
#             min2 = terms[1]
#             terms.insert(2,({'0':min1[0],'1':min2[0]}, min1[1]+min2[1]))
#             del terms[0]
#             del terms[0]
#             terms = sorted(terms, key=lambda x:x[1])
#     iterate('',terms[0][0])
#     return result, terms[0][0]
#
#
def convert_binary(huff_str):
    data = array.array('B')
    c_b = '00000000'
    length = len(huff_str)
    huff_str += c_b[:(8-len(huff_str)%8)]
    for i in range(0,len(huff_str), 8):
        bytes = int(huff_str[i:i+8],2)
        data.append(bytes)
    # print(int(huff_str[:8],2))   238
    # print(huff_str[-8:])
    return data,length
#
#
def store(file_path,huff_str, model):
    data, length = convert_binary(huff_str)
    with open(file_path+".bin","wb") as f:
        data.tofile(f)
    with open(file_path+'.plk', "wb") as f:
        model.length = length

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
#
#
# # ________main__________
# # parser = argparse.ArgumentParser()
# # parser.add_argument('-s', type=str, help='Symbol')
# # parser.add_argument('input', type=str, help="Input file")
# # args = parser.parse_args()
#
# # if "s" in args and "input" in args:
# #     symbol = args.s if args.s else 'word'
# #     file_path  = args.input if args.input else 'infile.txt'
# #     text = ""
# #     else:
# #         sys.exit()
#
symbol = 'word'
file_path  =  'infile.txt'
text = ""

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
terms_huffman, huffman_model =build_huffman(term_array)

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
# print(len(huff_str)) #5522874

store(file_path, huff_str, huffman_model)
print('%.2f'%(time.clock()-start))