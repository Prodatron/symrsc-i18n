import glob
import sys


"""
===============================================================================
SYSTEM FONT GENERATOR FROM BMP
===============================================================================

Converts BMP files to system font file
supports BMP files with 4/8bpp, uncompressed;
graphic must be 2 colour indexed, colour 0 paper, colour 1 pen,
                128*128 pixel, 16x16 chars

usage:
python3 font_bmp2system.py [filemask]
"""


### ---------------------------------------------------------------------------
### get word from binary
### ---------------------------------------------------------------------------
def word_get(binary):
    return binary[0] + 256 * binary[1]


### ---------------------------------------------------------------------------
### load binary
### ---------------------------------------------------------------------------
def bin_load(file):
    fil_bin = open(file, "rb")
    binary = fil_bin.read()
    fil_bin.close()
    return binary


### ---------------------------------------------------------------------------
### save binary
### ---------------------------------------------------------------------------
def bin_save(file, binary):
    fil_bin = open(file, "wb")
    fil_bin.write(binary)
    fil_bin.close()


### ---------------------------------------------------------------------------
### save text
### ---------------------------------------------------------------------------
def txt_save(file, txt):
    fil_txt = open(file, "w")
    fil_txt.write(txt)
    fil_txt.close()


### ---------------------------------------------------------------------------
### returns 0-padded hex string
### ---------------------------------------------------------------------------
def hexpad(num, size):
    hexstr = hex(num).split("x")[1]
    return "0"*(size-len(hexstr)) + hexstr


### ---------------------------------------------------------------------------
### generates RAW from BMP
### ---------------------------------------------------------------------------
def bmp2raw(bin_bmp, xlen, ylen):
    bin_raw = bytearray()

    # check for valid BMP parameters
    xorg = word_get(bin_bmp[18:20])
    yorg = word_get(bin_bmp[22:24])
    if bin_bmp[25] > 128:
        yorg = 65536 - yorg
    if (xorg != xlen) or (yorg != ylen):
        print(f"wrong image size; must be {xlen} x {ylen}")
    elif (bin_bmp[28] != 8) and (bin_bmp[28] != 4):
        print("unsupported colourdepth; must be 4 or 8 bpp")
    elif bin_bmp[30] != 0:
        print("file must be uncompressed")
    else:

        if bin_bmp[28] == 4:
            xbyt = int(xlen/2)
        else:
            xbyt = xlen

        adr_beg = word_get(bin_bmp[10:12])
        for i in range(ylen):
            if bin_bmp[25] > 128:
                adr_lin = adr_beg + i * xbyt
            else:
                adr_lin = adr_beg + (ylen - 1 - i) * xbyt

            if bin_bmp[28] == 4:
                for i in range(xbyt):
                    bin_raw += bytearray([int(bin_bmp[adr_lin + i] / 16), bin_bmp[adr_lin + i] % 16])
            else:
                bin_raw += bin_bmp[adr_lin:adr_lin + xlen]

    return bin_raw


### ---------------------------------------------------------------------------
### generates FNT from RAW
### ---------------------------------------------------------------------------
def raw2fnt(bin_raw, xcount, ycount, xmax, yheight, cstart, prop, codepage):
    bin_fnt = bytearray([yheight+128+32, int(codepage)])
    cnt = 0
    for y in range(ycount):
        for x in range(xcount):
            bin_chr = bytearray()
            if prop:
                xlen = 1
                if cnt == 32:                   # space
                    xlen = 3
                elif cnt == 29:                 # space8 (e.g. tree control)
                    xlen = 8
            else:
                xlen = xmax
            for l in range(yheight):
                byt = 0
                for b in range(xmax):
                    adr = y*yheight*xmax*xcount + l*xcount*xmax + x*xmax + b
                    byt = byt * 2 + bin_raw[adr]
                    if bin_raw[adr]>0:
                        xlen = max(xlen, b+2)
                for b in range(8-xmax):
                    byt *= 2
                bin_chr += bytearray([byt])
            for l in range(8-yheight):
                bin_chr += bytearray([0])
            if (xlen == 1) and (cnt == 160):    # NBSP
                xlen = 3
            if cnt > 0:
                bin_fnt += bytearray([xlen]) + bin_chr
            cnt += 1
    
    return bin_fnt


### ---------------------------------------------------------------------------
### generates ASM from FNT
### ---------------------------------------------------------------------------
def fnt2asm(bin_fnt, cstart):
    txt_asm = f"db {bin_fnt[0]},{bin_fnt[1]}\n"
    for i in range(int((len(bin_fnt)-2)/9)):
        adr = i*9+2
        txt_asm += f"db {bin_fnt[adr+0]}"
        for j in range(8):
            txt_asm += f",#{hexpad(bin_fnt[adr+1+j],2)}"
        chrnum = i+cstart
        if chrnum<10:
            txt_asm += f"  ;00{chrnum}"
        elif chrnum<100:
            txt_asm += f"  ;0{chrnum}"
        else:
            txt_asm += f"  ;{chrnum}"
        if (chrnum>32) and (chrnum<128):
            txt_asm += " " + chr(chrnum)
        txt_asm += "\n"
    return txt_asm


### ---------------------------------------------------------------------------
### generates FNT from BMP or RAW
### ---------------------------------------------------------------------------
def gen_fnt(file):
    codepage = int(file[1:3])
    xcount = 16
    ycount = 16
    xmax = 8
    yheight = 8
    cstart = 1

    print(file, xcount, ycount, xmax, yheight, cstart)
    print(f"Codepage {codepage}")

    xlen = xcount * xmax
    ylen = ycount * yheight

    fil_fnt = file[:len(file) - 4] + ".fnt"
    fil_asm = file[:len(file) - 4] + ".asm"
    print(f"converting {file} to {fil_fnt}...")

    if file[len(file) - 4:] == '.bmp':
        bin_bmp = bin_load(file)
        bin_raw = bmp2raw(bin_bmp, xlen, ylen)
        if len(bin_raw) == 0:
            return
        bin_fnt = raw2fnt(bin_raw, xcount, ycount, xmax, yheight, cstart, True, codepage)
    else:
        print("unknown filetype")
        return

    bin_fnt[(29-1)*9+2] = 8
    bin_save(fil_fnt, bin_fnt)
    #txt_save(fil_asm, fnt2asm(bin_fnt, cstart))
    print("DONE!")


### batch
if len(sys.argv) != 2:
    print("python3 font_bmp2system.py [filemask]")
else:
    files = glob.glob(sys.argv[1])
    if len(files) == 0:
        print("File(s) not found")
    else:
        for file in files:
            gen_fnt(file)
