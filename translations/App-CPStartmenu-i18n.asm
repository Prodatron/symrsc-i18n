;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@                                                                            @
;@                S y m b O S   -   C o n t r o l   P a n e l                 @
;@                              STARTMENU EDITOR                              @
;@                   (default application texts [english])                    @
;@                                                                            @
;@             (c) 2015-2015 by Prodatron / SymbiosiS (Jörn Mika)             @
;@                                                                            @
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

;### POINTER ##################################################################

prgokytxt   db 1:dw prgokytxt_eng
prgcnctxt   db 1:dw prgcnctxt_eng
prgapltxt   db 1:dw prgapltxt_eng

stmtxttit   db 1:dw stmtxttit_eng
stmtxtcls   db 1:dw stmtxtcls_eng

tabmentxt   db 1:dw tabmentxt_eng
tabbuttxt   db 1:dw tabbuttxt_eng

stmtxtasc   db 1:dw stmtxtasc_eng
stmtxtasm   db 1:dw stmtxtasm_eng
stmtxtedi   db 1:dw stmtxtedi_eng
stmtxtnms   db 1:dw stmtxtnms_eng
stmtxtnmd   db 1:dw stmtxtnmd_eng
stmtxtptd   db 1:dw stmtxtptd_eng
stmtxtbrw   db 1:dw stmtxtbrw_eng
stmtxtstd   db 1:dw stmtxtstd_eng
stmtxtrnd   db 1:dw stmtxtrnd_eng
stmtxtrfs   db 1:dw stmtxtrfs_eng
stmtxtfav   db 1:dw stmtxtfav_eng

stmtxtrun0  db 1:dw stmtxtrun0_eng
stmtxtrun1  db 1:dw stmtxtrun1_eng
stmtxtrun2  db 1:dw stmtxtrun2_eng
stmtxtrun3  db 1:dw stmtxtrun3_eng

errmemtxt1  db 1:dw errmemtxt1_eng
errmemtxt2  db 1:dw errmemtxt2_eng
errmemtxt3  db 1:dw errmemtxt3_eng

errnumtxt1  db 1:dw errnumtxt1_eng
errnumtxt2  db 1:dw errnumtxt2_eng
errnumtxt3  db 1:dw errnumtxt3_eng

errsubtxt1  db 1:dw errsubtxt1_eng
errsubtxt2  db 1:dw errsubtxt2_eng
errsubtxt3  db 1:dw errsubtxt3_eng

icnfrmtxt   db 1:dw icnfrmtxt_eng
butfrmtxt   db 1:dw butfrmtxt_eng
icncoltxt   db 1:dw icncoltxt_eng
butwditxt   db 1:dw butwditxt_eng
butwdttxt   db 1:dw butwdttxt_eng
butcpttxt   db 1:dw butcpttxt_eng
butprttxt   db 1:dw butprttxt_eng
icnlodtxt   db 1:dw icnlodtxt_eng
icnsavtxt   db 1:dw icnsavtxt_eng


;### TEXTS ####################################################################

prgokytxt_eng   db "Ok",0
prgcnctxt_eng   db "Cancel",0
prgapltxt_eng   db "Apply",0

stmtxttit_eng   db "Startmenu Editor",0
stmtxtcls_eng   db "Close",0

tabmentxt_eng   db "Menu",0
tabbuttxt_eng   db "Button",0

stmtxtasc_eng   db "Add shortcut",0
stmtxtasm_eng   db "Add submenu",0
stmtxtedi_eng   db "Edit entry",0
stmtxtnms_eng   db "[entry is read only]",0
stmtxtnmd_eng   db "Name",0
stmtxtptd_eng   db "Target",0
stmtxtbrw_eng   db "Browse",0
stmtxtstd_eng   db "Start in",0
stmtxtrnd_eng   db "Run",0
stmtxtrfs_eng   db "Refresh",0
stmtxtfav_eng   db "Favourites",0

stmtxtrun0_eng  db "Default",0
stmtxtrun1_eng  db "Normal window",0
stmtxtrun2_eng  db "Minimized",0
stmtxtrun3_eng  db "Maximized",0

errmemtxt1_eng  db "Memory full!",0
errmemtxt2_eng  db "There is no memory left for",0
errmemtxt3_eng  db "completing this operation.",0

errnumtxt1_eng  db "Too many entries! The maximum",0
errnumtxt2_eng  db "amount of entries (24) for this",0
errnumtxt3_eng  db "submenu has been reached.",0

errsubtxt1_eng  db "Too many nested submenus!",0
errsubtxt2_eng  db "The deepest level for a",0
errsubtxt3_eng  db "submenu is 5.",0

icnfrmtxt_eng   db "Icon",0
butfrmtxt_eng   db "Button",0
icncoltxt_eng   db "Colour",0
butwditxt_eng   db "Icon width",0
butwdttxt_eng   db "Total width",0
butcpttxt_eng   db "Caption",0
butprttxt_eng   db "Preview",0
icnlodtxt_eng   db "Import SGX",0
icnsavtxt_eng   db "Export SGX",0

;### RESERVE
ds 50
