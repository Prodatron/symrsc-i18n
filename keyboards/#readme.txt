S Y M B O S   I N T E R N A T I O N A L I Z A T I O N
Author: Prodatron / SymbiosiS
Date:   07.05.2026
===============================================================================

I N T E R N A T I O N A L   K E Y B O A R D   L A Y O U T S


International keyboard layouts can be added and modified by editing the KEY_KEXGEN.TXT file and subsequently running the KEY_KEXGEN.PY Python script.

The first two lines contain comments, which describe the content of the first lines of a definition block. They are followed by an empty line. Now there is a block of definitions for each country specific keyboard layout.


FIRST LINE OF A DEFINITION BLOCK

- name: it contains a 8 char short form and the full language name written in the specific language
- codepage:
    2 : Latin 1
    3 : Japanese
    4 : Greek
    5 : Cherokee
    6 : Cyrillic
    7 : Latin 2
- number_of_layouts: The number of switchable keyboard layouts for this country. A layout is defined by a keyboard map, optional definitions for dead keys, and optional trees.
- number_of_trees: Each dead key definition represents a tree; the same applies to more complex trees, such as those used in the Japanese "Romaji" input method.
- flag_if_deadkeys: 1 if dead key definitions are present; 0 if not.


KEYBOARD LAYOUTS

There is a separate line for each switchable keyboard layout.

- name: The description of the layout.
- map: The keyboard map used by the layout; numbering starts at 1.
- tree: The tree used by the layout. If the layout contains dead keys, this value represents the index of the dead key definition (starting at 1). If the layout contains complex trees (e.g., for Romaji), this value represents the index of the tree (starting at 1), to which the value 32 is additionally added (thus, the value 33 or higher appears here). If the layout contains neither dead keys nor trees, the value 0 is entered here.
- additional icon bitmap: If more than one layout is present, the bitmap for the layout icon follows at this position (2x8 bytes; CPC 4-color encoding).


KEYBOARD MAPS

Each keyboard mapping begins with a line consisting of 13 "=" characters; this is followed by a line indicating the number of the associated dead key tree (Redundancy for simplifying the converter).
This is followed by 4x2 lines defining the key assignments without the AltGr key pressed. The first of these lines corresponds to the first row of keys without the Shift key pressed; The second line corresponds to the first row with the Shift key pressed; the third line corresponds to the second row without the Shift key, and so on.

The keys are these from an ISO keyboard with 48 printable chars (without space):
1st row: 13 keys
2nd row: 12 keys
3rd row: 12 keys
4th row: 11 keys

ANSI keyboards (e.g., US or UK layouts) feature only 47 keys; the first key in the fourth row (to the left of the first letter) is missing.

A line consisting of 13 "-" characters separates the next section of the layout, which defines the key assignments when the AltGr key is pressed. A space character (" ") indicates that no keyboard function is assigned to the corresponding position. The second section of the layout is finally followed by a line consisting of 13 "-" characters.


DEFINITIONS FOR DEAD KEYS

If one or more dead key definitions are present, they begin at this point. Each dead key definition starts with a line containing all the dead key characters. This is followed - for each of these characters and in the same order - by a list of all possible character combinations. The first character on a line is the one that is produced; this is followed by a space, which is in turn followed by the two characters that must be pressed to obtain the first one.

Each dead character definition, as well as each complete country-specific definition, ends with a line consisting of 13 "#" characters.
