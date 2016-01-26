from RSN import RSN
from SPC import SPC
import sys

filename = sys.argv[1]
rsn = RSN(filename)

for f in rsn.files():
    if f.filename.endswith("spc"):
        print SPC(rsn.read_file(f))

