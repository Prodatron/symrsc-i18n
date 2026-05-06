import sys, subprocess
import glob
import os
import json
import csv
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

FILE_UNICODE_TRANSLATION = "../SymbOS-Multilingual-Characters.txt"
FILE_GLOBAL_CONFIG       = "translation.json"

"""
### ===========================================================================
### MULTILINGUAL MANAGEMENT
### ===========================================================================

- reads JSON info file, which specifies
  - english ASM sourcefile
  - multilingual CSV table
  - SymbOS LNG binary
- generates CSV from ASM files, if not already existing
- auto-syncs lines in CSV according to ASM changes
  - inserts new lines
  - removes lines if not existing anymore
- auto-completes missing phrases, if found in phrase database ("translation.lib")
- re-generates CSV table, backups old one
- logs auto-changes ("translation.log")
- generates LNG binary

Requires
- uncode to symbos codepade translation file at FILE_UNICODE_TRANSLATION


usage:
python3 translation.py [file].json
"""

# 3_char_ID : MS_ID, codepage, 2or3_char_ID,name_english
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


### ---------------------------------------------------------------------------
### expression library
### ---------------------------------------------------------------------------
class expression_lib:

    def __init__(self):
        with open(str(Path(__file__).resolve().parent) + "/translation.lib", "r", encoding="utf-8") as f:
            self.expr = json.load(f)
            self.strip_chars = " .-[]1234567890０１２３４５６７８９"

    def add(self, keystr, values):
        values = {k: v for k, v in values.items() if v != "#TRANSLATE#"}
        key = values.pop("ENG", "").strip(self.strip_chars)
        if key != "":
            if key in self.expr:
                for lang in values:
                    value = values[lang].strip(self.strip_chars)
                    if value != "":
                        if lang in self.expr[key]:
                            if (value != self.expr[key][lang]) and (key.count(" ") < 4):
                                changelog(f'{keystr} -> "{key}": for {lang}, is "{self.expr[key][lang]}", new expression "{value}"')
                        else:
                            self.expr[key][lang] = value
            else:
                self.expr[key] = {}
                for lang in values:
                    value = values[lang].strip(self.strip_chars)
                    if value != "":
                        self.expr[key][lang] = value

    def get(self, key, lang):
        keystrip = key.strip(self.strip_chars)
        if keystrip in self.expr:
            if lang in self.expr[keystrip]:
                #print(f' -> expression for "{key}" in "{lang}" is "{self.expr[keystrip][lang]}"')
                pos = key.find(keystrip)
                return key[:pos] + self.expr[keystrip][lang] + key[pos + len(keystrip):]
        return "#TRANSLATE#"

    def save(self):
        with open(str(Path(__file__).resolve().parent) + "/translation.lib", "w", encoding="utf-8") as f:
            json.dump(self.expr, f, indent=2, ensure_ascii=False)

exprlib = expression_lib()



### ---------------------------------------------------------------------------
### load text
### ---------------------------------------------------------------------------
def txt_load(file):
    fil_txt = open(file, "r")
    txt = fil_txt.read().splitlines()
    fil_txt.close()
    return txt


### ---------------------------------------------------------------------------
### load text
### ---------------------------------------------------------------------------
def txt_load_utf8(file):
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
### load binary
### ---------------------------------------------------------------------------
def bin_load(file):
    fil_bin = open(file, "rb")
    binary = fil_bin.read()
    fil_bin.close()
    return bytearray(binary)


### ---------------------------------------------------------------------------
### save binary
### ---------------------------------------------------------------------------
def bin_save(file, binary):
    fil_bin = open(file, "wb")
    fil_bin.write(binary)
    fil_bin.close()


### ---------------------------------------------------------------------------
### generate backup name
### ---------------------------------------------------------------------------
def backup_file(path):
    path = Path(path)

    if not path.exists():
        return

    i = 0
    while True:
        suffix = ".bak" if i == 0 else f".bak.{i}"
        backup = path.with_name(path.name + suffix)
        if not backup.exists():
            path.rename(backup)
            return
        i += 1


### ---------------------------------------------------------------------------
### execute shell command
### ---------------------------------------------------------------------------
def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    c = p.communicate()


### ---------------------------------------------------------------------------
### compress data
### ---------------------------------------------------------------------------
def compress(binary):
    bin_save("temp", binary[:len(binary) - 4])
    run_cmd(str(Path(__file__).resolve().parent) + "/-zx0 temp")
    bin_crn = bin_load("temp.zx0")
    run_cmd("del temp")
    run_cmd("del temp.zx0")
    bin_crn = binary[len(binary) - 4:] + bytearray(2) + bin_crn
    return word_bin(len(bin_crn)) + bin_crn


### ---------------------------------------------------------------------------
### return word as binary
### ---------------------------------------------------------------------------
def word_bin(word):
    return bytearray([word % 256, int(word/256)])


### ---------------------------------------------------------------------------
### set word in header
### ---------------------------------------------------------------------------
def word_set(binary, adr, word):
    binary[adr+0] = word % 256
    binary[adr+1] = int(word/256)


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
### generate translation file
### ---------------------------------------------------------------------------
def trans_out(filein, fileout):

    trans_codes = load_unicode()

    global langnum

    version = 0
    print("\nGenerating LNG file...\n")

    txt_inp = txt_load_utf8(filein)
    texts = []      # textlines per pack
    packmax = []    # max values per pack

    infos = next(csv.reader(StringIO(txt_inp.pop(0))))

    langids = infos[2:]
    languages = len(langids)

    packs = 0
    for txt_line in txt_inp:
        if txt_line[:3] == "###":
            packs += 1
            parts = next(csv.reader(StringIO(txt_line)))
            packmax.append([int(parts[1]),int(parts[2])])
            texts.append([])
        else:
            parts = next(csv.reader(StringIO(txt_line)))
            textline = parts[2:]
            if len(textline) != languages:
                print(f"\n**ERROR**\nwrong column(s) at label '{parts[0]}'\n")
                return
            for i in range(len(textline)):
                if textline[i] == "#TRANSLATE#":
                    textline[i] = parts[1]
            if parts[0][:1] != "_":
                for i in range(len(textline)):
                    textline[i] += "\x00"
            texts[packs-1].append(textline)

    bin_out = bytearray([version, languages, packs])
    for i in range(packs):
        bin_out += bytearray([0,0]) + word_bin(len(texts[i])) + bytearray([0,0])
    for i in range(packs):
        word_set(bin_out, 3+4+i*6, len(bin_out))
        for j in range(languages):
            bin_out += bytearray([langnum[langids[j].lower()][0],0,0])

    tot_org = 0
    tot_crn = 0

    unknown_values = set()

    for i in range(packs):
        if len(texts[i]) > packmax[i][0]:
            print(f"\n**ERROR**\nPack {i} wrong number of lines {len(texts[i])} instead of {packmax[i][0]}\n")
        packlen = 0
        for j in range(languages):
            bin_pointers = bytearray()
            bin_texts = bytearray()
            for k in range(len(texts[i])):
                bin_pointers += bytearray([1]) + word_bin(3*len(texts[i])+len(bin_texts))
                for l in range(len(texts[i][k][j])):
                    char = ord(texts[i][k][j][l])
                    if char < 256:
                        bin_texts += bytearray([char])
                    elif (char>=0xFF01) and (char<=0xFF5E):
                        bin_texts += bytearray([char-0xFF01+33])
                    else:
                        val = False
                        key = str(char) + "-" + str(langnum[langids[j].lower()][1]) # codepage specific characters
                        if key in trans_codes:
                            val = trans_codes[key]
                        key = str(char) + "-0"                                      # common characters
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
                            unknown_values.add(char)
                            print(texts[i][k][j])

            bin_total = bin_pointers + bin_texts
            if len(bin_total) > packmax[i][1]:
                print(f"\n**ERROR**\nPack {i}, Language {j} too many bytes, {len(bin_total)} instead of {packmax[i][1]}, reduce by {len(bin_total)-packmax[i][1]} or increase text space.\n")
            packlen = max(len(bin_total), packlen)
            word_set(bin_out, 3+packs*6 + i*3*languages + j*3+1, len(bin_out))
            len_org = len(bin_total)
            tot_org += len_org
            bin_total = compress(bin_total)
            len_crn = len(bin_total)
            tot_crn += len_crn
            bin_out += bin_total
            print(f"Pack {i}, Language {j} compressed from {len_org} to {len_crn} ({len_crn/len_org*100:.0f}%)")
        word_set(bin_out, 3+0+i*6, packlen)
        print(f"Pack {i}: max {packlen} bytes used, {packmax[i][1]-packlen} bytes left\n")
    print(f"Total compressed from {tot_org} to {tot_crn} ({tot_crn/tot_org*100:.0f}%)")

    if len(unknown_values)>0:
        print(f"Unknown chars: {unknown_values}")
       
    bin_save(fileout, bin_out)


### ---------------------------------------------------------------------------
### read english language pack from asm source code
### ---------------------------------------------------------------------------
def asm_read(filein):
    txt_inp = txt_load(filein)
    labels = {}
    section = 0
    reserve = 0

    for txt_line in txt_inp:
        if "###" in txt_line:
            section += 1
        else:
            if section == 3:
                reserve = int(txt_line.split(" ")[1])
            else:
                txt_strip = txt_line.strip()
                if txt_strip[:1] != ";":
                    txt_split = txt_strip.split()
                    if len(txt_split) > 2:
                        if txt_split[1] == "db":
                            label = txt_split[0]
    
                            if section == 1:
                                labels[label.replace("_poi","")] = "*not found*"
    
                            elif section == 2:
                                label = label[:len(label)-4]
                                txtpos = txt_strip.find("db ")
                                if txtpos > -1:
                                    labels[label] = txt_strip[txtpos+3:]

    pack_out = {}
    for key, value in labels.items():
        label = key
        if value[len(value)-2:] == ",0":
            value = value[:len(value)-2]
        else:
            label = "_" + label
        pack_out[label] = value[1:len(value)-1]

    return pack_out, reserve


### ---------------------------------------------------------------------------
### read full language pack csv table
### ---------------------------------------------------------------------------
def csv_read(file):

    if not Path(file).exists():
        return [],[]

    txt_inp = txt_load_utf8(file)

    infos = next(csv.reader(StringIO(txt_inp.pop(0))))
    languages = infos[1:]
    packs = 0
    packs_out = []

    for txt_line in txt_inp:
        if txt_line[:3] == "###":
            packs += 1
            parts = next(csv.reader(StringIO(txt_line)))
            packs_out.append({})
        else:
            parts = next(csv.reader(StringIO(txt_line)))
            if (len(parts) - 1) != len(languages):
                print(f"\n**ERROR**\nwrong column(s) at label '{parts[0]}'\n")
                return
            packs_out[packs - 1][parts[0]] = {}

            for i in range(len(languages)):
                if (i > 0) and (parts[1+i] == "#TRANSLATE#"):
                    expr = exprlib.get(parts[1], languages[i])
                else:
                    expr = parts[1+i]
                packs_out[packs - 1][parts[0]][languages[i]] = expr


            exprlib.add(parts[0], packs_out[packs - 1][parts[0]])

    return packs_out, languages


### ---------------------------------------------------------------------------
### write full language pack csv table
### ---------------------------------------------------------------------------
def csv_write(file, packs_csv, languages, reserves):
    with open(file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["labels"] + [l for l in languages])
        for i in range(len(packs_csv)):
            packs_bytes = []                                        # generate pack titles
            for j in languages:
                pack_bytes = 0
                for label in packs_csv[i]:
                    pack_bytes += 3                                 # add 3 byte per pointer (1,pointer)
                    add_null = 0 if label[:1] == "_" else 1         # labels with _ don't have 0-terminator in expression
                    if packs_csv[i][label][j] == "#TRANSLATE#":
                        add_len = len(packs_csv[i][label]["ENG"])
                    else:
                        add_len = len(packs_csv[i][label][j])
                    pack_bytes += add_len + add_null
                packs_bytes.append(pack_bytes)
            writer.writerow([f"### pack{i}", len(packs_csv[i]), packs_bytes[0] + reserves[i]])
            for label in packs_csv[i]:                              # generate pack content
                line = [label]
                for clm in packs_csv[i][label]:
                    line.append(packs_csv[i][label][clm])
                writer.writerow(line)


### ---------------------------------------------------------------------------
### log changes
### ---------------------------------------------------------------------------
def changelog(text):
    with open(str(Path(__file__).resolve().parent) + "/translation.log", "a", encoding="utf-8") as f:
        f.write(text + "\n")
        #print(text)


### ---------------------------------------------------------------------------
### ask user for language IDs
### ---------------------------------------------------------------------------
def language_ask(text):
    global langnum

    languages = []
    print("\n" + text + "\nPlease enter at least one language, press [Return] to complete.\n")
    while True:
        language = input("3-letter ID: ").upper()
        if language == "":
            if len(languages)>0:
                return languages
        else:
            if language.lower() in langnum:
                languages.append(language)
            else:
                print("*unknown or wrong language ID*")


### ---------------------------------------------------------------------------
### converts asm to csv base file and adds additional languages
### ---------------------------------------------------------------------------
def asm2csv(packs_asm, languages):
    packs_csv = []

    for i in range(len(packs_asm)):
        pack_csv = {}
        for label in packs_asm[i]:
            pack_csv[label] = {"ENG": packs_asm[i][label]}
            for language in languages:
                pack_csv[label][language] = exprlib.get(packs_asm[i][label], language)
        packs_csv.append(pack_csv)

    return packs_csv


### ---------------------------------------------------------------------------
### do full translation
### ---------------------------------------------------------------------------
def i18n_translate_full(file_config):
    with open(file_config, "r") as f:
        config = json.load(f)

    packs_asm = []
    reserves = []
    for file in config["asm"]:
        pack_asm, reserve = asm_read(config["asm"][file])
        packs_asm.append(pack_asm)
        reserves.append(reserve)

    packs_csv, languages = csv_read(config["csv"])
    if packs_csv == []:
        languages = language_ask("No existing multlingual file.\nWhat languages you want to add?\n")
        packs_csv = asm2csv(packs_asm, languages)
        languages = ["ENG"] + languages

    if len(packs_csv) != len(packs_asm):
        print("number of packs do not match")
        return

    packs_new = []
    for pack_id in range(len(packs_asm)):
        print(f"Preparing Pack {pack_id}...")
        keys_asm = set(packs_asm[pack_id].keys())
        keys_csv = set(packs_csv[pack_id].keys())

        asm_new = list(keys_asm - keys_csv)
        csv_new = list(keys_csv - keys_asm)

        for label in csv_new:
            changelog(f'[{label}] removed, was "{packs_csv[pack_id][label]["ENG"]}"')
            del packs_csv[pack_id][label]

        for label in asm_new:
            changelog(f'[{label}] added, new is "{packs_asm[pack_id][label]}"')
            packs_csv[pack_id][label] = {"ENG": packs_asm[pack_id][label]}
            for language in languages:
                if language != "ENG":
                    packs_csv[pack_id][label][language] = exprlib.get(packs_asm[pack_id][label], language)     #"#TRANSLATE#"
            packs_csv[pack_id][label]["ENG"] = packs_asm[pack_id][label]

        pack_new = {}
        for label in packs_asm[pack_id]:
            if packs_asm[pack_id][label] != packs_csv[pack_id][label]["ENG"]:
                changelog(f'[{label}] changed, was "{packs_csv[pack_id][label]["ENG"]}", now is "{packs_asm[pack_id][label]}"')
                packs_csv[pack_id][label]["ENG"] = packs_asm[pack_id][label]
            pack_new[label] = packs_csv[pack_id][label]
        packs_new.append(pack_new)

    backup_file(config["csv"])
    csv_write(config["csv"], packs_new, languages, reserves)
    trans_out(config["csv"], config["lng"])

    exprlib.save()


### ---------------------------------------------------------------------------
### count missing phrases for one app and language
### ---------------------------------------------------------------------------
def i18n_translate_miss_combo(language, config_file):
    with open(config_file, "r") as f:
        config = json.load(f)

    cfg_path = config["csv"]
    if os.path.dirname(config_file) != "":
        cfg_path = os.path.dirname(config_file) + "/" + cfg_path

    packs_csv, languages = csv_read(cfg_path)
    if language in languages:
        miss = []
        for pack in packs_csv:
            miss_pack = {}
            for label in pack:
                if pack[label][language] == "#TRANSLATE#":
                    miss_pack[label] = pack[label]["ENG"]
            miss.append(miss_pack)
    else:
        miss = -1

    return miss


### ---------------------------------------------------------------------------
### display missing phrases for one languages
### ---------------------------------------------------------------------------
def i18n_translate_miss_one(language):
    with open(FILE_GLOBAL_CONFIG, "r") as f:
        global_config = json.load(f)
    print(language)
    for config_file in global_config["app_configs"]:
        miss = i18n_translate_miss_combo(language, config_file)
        if miss == -1:
            print(f"\n{os.path.basename(config_file).replace('json','csv')} -> NOT TRANSLATED")
        else:
            lines = 0
            for pack in miss:
                lines += len(pack)
            if lines > 0:
                print(f"\n{os.path.basename(config_file).replace('json','csv')}")
                pack_cnt = 0
                for pack in miss:
                    for label in pack:
                        print(f"Pack {pack_cnt} -> {label}: {pack[label]}")
                    pack_cnt += 1


### ---------------------------------------------------------------------------
### count and display missing phrases for all languages
### ---------------------------------------------------------------------------
def i18n_translate_miss_all():
    with open(FILE_GLOBAL_CONFIG, "r") as f:
        global_config = json.load(f)
    for language in global_config["languages"]:
        print("\n" + language)
        compl = True
        for config_file in global_config["app_configs"]:
            miss = i18n_translate_miss_combo(language, config_file)
            if miss == -1:
                compl = False
                print(os.path.basename(config_file).replace("json","csv") + ":not translated")
            else:
                lines = 0
                for pack in miss:
                    lines += len(pack)
                if lines > 0:
                    compl = False
                    print(os.path.basename(config_file).replace("json","csv") + ":" + str(lines))
        if compl:
            print("*complete*")



### batch
if len(sys.argv) == 2:
    if sys.argv[1] == "stats":
        i18n_translate_miss_all()
    elif sys.argv[1][:5] == "miss:":
        i18n_translate_miss_one(sys.argv[1][5:].upper())
    else:
        files = glob.glob(sys.argv[1])
        for file in files:
            i18n_translate_full(file)
        input("DONE!")
else:
    print("\npython3 translation.py [CONFIG].json")
    print("    generates LNG file for one app and updates translation CSV table")
    print("\npython3 translation.py stats")
    print("    shows overview of missing translations for all apps")
    print("\npython3 translation.py miss:[LNG]")
    print("    shows missing translations for all language, [LNG]=three character identifier, e.g. miss:SPA")
