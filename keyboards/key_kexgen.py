import glob
import sys

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
### returns 0-padded text as binary
### ---------------------------------------------------------------------------
def bin_text(text, length):
    return bytearray(text + chr(0) * (length - len(text)), "utf-8")


### ---------------------------------------------------------------------------
### generates layout data
### ---------------------------------------------------------------------------
def kex_layout(txt_line):
    infos = txt_line.split(";")
    bin_layout = bytearray([int(infos[1]),int(infos[2])]) + bin_text(infos[0], 22)
    if len(infos) == 4:
        bin_layout += bytearray.fromhex(infos[3][1:].replace(",#"," "))
    else:
        bin_layout += bytearray(16)
    return bin_layout


### ---------------------------------------------------------------------------
### translate
### ---------------------------------------------------------------------------
def chr_map(char, trans_codes, codepage):
    code = ord(char)
    val = False
    key = str(code) + "-" + str(codepage)
    if key in trans_codes:
        val = trans_codes[key]
    key = str(code) + "-0"
    if key in trans_codes:
        val = trans_codes[key]
    if val:
        code = int(val, 16)
    if code>255:
        print(f"Unknown Unicode char: {char} -> {code}")
        print(codepage)
    return code


### ---------------------------------------------------------------------------
### translate
### ---------------------------------------------------------------------------
def key_map(txt_map, trans_codes, dead_list, codepage):
    ascii = "`1234567890-=" + "~!@#$%^&*()_+" + "qwertyuiop[]" + "QWERTYUIOP{}" + "asdfghjkl;'\\" + "ASDFGHJKL:\"|" + chr(30) + "zxcvbnm,./" + chr(31) + "ZXCVBNM<>?"

    for i in range(len(dead_list)):
        txt_map = txt_map.replace(dead_list[i], chr(i + 24))

    chrmap = bytearray(100)
    chrmap[4] = 32

    for i in range(len(txt_map)):
        code = chr_map(txt_map[i], trans_codes, codepage)
        if code == 32:
            code = 0
        chrmap[ord(ascii[i])-28] = code

    return chrmap


### ---------------------------------------------------------------------------
### generates one-layout KEX files
### ---------------------------------------------------------------------------
def kex_write(out_name, codepage, layouts, maps, trees, bin_data):
    langnum = {
        "ara": [0x0001, -1, "ar","Arabic"],
        "bul": [0x0002, -1, "bg","Bulgarian"],
        "cat": [0x0003,  2, "ca","Catalan"],
        "zho": [0x0004, -1, "zh","Chinese"],
        "ces": [0x0005,  7, "cs","Czech"],
        "dan": [0x0006,  2, "da","Danish"],
        "deu": [0x0007,  2, "de","German"],
        "ell": [0x0008,  4, "el","Greek"],
        "eng": [0x0009,  2, "en","English"],
        "spa": [0x000A,  2, "es","Spanish"],
        "fin": [0x000B,  2, "fi","Finnish"],
        "fra": [0x000C,  2, "fr","French"],
        "heb": [0x000D, -1, "he","Hebrew"],
        "hun": [0x000E,  7, "hu","Hungarian"],
        "isl": [0x000F,  2, "is","Icelandic"],
        "ita": [0x0010,  2, "it","Italian"],
        "jpn": [0x0011,  3, "ja","Japanese"],
        "kor": [0x0012, -1, "ko","Korean"],
        "nld": [0x0013,  2, "nl","Dutch"],
        "nor": [0x0014,  2, "no","Norwegian"],
        "pol": [0x0015,  7, "pl","Polish"],
        "por": [0x0016,  2, "pt","Portuguese"],
        "roh": [0x0017, -1, "rm","Romansh"],
        "ron": [0x0018,  7, "ro","Romanian"],
        "rus": [0x0019,  6, "ru","Russian"],
        "hrv": [0x001A,  7, "hr","Croatian"],
        "slk": [0x001B,  7, "sk","Slovak"],
        "sqi": [0x001C,  7, "sq","Albanian"],
        "swe": [0x001D,  2, "sv","Swedish"],
        "tha": [0x001E, -1, "th","Thai"],
        "tur": [0x001F,  2, "tr","Turkish"],
        "urd": [0x0020, -1, "ur","Urdu"],
        "ind": [0x0021,  2, "id","Indonesian"],
        "ukr": [0x0022,  6, "uk","Ukrainian"],
        "bel": [0x0023,  6, "be","Belarusian"],
        "slv": [0x0024,  7, "sl","Slovenian"],
        "est": [0x0025, -1, "et","Estonian"],
        "lav": [0x0026, -1, "lv","Latvian"],
        "lit": [0x0027, -1, "lt","Lithuanian"],
        "tgk": [0x0028, -1, "tg","Tajik"],
        "fas": [0x0029, -1, "fa","Persian"],
        "vie": [0x002A, -1, "vi","Vietnamese"],
        "hye": [0x002B, -1, "hy","Armenian"],
        "azj": [0x002C, -1, "az","Azerbaijani (North)"],
        "eus": [0x002D,  2, "eu","Basque"],
        "hsb": [0x002E, -1, "hsb","Upper Sorbian"],
        "mkd": [0x002F, -1, "mk","Macedonian"],
        "sot": [0x0030, -1, "st","Southern Sotho"],
        "tso": [0x0031, -1, "ts","Tsonga"],
        "tsn": [0x0032, -1, "tn","Tswana"],
        "ven": [0x0033, -1, "ve","Venda"],
        "xho": [0x0034, -1, "xh","Xhosa"],
        "zul": [0x0035, -1, "zu","Zulu"],
        "afr": [0x0036,  2, "af","Afrikaans"],
        "kat": [0x0037, -1, "ka","Georgian"],
        "fao": [0x0038,  2, "fo","Faroese"],
        "hin": [0x0039, -1, "hi","Hindi"],
        "mlt": [0x003A, -1, "mt","Maltese"],
        "sme": [0x003B, -1, "se","Northern Sami"],
        "gle": [0x003C,  2, "ga","Irish"],
        "yid": [0x003D, -1, "yi","Yiddish"],
        "msa": [0x003E,  2, "ms","Malay"],
        "kaz": [0x003F, -1, "kk","Kazakh"],
        "kir": [0x0040, -1, "ky","Kyrgyz"],
        "swa": [0x0041,  2, "sw","Swahili"],
        "tuk": [0x0042, -1, "tk","Turkmen"],
        "uzb": [0x0043, -1, "uz","Uzbek"],
        "tat": [0x0044, -1, "tt","Tatar"],
        "ben": [0x0045, -1, "bn","Bengali"],
        "pan": [0x0046, -1, "pa","Punjabi"],
        "guj": [0x0047, -1, "gu","Gujarati"],
        "ori": [0x0048, -1, "or","Odia"],
        "tam": [0x0049, -1, "ta","Tamil"],
        "tel": [0x004A, -1, "te","Telugu"],
        "kan": [0x004B, -1, "kn","Kannada"],
        "mal": [0x004C, -1, "ml","Malayalam"],
        "asm": [0x004D, -1, "as","Assamese"],
        "mar": [0x004E, -1, "mr","Marathi"],
        "san": [0x004F, -1, "sa","Sanskrit"],
        "mon": [0x0050, -1, "mn","Mongolian"],
        "bod": [0x0051, -1, "bo","Tibetan"],
        "cym": [0x0052,  2, "cy","Welsh"],
        "khm": [0x0053, -1, "km","Khmer"],
        "lao": [0x0054, -1, "lo","Lao"],
        "mya": [0x0055, -1, "my","Burmese"],
        "glg": [0x0056,  2, "gl","Galician"],
        "kok": [0x0057, -1, "kok","Konkani"],
        "mni": [0x0058, -1, "mni","Manipuri"],
        "snd": [0x0059, -1, "sd","Sindhi"],
        "syc": [0x005A, -1, "syr","Syriac (Classical)"],
        "sin": [0x005B, -1, "si","Sinhala"],
        "chr": [0x005C,  5, "chr","Cherokee"],
        "iku": [0x005D, -1, "iu","Inuktitut"],
        "amh": [0x005E, -1, "am","Amharic"],
        "tzm": [0x005F, -1, "tzm","Central Atlas Tamazight"],
        "kas": [0x0060, -1, "ks","Kashmiri"],
        "nep": [0x0061, -1, "ne","Nepali"],
        "fry": [0x0062, -1, "fy","Western Frisian"],
        "pus": [0x0063, -1, "ps","Pashto"],
        "fil": [0x0064,  2, "fil","Filipino"],
        "div": [0x0065, -1, "dv","Dhivehi"],
        "bin": [0x0066, -1, "bin","Bini / Edo"],
        "ful": [0x0067, -1, "ff","Fulah"],
        "hau": [0x0068, -1, "ha","Hausa"],
        "ibb": [0x0069, -1, "ibb","Ibibio"],
        "yor": [0x006A, -1, "yo","Yoruba"],
        "quz": [0x006B, -1, "quz","Quechua (Cusco)"],
        "nso": [0x006C, -1, "nso","Northern Sotho"],
        "bak": [0x006D, -1, "ba","Bashkir"],
        "ltz": [0x006E,  2, "lb","Luxembourgish"],
        "kal": [0x006F, -1, "kl","Greenlandic"],
        "ibo": [0x0070, -1, "ig","Igbo"],
        "kau": [0x0071, -1, "kr","Kanuri"],
        "orm": [0x0072, -1, "om","Oromo"],
        "tir": [0x0073, -1, "ti","Tigrinya"],
        "grn": [0x0074, -1, "gn","Guarani"],
        "haw": [0x0075, -1, "haw","Hawaiian"],
        "lat": [0x0076, -1, "la","Latin"],
        "som": [0x0077, -1, "so","Somali"],
        "iii": [0x0078, -1, "ii","Sichuan Yi"],
        "pap": [0x0079, -1, "pap","Papiamento"],
        "arn": [0x007A, -1, "arn","Mapudungun"],
        "moh": [0x007C, -1, "moh","Mohawk"],
        "bre": [0x007E, -1, "br","Breton"],
        "uig": [0x0080, -1, "ug","Uyghur"],
        "mri": [0x0081, -1, "mi","Maori"],
        "oci": [0x0082,  2, "oc","Occitan"],
        "cos": [0x0083, -1, "co","Corsican"],
        "gsw": [0x0084,  2, "gsw","Swiss German / Alemannic"],
        "sah": [0x0085, -1, "sah","Yakut"],
        "qut": [0x0086, -1, "qut","K'iche' (Guatemala)"],
        "kin": [0x0087, -1, "rw","Kinyarwanda"],
        "wol": [0x0088, -1, "wo","Wolof"],
        "prs": [0x008C, -1, "prs","Dari (Afghan Persian)"],
        "gla": [0x0091,  2, "gd","Scottish Gaelic"],
        "kur": [0x0092, -1, "ku","Kurdish"],
        "quc": [0x0093, -1, "quc","K'iche'"],
    }

    langid = langnum[out_name[:3].lower()][0]

    if layouts < 2:
        flags = 1
    else:
        flags = 3

    bin_out = bytearray([ord("K"),ord("X"),0, flags, len(bin_data) % 256, int(len(bin_data)/256), layouts, maps, trees, codepage, langid]) + bytearray(13) + bin_text(out_name, 24) + bin_data

    filnam = out_name[:7].rstrip(" ")
    bin_save("K_" + filnam + ".KEX", bin_out)


### ---------------------------------------------------------------------------
### sets pointer offset in tree structure
### ---------------------------------------------------------------------------
def offset(tree_bin, poi_adr, dst_adr):
    ofs_dif = dst_adr - poi_adr - 2
    tree_bin[poi_adr + 0] = ofs_dif % 256
    tree_bin[poi_adr + 1] = int(ofs_dif / 256)

    return tree_bin


### ---------------------------------------------------------------------------
### generates all KEX files
### ---------------------------------------------------------------------------
def kex_gen(file):
    trans_codes = load_unicode()

    txt_kex = txt_load(file)
    txt_pos = 3

    while txt_pos < len(txt_kex):
        infos = txt_kex[txt_pos].split(";")
        kex_name     = infos[0]
        print(kex_name)
        kex_codepage = int(infos[1])
        kex_layouts  = int(infos[2])
        kex_maps     = int(infos[3])
        kex_trees    = int(infos[4])
        kex_deadflag = int(infos[5])

        bin_layout = bytearray()
        for i in range(kex_layouts):
            bin_layout += kex_layout(txt_kex[txt_pos + 1 + i])

        dead_pos = txt_pos + 1 + kex_layouts + kex_maps * 19 + 1
        bin_tree = bytearray()
        dead_list = [""]
        if kex_deadflag == 1:
            dead_trees = []
            for i in range(kex_trees):
                dead_keys = txt_kex[dead_pos]
                dead_list.append(dead_keys)
                dead_tree = []
                dead_pos += 1
                dead_count = 0
                while txt_kex[dead_pos] != "#############":
                    dead_tree.append(txt_kex[dead_pos])
                    dead_pos += 1
                    dead_count += 1
                dead_pos += 1
                dead_bin = bytearray(1 + len(dead_keys) * (3 + 1) + dead_count * (3 + 3))
                dead_bin[0] = len(dead_keys)
                adr_root = 1
                adr_mid = 1+3*len(dead_keys)
                adr_end = 1 + len(dead_keys) * (3 + 1) + dead_count * 3
                key_index = -1
                key_last = ""
                line_cnt = 0
                for line in dead_tree:
                    if line[2] != key_last:
                        key_index += 1
                        dead_bin[adr_root + 0] = 24 + key_index
                        dead_bin = offset(dead_bin, adr_root + 1, adr_mid)
                        adr_root += 3
                        key_last = line[2]
                        adr_cnt = adr_mid
                        dead_bin[adr_cnt] = 0
                        adr_mid += 1
                    dead_bin[adr_cnt] += 1
                    dead_bin[adr_end + line_cnt * 3 + 0] = 0
                    dead_bin[adr_end + line_cnt * 3 + 1] = chr_map(line[0], trans_codes, kex_codepage)
                    dead_bin[adr_end + line_cnt * 3 + 2] = 0
                    key_second = line[3].replace("_", " ")
                    if dead_keys.find(key_second) > -1:
                        key_second = chr(dead_keys.find(key_second) + 24)
                    dead_bin[adr_mid] = chr_map(key_second, trans_codes, kex_codepage)
                    dead_bin = offset(dead_bin, adr_mid+1, adr_end + line_cnt*3)
                    adr_mid += 3
                    line_cnt += 1
                dead_trees.append(dead_bin)
            dead_poi = bytearray()
            dead_all = bytearray()
            for i in range(kex_trees):
                ofs_dif = kex_trees * 2 + len(dead_all) - len(dead_poi) - 2
                dead_poi += bytearray([ofs_dif % 256, int(ofs_dif / 256)])
                dead_all += dead_trees[i]
            bin_tree = dead_poi + dead_all

        bin_map = bytearray()
        for i in range(kex_maps):
            map_pos = txt_pos + 2 + kex_layouts + 1 + i * 19
            map_dead = int(txt_kex[map_pos - 1])
            bin_map += key_map("".join(txt_kex[map_pos  :map_pos+8]),  trans_codes, dead_list[map_dead], kex_codepage)
            bin_map += key_map("".join(txt_kex[map_pos+9:map_pos+17]), trans_codes, dead_list[map_dead], kex_codepage)

        kex_write(kex_name, kex_codepage, kex_layouts, kex_maps, kex_trees, bin_layout + bin_map + bin_tree)

        txt_pos = dead_pos


# batch
kex_gen("key_kexgen.txt")
