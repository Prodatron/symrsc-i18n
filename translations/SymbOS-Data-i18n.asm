;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@                                                                            @
;@                  S y m b O S   -   S y s t e m - D a t a                   @
;@                                 DATA-AREA                                  @
;@                                                                            @
;@                         (default texts [english])                          @
;@                                                                            @
;@            (c) 2000-2026 by Prodatron / SymbiosiS (Joern Mika)             @
;@                                                                            @
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

;### POINTER ##################################################################

;general

sysbutok    db 1:dw sysbutok_eng
sysbutcnc   db 1:dw sysbutcnc_eng
sysbutsrc   db 1:dw sysbutsrc_eng
sysbutyes   db 1:dw sysbutyes_eng
sysbutno    db 1:dw sysbutno_eng
systiterr   db 1:dw systiterr_eng
systitinf   db 1:dw systitinf_eng
systitwrn   db 1:dw systitwrn_eng
systitcnf   db 1:dw systitcnf_eng
sysbutopn   db 1:dw sysbutopn_eng
sysbutsav   db 1:dw sysbutsav_eng

;text editor

ticmentx1   db 1:dw ticmentx1_eng
ticmentx2   db 1:dw ticmentx2_eng
ticmentx3   db 1:dw ticmentx3_eng
ticmentx4   db 1:dw ticmentx4_eng
ticmentx5   db 1:dw ticmentx5_eng

;run

systitrun   db 1:dw systitrun_eng
systxtrun1t db 1:dw systxtrun1t_eng
systxtrun2t db 1:dw systxtrun2t_eng
systxtrun3t db 1:dw systxtrun3t_eng

;shutdown

systitoff   db 1:dw systitoff_eng
systxtoff1t db 1:dw systxtoff1t_eng
systxtoff2t db 1:dw systxtoff2t_eng

;error messages

sysmsgver2  db 1:dw sysmsgver2_eng
sysmsgver3  db 1:dw sysmsgver3_eng

sysmsgfnd1  db 1:dw sysmsgfnd1_eng
sysmsgfnd2  db 1:dw sysmsgfnd2_eng
sysmsgfnd3  db 1:dw sysmsgfnd3_eng

sysmsgexe1  db 1:dw sysmsgexe1_eng
sysmsgexe2  db 1:dw sysmsgexe2_eng
sysmsgexe3  db 1:dw sysmsgexe3_eng

sysmsgmem1  db 1:dw sysmsgmem1_eng
sysmsgmem2  db 1:dw sysmsgmem2_eng
sysmsgmem3  db 1:dw sysmsgmem3_eng

sysmsglod1  db 1:dw sysmsglod1_eng
sysmsgdir1  db 1:dw sysmsgdir1_eng

;file select box

filseltit1  db 1:dw filseltit1_eng
filseltit2  db 1:dw filseltit2_eng
filseltxt1  db 1:dw filseltxt1_eng
filseltxt2  db 1:dw filseltxt2_eng
filseltxt3  db 1:dw filseltxt3_eng
filseltxt4  db 1:dw filseltxt4_eng

selopntab3a   db 1:dw selopntab3a_eng
selopntab3b   db 1:dw selopntab3b_eng
selopntab3c   db 1:dw selopntab3c_eng
selopntab3d   db 1:dw selopntab3d_eng
selopntab3e   db 1:dw selopntab3e_eng

;window control menu

dskctltx1   db 1:dw dskctltx1_eng
dskctltx2   db 1:dw dskctltx2_eng
dskctltx3   db 1:dw dskctltx3_eng
dskctltx4   db 1:dw dskctltx4_eng
dskctltx5   db 1:dw dskctltx5_eng
dskctltx7   db 1:dw dskctltx7_eng

;### TEXTS ####################################################################

;general

sysbutok_eng    db "Ok",0
sysbutcnc_eng   db "Cancel",0
sysbutsrc_eng   db "Browse...",0
sysbutyes_eng   db "Yes",0
sysbutno_eng    db "No",0
systiterr_eng   db "Error!",0
systitinf_eng   db "Info",0
systitwrn_eng   db "Warning",0
systitcnf_eng   db "Confirmation",0
sysbutopn_eng   db "Open",0
sysbutsav_eng   db "Save",0

;text editor

ticmentx1_eng   db "Cut",0
ticmentx2_eng   db "Copy",0
ticmentx3_eng   db "Paste",0
ticmentx4_eng   db "Delete",0
ticmentx5_eng   db "Select All",0

;run

systitrun_eng   db "Run",0
systxtrun1t_eng db "Type the path of a program or document,",0
systxtrun2t_eng db "and SymbOS will open it for you.",0
systxtrun3t_eng db "Open:",0

;shutdown

systitoff_eng   db "Shut Down SymbOS",0
systxtoff1t_eng db "What do you want the computer",0
systxtoff2t_eng db "to do?",0

;error messages

sysmsgver2_eng  db "This application requires a newer",0
sysmsgver3_eng  db "SymbOS version. Please upgrade.",0

sysmsgfnd1_eng  db "File not found:",0
sysmsgfnd2_eng  db "The file or the path don't exist.",0
sysmsgfnd3_eng  db "Please check your input.",0

sysmsgexe1_eng  db "File is not executable:",0
sysmsgexe2_eng  db "The selected file is not executable",0
sysmsgexe3_eng  db "in the SymbOS environment.",0

sysmsgmem1_eng  db "Memory full:",0
sysmsgmem2_eng  db "There is not enough memory for",0
sysmsgmem3_eng  db "executing the application.",0

sysmsglod1_eng  db "Disc error while loading file",0
sysmsgdir1_eng  db "Error while reading directory",0

;file select box

filseltit1_eng  db "Select file",0
filseltit2_eng  db "Select folder",0
filseltxt1_eng  db "Look in:",0
filseltxt2_eng  db "File name:",0
filseltxt3_eng  db "File type:",0
filseltxt4_eng  db "Folder:",0

selopntab3a_eng db "Name",0
selopntab3b_eng db "Size",0
selopntab3c_eng db "Date modified",0
selopntab3d_eng db "Attr.",0
selopntab3e_eng db "-"

;window control menu

dskctltx1_eng db "Restore",0
dskctltx2_eng db "Move",0
dskctltx3_eng db "Resize",0
dskctltx4_eng db "Minimize",0
dskctltx5_eng db "Maximize",0
dskctltx7_eng db "Close",0

;### RESERVE
ds 0
