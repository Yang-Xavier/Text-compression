import array, argparse,time, pickle,sys


class Huffman_model:
    def __init__(self, model):
        self.model = model
        self.iterate_model = model

    def iterate_(self, index):
        node = self.iterate_model[index]
        if isinstance(node, str):
            return node
        else:
            self.iterate_model = node

    def reset(self):
        self.iterate_model = self.model

#---------------main----------------------------

parser = argparse.ArgumentParser()
parser.add_argument('bin', type=str, help="the compression file XXXX.bin")
args = parser.parse_args()

if 'bin' in args:
    bin_file = args.bin
    plk_file = bin_file[:bin_file.find('.bin')] + '.plk'
else:
    sys.exit()
# bin_file = 'infile.txt.bin'
plk_file = bin_file[:bin_file.find('.bin')] + '-symbol-model.pkl'
out_file = bin_file[:bin_file.find('.bin')] + '-decompressed.txt'
length = 0
model = {}
with open(plk_file, 'rb') as f:
    model = pickle.load(f)
length = model['length']
huffman = Huffman_model(model)

bytes = bytes();
data = array.array('B')
with open(bin_file, 'rb') as f:
    bytes = f.read()

length_r = 0
c_b = '00000000'
recover_file = ''
for ab in bytes:
    bstr = bin(ab)[2:]
    bstr = c_b[0:(8-len(bstr))] + bstr
    for b in bstr:
        r = huffman.iterate_(b)
        length_r+=1
        if isinstance(r,str):
            recover_file += r
            huffman.reset()
        if length_r >=length:
            break
with open(out_file, 'w') as f:
    f.write(recover_file)