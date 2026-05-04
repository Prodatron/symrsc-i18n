;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
;@                                                                            @
;@                          H e l p - B r o w s e r                           @
;@                   (default application texts [english])                    @
;@                                                                            @
;@             (c) 2015-2025 by Prodatron / SymbiosiS (Jörn Mika)             @
;@                                                                            @
;@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

;### POINTER ##################################################################

prgtxtinf1  db 1:dw prgtxtinf1_eng

hlptabtxt1  db 1:dw hlptabtxt1_eng
hlptabtxt2  db 1:dw hlptabtxt2_eng
hlpdsptxt1  db 1:dw hlpdsptxt1_eng
hlpdsptxt2  db 1:dw hlpdsptxt2_eng
hlpbuttxt1  db 1:dw hlpbuttxt1_eng
hlpbuttxt2  db 1:dw hlpbuttxt2_eng

txtprt1     db 1:dw txtprt1_eng

errlodtxt1  db 1:dw errlodtxt1_eng
errlodtxt2  db 1:dw errlodtxt2_eng
errlodtxt3  db 1:dw errlodtxt3_eng

errfndtxt1  db 1:dw errfndtxt1_eng
errfndtxt2  db 1:dw errfndtxt2_eng
errfndtxt3  db 1:dw errfndtxt3_eng

prgtxterrg  db 1:dw prgtxterrg_eng

;### TEXTE ####################################################################

prgtxtinf1_eng  db "Help Browser for SymbOS",0

hlptabtxt1_eng  db "Contents",0
hlptabtxt2_eng  db "Search",0
hlpdsptxt1_eng  db "Keyword to find:",0
hlpdsptxt2_eng  db "Select Topic:",0
hlpbuttxt1_eng  db "List Topics",0
hlpbuttxt2_eng  db "Show/Next",0

txtprt1_eng     db "Printing...",0

errlodtxt1_eng  db "Error while loading help file",0
errlodtxt2_eng  db "A disc error or a file format error",0
errlodtxt3_eng  db "occured.",0

errfndtxt1_eng  db "No topics found.",0
errfndtxt2_eng  db "This document doesn't contain",0
errfndtxt3_eng  db "the keyword you entered.",0

prgtxterrg_eng  db "Printer Daemon not found.",0

;### RESERVE
ds 20
