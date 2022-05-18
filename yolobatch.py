import os, re, glob, sys
from colorama import Fore, Style, init

init(convert = True)
s = 1
CHECK, TITLE, CHAPTER = False, False, False
FONT_MODE = 1
ALL, L_DONE = list(), list()

def collect_font():
    print_message()
    giga = []
    path = str(input())
    folder = os.listdir(path)
    for sub in folder:
        sub = os.path.join(path,sub)
        try :
            s = os.listdir(sub)
            if s:
                true_font = []
                for font in s:
                    if ".otf" in font.lower():
                        font = os.path.join(path,sub,font)
                        true_font.append(font)
                    elif ".ttf" in font.lower():
                        font = os.path.join(path,sub,font)
                        true_font.append(font)
                    elif ".ttc" in font.lower():
                        font = os.path.join(path,sub,font)
                        true_font.append(font)
                if true_font:
                    giga.append(true_font)
        except:
            pass
    return giga

def write_fonts(list):
    list_line = []
    standard_ttf = ' --attachment-name {} --attachment-mime-type application/x-truetype-font --attach-file ^"{}^"'
    standard_otf = ' --attachment-name {} --attachment-mime-type application/vnd.ms-opentype --attach-file ^"{}^"'
    standard_ttc = ' --attachment-name {} --attachment-mime-type font/collection --attach-file ^"{}^"'
    for fonts in list:
        line = ""
        for font in fonts:
            if ".otf" in font.lower():
                otf = standard_otf.replace('{}', os.path.basename(font) ,1).replace('{}', font, 1)
                line = line + otf
            if ".ttf" in font.lower():
                ttf = standard_ttf.replace('{}', os.path.basename(font) ,1).replace('{}', font, 1)
                line = line + ttf
            if ".ttc" in font.lower():
                ttc = standard_ttc.replace('{}', os.path.basename(font) ,1).replace('{}', font, 1)
                line = line + ttc
        list_line.append(line)
    return list_line

def print_message():
    print(Fore.GREEN + "Les fonts doivent être rangée dans un dossier pour chaque épisodes :\ns'il y a 25 épisodes alors il faudra 25 dossiers avec des fonts dans chacun d'entre eux.")
    print("De préférence numéroté comme suit : \\01\\, \\02\\, [...], \\25\\.")
    print("Les formats pris en compte sont : .otf et .tff")
    print("Attention, vous ne devez pas ajouter vous même les fonts dans le mkv, les attachements ne doivent pas contenir de font contenu dans ces dossiers sous peine de doublons.")
    print("Coller le chemin complet du dossier qui contient tout les sous dossiers pour les fonts :")
    print(Style.RESET_ALL)

def find_output(command):
    output = command[command.find('--output') + 11 : command.find(".mkv^") + 4]
    ALL.append(output)
    return output

def find_all_input(command):
    a = re.findall('\"\^\(.*?\)\^\"', command)
    for i in a:
        j = i.replace('"^(^" ^"', '').replace('^" ^"^)^"', '')
        ALL.append(j)
    track = command.find("--track-order")
    if "--title" in command:
        index = command.find("--title")
        title = command[index + 10 : command.find('^" ', index, track)]
        if len(title) > 0:
            global TITLE
            TITLE = True
            ALL.append(title)
    if "--chapter" in command:
        index = command.find("--chapters")
        chapter = command[index + 13 : command.find('^" ', index, track)]
        if len(chapter) > 0:
            global CHAPTER
            CHAPTER = True
            ALL.append(chapter)
    return ALL

def number_raw_input(liste):
    raw = liste[1].replace('"^', "").replace('^"', "").replace('^', "")
    index = check_regex(raw,1)
    path = os.path.dirname(raw)
    dir = os.listdir(path)
    extension = raw[raw.rfind("."):]
    grab = [i for i in dir if extension in i]
    check = raw[:raw.find(index)].replace(path + '\\', "")
    tmp = [i for i in grab if check in i]
    return len(tmp)

def format_mkv(command, inputs):
    for i in inputs:
        command = command.replace(i, "{}")
    return command

def add_one(line, num_o, num_n):
    done = [line]
    path = os.path.dirname(line)
    linel = line.replace(path, "")
    for i in range(1, len_raw):
        if 'S' in num_o:
            z = num_o[4:]
            num_n = num_o[:4] + (str(int(z) + (i * s)).zfill(len(z)))
        else:
            num_n = num_o[0] + str(int(num_o[1:-1]) + (i*s)).zfill(len(num_o[1:-1])) + num_o[-1]
        final = linel.replace(num_o, num_n)
        done.append(path + final)
    return done

def process(liste):
    big = list()
    for i in liste:
        tmp = list()
        num, numE = check_regex(i,2)
        if num != numE:
            tmp = add_one(i, num, numE)
        if num == numE:
            for n in range(0, len_raw):
                tmp.append(num)
        big.append(tmp)
    return big

def check_regex(name, mode):
    regular = re.findall("[\s#._\[]\d+[\s._\]]", name)
    if not regular:
        season = re.findall("\w\d\d\w\d+", name)
        if season:
            previous = season[0]
            number = previous[4:]
            next = previous[:4] + str(int(number) + (1*s)).zfill(len(number))
        if not season:
            if TITLE and (name in ALL[len(ALL)-1] or name in ALL[len(ALL)-2]):
                return name, name
            else:
                print(Fore.RED + f"The file {name} is not named correctly.")
                print(Style.RESET_ALL)
                sys.exit()
    if regular:
        previous = regular[0]
        next = previous[0] + str(int(previous[1:-1]) + (1*s)).zfill(len(previous[1:-1])) + previous[-1]
    
    if mode == 1:
        return previous
    if mode == 2:
        return previous, next

def exist(gigalist):
    nope = list()
    less = gigalist.copy()
    less.pop(0)
    if TITLE and CHAPTER:
        less.pop(len(gigalist)-3)
    if TITLE and not CHAPTER:
        less.pop(len(gigalist)-2)

    for liste in less:
        for i in liste:
            i = i.replace('^', '')
            exists = os.path.exists(i)
            if not exists:
                nope.append(i)
    if nope:
        print(Fore.YELLOW + "\nThe following file(s) need to be renamed for the .bat to work proprely (they might also not exist):")
        [print(bruh) for bruh in nope]

def make(fi, clear, gigalist):
    make = clear
    for i in range(len(gigalist)):
        a = gigalist[i][fi]
        make = make.replace('{}', a, 1)
    L_DONE.append(make)

def write(liste, fo, font):
    f = open("batch.bat", "a", encoding="utf-8")
    f.write("chcp 65001 >nul \n")
    if fo == 0:
        [f.write(i + "\n") for i in liste]
    else:
        for i,j in zip(liste,font):
            line = i + j
            f.write(line + "\n")
    f.close

if __name__ == "__main__" : 
    list_fonts = list()
    try:
        f = sys.argv[1]
        if f == "-f":
            list_fonts = write_fonts(collect_font())
        else:
            f = 0
    except:
        f = 0
    mkv = input("Paste your MkvToolNix Command Here:\n\n")
    output = find_output(mkv)
    mkv_in = mkv.replace(output, "{}", 1)
    mkv_ready = format_mkv(mkv_in, find_all_input(mkv_in))
    len_raw = number_raw_input(ALL)
    if len_raw != 0:
        big_bertha = process(ALL)
        exist(big_bertha)
        [make(i,mkv_ready, big_bertha) for i in range(len_raw)]
        write(L_DONE, f, list_fonts)
    else:
        print(Fore.RED + f"Could'nt find the raw used for {ALL[1]}")
        print(Style.RESET_ALL)
    print(Fore.GREEN + "Done")
    input()
    print(Style.RESET_ALL)
