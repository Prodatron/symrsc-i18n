org #0000
nolist

write"k_jpnful.kex"

incbin"k_jpn.kex"

list
dw tree1-$-2
nolist

tree1
read"jpn_tree_romaji.asm"

list
totlen equ $-48     ;write this to header offset #04 !
