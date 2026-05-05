import sys, subprocess
import glob
import os

from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import csv
from io import StringIO


FILE_UNICODE_TRANSLATION = "../SymbOS-Multilingual-Characters.txt"

### ---------------------------------------------------------------------------
### load text
### ---------------------------------------------------------------------------
def txt_load(file):
    fil_txt = open(file, "r", encoding="utf-8")
    txt = fil_txt.read().splitlines()
    fil_txt.close()
    return txt


### ---------------------------------------------------------------------------
### save text
### ---------------------------------------------------------------------------
def txt_save(file, text):
    fil_txt = open(file, "w", encoding="utf-8")
    txt_out = ""
    for txt_lin in text:
        txt_out += txt_lin + "\n"
    fil_txt.write(txt_out)
    fil_txt.close()


### ---------------------------------------------------------------------------
### save binary
### ---------------------------------------------------------------------------
def bin_save(file, binary):
    fil_bin = open(file, "wb")
    fil_bin.write(binary)
    fil_bin.close()


### ---------------------------------------------------------------------------
### load unicode translation table
### ---------------------------------------------------------------------------
def load_unicode():
    file = FILE_UNICODE_TRANSLATION
    unicodes = txt_load(file)
    unicode = {}
    for line in unicodes:
        if line == "":
            continue
        if line[0] == "#":
            continue
        key   = str(int(line[8:14].strip(), 16)) + "-" + str(int(line[16:18]))
        value = line[0:8].strip()
        unicode[key] = value
    return unicode


### ---------------------------------------------------------------------------
### convert unicode to symbos codepage
### ---------------------------------------------------------------------------
def uni2sym(text, codepage):
    trans_codes = load_unicode()

    err = False
    bin_texts = bytearray()
    for chrstr in text:
        code = ord(chrstr)
        if code < 256:
            bin_texts += bytearray([code])
        elif (code>=0xFF01) and (code<=0xFF5E):
            bin_texts += bytearray([code-0xFF01+33])
        else:
            val = False
            key = str(code) + "-" + str(codepage)
            if key in trans_codes:
                val = trans_codes[key]
            key = str(code) + "-0"
            if key in trans_codes:
                val = trans_codes[key]
            if val:
                val = val.split("-")
                bin_texts += bytearray([int(val[0], 16)])
                if len(val) == 2:
                    if val[1] == "d":
                        bin_texts += bytearray([0xde])
                    elif val[1] == "h":
                        bin_texts += bytearray([0xdf])
            else:
                err = True
    txt_out = ",".join(f"#{bchr:02x}" for bchr in bin_texts)
    
    return txt_out, err


### ---------------------------------------------------------------------------
### converts tree to asm
### ---------------------------------------------------------------------------
def tree2asm(sub_tree, address, father, subname):
    if isinstance(sub_tree, str):
        return f'_node{subname}{address}\n  db 0,{sub_tree},0     ;{father}\n'
    else:
        txt_asm = f'_node{subname}{address}\n  db {len(sub_tree)}     ;{father}\n'
        for i in range(len(sub_tree)):
            txt_asm += f'  db "{list(sub_tree.keys())[i]}":dw _node{subname}{address}_{i}-$-2\n'
        for i in range(len(sub_tree)):
            txt_asm += tree2asm(sub_tree[list(sub_tree.keys())[i]], f'{address}_{i}', father + list(sub_tree.keys())[i], subname)

    return txt_asm


### ---------------------------------------------------------------------------
### generate key tree
### ---------------------------------------------------------------------------
def tree_gen(filename, subname, codepage):
    lines = txt_load(filename)[1:]

    key_tree = {}

    for line in lines:
        sep = line.find(" ")
        out, err = uni2sym(line[:sep], codepage)
        if err:
            print(f"unknown code in:\n{line}")
        inps = line[sep+1:].rstrip().split(" ")
        for inp in inps:
            sub_tree = key_tree
            for i in range(len(inp)-1):
                char = inp[i]
                if char not in sub_tree:
                    sub_tree[char] = {}
                sub_tree = sub_tree[char]
            sub_tree[inp[len(inp)-1]] = out

    txt_asm = tree2asm(key_tree, "", "", subname)

    txt_save(filename.replace(".txt","") + ".asm",[txt_asm])


### batch
if len(sys.argv) == 4:
    tree_gen(sys.argv[1], sys.argv[2], int(sys.argv[3]))
else:
    print("key_tree.py filename subname codepage")
