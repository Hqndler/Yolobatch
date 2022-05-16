# Yolobatch

[French README](https://github.com/Hqndler/Yolobatch/blob/main/README.fr.md)

Will create the .bat for you. Copy the command line MkvToolNix and paste it in the script, it will do the rest.

### How yo use it ?

The script is based on the naming, on the names of the files, so it is important not to name them well.
Two type of namming recognized: 
- Serie's name S01E01.mp4
- Serie's name 01.mkv / Name.of.the.series.01.hevc / Serie's name #01.avi / Name of the series - 01 - BdRip.webm / Serie's name [01].cequetuveux
It's important to have a name that have at least a letter or several words for it to works.
##### `01.mp4` please make a little bit of effort in the naming
#### If the number is in brackets it will not be taken into account: `Name of the series (01).mkv` => not good
Don't hesitate to name differently each element that will constitute the final mkv.

### Requirements

Python 3.4+
`pip install colorama`
