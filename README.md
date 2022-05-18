# Yolobatch

[French README](https://github.com/Hqndler/Yolobatch/blob/main/README.fr.md)

Will create the .bat for you. Copy the command line MkvToolNix and paste it in the script, it will do the rest.

### Requirements

Python 3.6+
`pip install colorama`

### How yo use it ?

The script is based on the naming, on the names of the files, so it is important not to name them well.<br>
Two type of namming recognized: 
- Serie's name `S01E01`.mp4
- Serie's name ` 01.`mkv / Name.of.the.series`.01.`__hevc / Serie's name `#01.`avi / Name of the series -` 01 `- BdRip.webm / Serie's name `[01]`[TV 460p 69fps].whatyouwant<br>

It's important to have a name that have at least a letter or several words for it to works.<br>
Minimal name will be : `#01.mkv`
##### `01.mp4` please make a little bit of effort in the naming
#### If the number is in brackets it will not be taken into account: `Name of the series (01).mkv` => not good
It will also be necessary that all the files used have the same name and the same path, at least the same path for each sources, except for the number that changes, a warning will be displayed if it's not the case.<br>
Don't hesitate to name differently each element that will constitute the final mkv.
