from argparse import ArgumentParser
from colorama import Fore, Style, init, Back
import re, os, sys, pyperclip, locale, ctypes
from shlex import split as sh_split

init(convert = True)

def print_message():
    if (locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()] == "fr_FR"):
        print(f"{Fore.BLUE}Versi{Fore.WHITE}on Franç{Fore.RED}aise")
        print(Fore.WHITE + "Les polices doivent être rangée dans un dossier pour chaque épisodes :\ns'il y a 25 épisodes alors il faudra 25 dossiers avec des polices dans chacun d'entre eux.")
        print("Attention, vous ne devez pas ajouter vous même les polices dans le mkv, les attachements ne doivent pas contenir de police contenu dans ces dossiers sous peine de doublons.")
        print("Coller le chemin complet du dossier qui contient tout les sous dossiers pour les polices :" + Style.RESET_ALL)
    else:
        print("Eng Ver")
        print("Fonts must be in a folder for each episode: \nif there's 25 ep then you must have 25 folders with fonts in it")
        print("Be aware that you don't need to include fonts in the mkv, attachements must not contain fonts or they will be duplicated.")
        print("Paste the path to the folder containing all the sub folders containing fonts :")

def collect_font() -> list:
    print_message()
    giga: list[str] = list()
    path: str = str(input())
    folder: list[str] = os.listdir(path)
    for sub in folder:
        sub = os.path.join(path, sub)
        try:
            tmp: list[str] = os.listdir(sub)
            if tmp:
                true_font: list[str] = list()
                for font in tmp:
                    if ".otf" in font.lower() or ".ttf" in font.lower() or ".ttc" in font.lower():
                        true_font.append(os.path.join(path, sub, font))
                if true_font:
                    giga.append(true_font)
        except:
            pass
    return giga

def write_font(array: list) -> list:
    list_line: list[str] = list()
    standard_ttf = ' --attachment-name ^"{}^" --attachment-mime-type application/x-truetype-font --attach-file ^"{}^"'
    standard_otf = ' --attachment-name ^"{}^" --attachment-mime-type application/vnd.ms-opentype --attach-file ^"{}^"'
    standard_ttc = ' --attachment-name ^"{}^" --attachment-mime-type font/collection --attach-file ^"{}^"'
    for fonts in array:
        line: str = str()
        for font in fonts:
            if ".otf" in font.lower():
                tmp: str = standard_otf.replace('{}', os.path.basename(font), 1).replace('{}', font, 1)
            if ".ttf" in font.lower():
                tmp: str = standard_ttf.replace('{}', os.path.basename(font), 1).replace('{}', font, 1)
            if ".ttc" in font.lower():
                tmp: str = standard_ttc.replace('{}', os.path.basename(font), 1).replace('{}', font, 1)
            line = line + tmp
        list_line.append(line)
    return list_line

def str_number(file: str, mode: int, typef: str) -> str:
    if typef == "Pass":
        file = file.replace(os.path.dirname(file), '')
        season: list[str] = re.findall("\w\d\d\w\d+", file)
        if season:
            return season[0][4:] if mode == 1 else season[0]
        regular: list[str] = re.findall("[\s#._\[]\d\d+[\s._\]]", file)
        if regular:
            return regular[0][1:-1] if mode == 1 else regular[0]
        else:
            print(Fore.RED + f"{file} not named proprely.")
            sys.exit()
    if typef == "title":
        int_groups = re.findall("([0-9]+)", file)
        if len(int_groups) != 1:
            return file
        else:
            s_regular: list[str] = re.findall("[\s#._]\d\d+", file)
            if s_regular:
                return s_regular[0][1:] if mode == 1 else s_regular[0]
            else:
                return file

def count_times(array: list) -> int:
    """
    Messy but fonctionnal, return the number of time the command line will be duplicated
    """
    file: str = array[0][array[0].rfind('\\') + 1:].replace('^', '')
    index: str = str_number(file, 0, "Pass")
    dir: list[str] = os.listdir(os.path.dirname(array[0].replace('^', '')))
    extension: str = file[file.rfind('.'):]
    left: str = file[:file.find(index)].replace(os.path.dirname(file) + '\\', '')
    right: str = file[file.find(index) + len(index):]
    first_pass: list[str] = [i for i in dir if extension in i]
    count: int = 0
    for i in first_pass:
        if left in i and right in i:
            count += 1
    print(count)
    return count

def format_mkv(command: str, source: list) -> str:
    for i in source:
        if i == "inputs":
            tmp = source[i]
            for j in tmp:
                command = command.replace(j, "{}")
            continue
        command = command.replace(source[i], "{}")
    return command

def exist(humongous: list, source: dict) -> None:
    nope: list[str] = list()
    for array in humongous:
        for i in array:
            if i == source.get("output") or i == source.get("title"):
                continue
            i = i.replace('^', '')
            if not os.path.exists(i):
                nope.append(i)
    if nope:
        print(Fore.YELLOW + "\nThe following file(s) need to be renamed for the .bat to work proprely (they might also not exist):")
        [print(bruh) for bruh in nope]

def make(ready: str, humongous: list):
    done: list[str] = list()
    for index in range(length):
        make: str = ready
        for i in range(len(humongous)):
            tmp: str = humongous[i][index]
            make = make.replace('{}', tmp, 1)
        done.append(make)
    return done

def write_bat(done: list, f: bool, font_list: list):
    with open("batch.bat", 'a', encoding="utf-8") as f:
        f.write("chcp 65001 >nul\n")
        if not f:
            [f.write(i + '\n') for i in done]
        else:
            for i, j in zip(done, font_list):
                f.write(i + j + '\n')

def get_source(command: str) -> dict:
    args: list = sh_split(command)
    source: dict = dict()
    for c,i in enumerate(args):
        if i == "--output":
            source["output"] = args[c + 1][1:-1] if "^" in args[c + 1] else args[c + 1]
            source["inputs"] = list()
        if i == '(' or i == "^^(^":
            source["inputs"].append(args[c + 1][1:-1] if "^" in args[c + 1] else args[c + 1])
        if i == "--chapters":
            source["chapter"] = args[c + 1][1:-1] if "^" in args[c + 1] else args[c + 1]
        if i == "--title" and len(args[c + 1]) != 0 and args[c + 1] != "^^":
            source["title"] = args[c + 1][1:-1] if "^" in args[c + 1] else args[c + 1]
    # print(source)
    return source

def add_one(file: str, num: str, typef: str) -> list:
    done: list = [file]
    path = os.path.dirname(file)
    line = file.replace(path, "")
    for i in range(1, length):
        if "S" in num:
            new_num = num[:4] + (str(int(str_number(line,1, typef)) + i).zfill(len(num) - 4))
        else:
            if typef == "Pass":
                new_num = num[0] + (str(int(str_number(line,1, typef)) + i).zfill(len(num) - 2)) + num[-1]
            if typef == "title":
                new_num = num[0] + (str(int(str_number(line,1, typef)) + i).zfill(len(num) - 1))
        done.append(path + line.replace(num, new_num))
    return done

def process(source_dict: dict) -> list:
    humongus: list[list[str]] = list()
    for i in source_dict:
        if i == None:
            continue
        if i == "inputs":
            inputs: list[str] = source_dict[i]
            for j in inputs:
                tmp: list[str] = list()
                num: str = str_number(j, 0, "Pass")
                tmp: list[str] = add_one(j, num, "Pass")
                humongus.append(tmp)
            continue

        tmp: list[str] = list()
        typef = "title" if i == "title" else "Pass"
        num = str_number(source_dict[i], 0, typef)
        if num == source_dict[i]:
            for _ in range(0, length):
                tmp.append(num)
        if num != source_dict[i]:
            tmp = add_one(source_dict[i], num, typef)
        humongus.append(tmp)
    return humongus

def main():
    font_list: list[str] = list()
    parser = ArgumentParser(description="Yolobatch - Makes your life easer by creating batch for you. A script for Mkvtoolnix.")
    parser.add_argument("-f", default=False, action="store_true", help="Copy the path of the folder with fonts to add them for each mkv")
    parser.add_argument("-drift", default=False, action="store_true", help="Un petit easter egg")
    args = parser.parse_args()
    if args.drift:
        print(Back.WHITE, end='')
        print(Fore.LIGHTMAGENTA_EX + "Drifters : Les Drifters de l'enfer.\nDans un Japon futuriste, un groupe de rebels a décidé de prendre les rues d'assaut\nen pratiquant le drifting, une discipline de conduite extrême qui consiste à")
        print("glisser et à déraper avec style. Menés par leur leader charismatique Ryo Kazuma, ces drifters\nse battent contre les forces de l'ordre et les gangsters qui contrôlent la ville.")
        print("Mais ils vont rapidement se rendre compte que leur lutte va bien au-delà des\nfrontières de la réalité, et qu'ils sont en réalité plongés dans un conflit cosmique")
        print("entre des êtres divins et des démons. Pour sauver le monde, ils vont devoir\napprendre à maîtriser leurs véhicules et leurs pouvoirs extraordinaires, et affronter\ndes ennemis de plus en plus puissants.")
    if args.f:
        font_list = write_font(collect_font())
    input("Make sure you've copied the MkvtoolNix command line. Press Enter to continue\n")
    while True:
        command = pyperclip.paste()
        if "mkvmerge" in command:
            break
        else:
            input("It seem's that you have not copied the commande line. Press Enter when you're done.\n")
    source: dict = get_source(command)
    ready: str = format_mkv(command, source)
    global length
    length = count_times(source["inputs"])
    if length:
        humongous: list[list[str]] = process(source)
        exist(humongous, source)
        write_bat(make(ready,humongous), args.f, font_list)
    else:
        print(Fore.RED + f"Could'nt find the raw used for {source['inputs'][0]}" + Style.RESET_ALL)
    print(Fore.GREEN + "Done" + Style.RESET_ALL + Back.RESET)
    input()

if __name__ == "__main__":
    main()
