S Y M B O S   I N T E R N A T I O N A L I Z A T I O N
Author: Prodatron / SymbiosiS
Date:   06.05.2026
===============================================================================

T R A N S L A T I N G   C O M P O N E N T S   A N D   A P P L I C A T I O N S


If you are interested in becoming part of the SymbOS translation team, the
following information will be very helpful.


CSV TABLES

Simple CSV tables are used to manage the multilingual support of SymbOS
operating system components and applications. A copy of the CSV table for each
application that supports multilingualism is located in this directory.

Simply open one of the tables in a modern spreadsheet program and take a look.
You'll probably get a good enough idea of how everything works. However, you'll
find all the details below.

Here is a list of the tables, grouped by importance:

Priority 1 - Operating System

App-OSExtend-i18n.csv       - Operating System
App-CPanel-i18n.csv         - Control Panel

Priority 2 - Standard Applications

App-Commander-i18n.csv      - SymCommander
App-TaskMgr-i18n.csv        - Task Manager
App-Wordpad-i18n.csv        - WordPad

Priority 3 - Daemons and more

Dmn-Sound-i18n.csv          - Sound Daemon
Dmn-Network-i18n.csv        - Network Daemon
App-Help-i18n.csv           - Helpfile Browser
App-Calc-i18n.csv           - Pocket Calculator
App-SymSee-i18n.csv         - SymSee picture viewer

Priority 4 - Everything else

[...currently no entries...]


Everything is in Unicode characters and UTF-8 encoded, todays standard for any 
Windows/Linux/Mac apps/spreadsheets. When translating, you should work through
the tables one after the other in order of importance.


TABLE STRUCTURE

The structure is very simple. A table begins with the "labels" column, which
contains a unique identifier for the phrase, and the column for the English
("ENG") version of the phrase. This is followed by another column for each
language containing its respective translation. The languages are defined in the
first row using the ISO 639-3 codes (see
https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes). The order is irrelevant,
except that English "ENG" must always be listed first after the "labels" column.

Some rows contain only the entry "###PACK[x]". An application can consist of
multiple language packages, for example, because it consists of multiple
executable files or multiple data areas. The translation is divided using these
"PACK" rows, so they must not be modified. The same applies, of course, to the
first ("labels") and second ("ENG") columns.


ADDING A NEW LANGUAGE

Adding a new language is very easy. Simply insert a new column (e.g., to the
right of the English column "ENG"), enter the three-letter language code in the
first row, and start translating.

Cells that are not yet translated should be filled with the placeholder
#TRANSLATE#
so the system knows that the translation is still missing. It will then use the
English text until the placeholder is replaced with the translation.

Some texts may be split across several consecutive cells; this always applies to
multi-line text in message boxes and similar formats. Here, care should be taken
to distribute the expressions as evenly as possible across the two or three
cells.

English is a compact language, and the SymbOS GUI was originally optimized for
it, but now tolerates longer expressions. Nevertheless, it can be tricky for
other languages to estimate the length of an expression so that it still fits
within the screen area. If there are already other translations, these can be
used as a guide, and shortening is necessary if needed. If that's too annoying,
you can simply ignore it. We have to check the screenshots afterwards anyway and
can optimize the expressions if necessary.


MAINTAINING AN EXISTING TRANSLATION

The file "#inclomplete.txt" contains all currently missing phrases, broken down
by language, file, and label. This allows you to immediately see if translations
need to be added for your language.


LOCAL TESTING OF THE TRANSLATION

You can test your translation yourself on your SymbOS installation. To do this,
download all associated application files (all "*.bat", "*.json", "*.asm") as
well as the "translation.*" files and "-zx0.exe" (ZX0 compressor) to the same
directory on your PC. Python3 must be installed on your computer. After saving
the edited CSV file, run the corresponding BAT file.

A new LNG file should now be generated. In your SymbOS installation, replace the
old LNG file with the newly generated one, and you can then start and test the
application in SymbOS. SymbOS must, of course, be switched to the appropriate
language beforehand.


RETURNING EDITED TABLES

If you have translated a new language or edited a table, you can simply return
it to Prodatron via email:

jmika at prodatron dot net

[Currently, I still need to test how well pull requests with CSV files and
writing back to the local application repositories work, so I can't provide
details on this method yet. Initially, I would prefer returns via email or
Discord, etc.]
