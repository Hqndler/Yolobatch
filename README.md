# Yolobatch

[French README](https://github.com/Hqndler/Yolobatch/blob/main/README.fr.md)

Will create a batch file for you. Copy the command line MkvToolNix and paste it in the script, it will do the rest.

## Requirements

Python 3.6+
`pip install colorama pyperclip`

## How yo use it ?

Do for the first file everything in MkvToolNix, then copy the command line via `Multiplexer -> Show command line` 

and launch the script `py yolobatch.py`. Done !

## Add fonts with -f argument

`python yolobatch.py -f "<path>"` where <path> is a <path> to the **base** folder of *sub* folders containing fonts to be add to the mkv<br>
You need to have as many folder as raw used for this part to work. Each folder will have fonts that are used in associated ASS file.<br>
You can generate those folders by manualy extracting every single fonts used with aegisub or use my other script [here](https://github.com/Hqndler/AssFontCollector)<br>
*Should look like what my other script create.*<br>
This will help you to mux the exact fonts for each mkv and not have unused fonts in them.

## Supported naming

This script use regex to located the number of the file to change, here a list of supported naming:
- `S01E01` / `s01e01` check the regex [here](https://regex101.com/r/QEEEZV/1)
- `<space>01<space>` / `[01]` / `_01_` / `.01.` / `#01 ` check the regex [here](https://regex101.com/r/4FQCIN/1)
- `01x01` (for season 01 episode 01, really chaotic imo) check the regex [here](https://regex101.com/r/yMGDZP/1)

Regex are checked in this order but last regex might cause you problem if you decide to put the resolution of the file in its name. You might want not put the resolution in the name and rename your file afterwards. It's a very unlucky case but if you have a doubt use the first regex as your default numbering scheme.

You can check any regex with the provited links by pasting the name of any file in the "insert your test string here" area.

Lazy naming is also supported. You can name your file `01.av1` without problem.

### Can also be used on Linux and macOS

### You can now leave a star to this repo ;)
