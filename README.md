# Yolobatch

[French README](https://github.com/Hqndler/Yolobatch/blob/main/README.fr.md)

Will create the .bat for you. Copy the command line MkvToolNix and paste it in the script, it will do the rest.

## Requirements

Python 3.6+
`pip install colorama pyperclip`

## How yo use it ?

Launch the script in the terminal and follow the step(s). Only the command line is needed, not the json version.<br><br>
The script is name based, it's important to name the file(s) well.<br>
Multiple regex are used to achieve that:<br>
1. [Relative](https://regex101.com/r/Eawjea/1) -> `Something 01 Videos Propreties.extension`<br>
The regex accept the folling characters between the number : `space`, "\[" for opening and "]" for closing, "\_" (underscore), "." (dot) and start with "#"<br>
The number will be at least a two digits number (01 to 09 included).<br>
The goal is to not have to rename the file to fit the regex.<br>

Some examples : `Something #01 someting.extension`, `Something - [1337][something not new].old`, `Somethin_01_something.avi` or `Something.01.something.mp4`<br>

2. [Season](https://regex101.com/r/Eawjea/3) -> `Someting S01E01 Videos Propreties.extension`<br>
The regex starts at the "S" and ends at the last digit of the number of the episode.<br>
The structure "SXXEXX" is the base line.<br>

Clic on the links to check the regex if you're not sure.<br>

## The title exception
The title name for the mkv can be change by the script if it follows the Relative regex for the first part, you don't need to have a closing character for the title.<br>
So the name can be `Episode 01`, without the closing space character.

## Add fonts with -f argument

You can launch the script with "-f" (`python yolobatch.py -f`) in argument to open a special menu.<br>
You need to have as many folder as raw used for this part to work. Each folder will have fonts that are used in associated ASS file.<br>
You can generate those folders by manualy extracting every single fonts used with aegisub or use my other script [here](https://github.com/Hqndler/AssFontCollector)<br>
Should look like [this](https://github.com/Hqndler/AssFontCollector/blob/main/Output%20proof%20for%20ALL_IN_ONE%20False.png).<br>
You just need to paste the folder where those sub folder are. This will help you to mux the exact fonts for each mkv and not have unused fonts in them.

### You can now leave a star to this repo ;)
