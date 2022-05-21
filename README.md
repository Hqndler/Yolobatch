# Yolobatch

[French README](https://github.com/Hqndler/Yolobatch/blob/main/README.fr.md)

Will create the .bat for you. Copy the command line MkvToolNix and paste it in the script, it will do the rest.

### Requirements

Python 3.6+
`pip install colorama pyperclip`

### How yo use it ?

The script is based on the naming, on the names of the files, so it is important not to name them well.<br>
It will also be necessary that all the files used have the same name and the same path (at least the same path for each sources), except for the number that changes, a warning will be displayed if it's not the case.<br>
Two type of namming recognized: 
- Series name `S01E01`.mp4
- Series name` 01.`mkv / Name.of.the.series`.01.`hevc / Series name `#01.`avi / Name of the series -` 01 `- BdRip.webm / Series name `[01]`[TV 460p 69fps].whatyouwant<br>

It's important to have a name that have at least a letter or several words for it to works.<br>
Minimal name can be `#01.mkv` for exemple.
#### If the number is in brackets it will not be taken into account: `Name of the series (01).mkv` => not recognized
Don't hesitate to name differently each element that will constitute the final mkv.
