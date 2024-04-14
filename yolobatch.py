import os, re, pyperclip, copy, platform, locale, ctypes, time
from argparse import ArgumentParser
from shlex import split as sh_split
from colorama import Fore, Style, init
from enum import Enum
from typing import Tuple, List

VERSION = 3.0
SYSTEM = platform.system()
WARNING = True

init(convert = True)

re_pattern_seasons = r"[S|s]\d+[E|e]\d+" # S01E01
re_pattern_general = r"[\s#._\[]\d+[\s._\]]" # _01_, [01], .01., #01 ,  01 , or any mix match of theses examples also works
re_pattern_shitier = r"\d+x\d+" # embrace chaos 01x01
re_pattern_lazynes = r"\d+" # for the one who are to lazy to proprely name file

class RegexType(Enum):
    SEASON = 1
    GENERAL = 2
    SHITTIER = 3
    LAZYNESS = 4

class Order(Enum):
    INPUT = 1
    CHAPTER = 2
    TITLE = 3
    OUTPUT = 4

class RegexNameException(Exception):
    pass

class NotACommandLine(Exception):
    pass

class Source:
    def __init__(self) -> None:
        self.source : dict = dict()
        self.order : list = list()

    def check_all(self) -> None:
        for elem in self.source:
            if elem == "inputs":
                [get_regex_result(os.path.basename(i)) for i in self.source[elem]]
                continue
            if elem == "title":
                try:
                    get_regex_result(os.path.basename(self.source[elem]))
                except RegexNameException:
                    print("Title will not be incremented")
                continue
            get_regex_result(os.path.basename(self.source[elem]))

class Args:
    def __init__(self) -> None:
        self.folder : str = ""

    def set_folder(self, path : str):
        if os.path.exists(path):
            self.folder = path
        else:
            raise FileNotFoundError(path)

def arg_parse() -> Args:
    parser = ArgumentParser(description= f"Yolobatch (v{VERSION})")
    parser.add_argument("-f", required=False, action="store", help="Path to the folder with fonts for mux")

    args = parser.parse_args()

    arg = Args()
    if args.f:
        arg.set_folder(args.f)

    return arg

def print_message():
    if (locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()] == "fr_FR"):
        print(f"{Fore.BLUE}Versi{Fore.WHITE}on Franç{Fore.RED}aise")
        print(Fore.WHITE + "Les polices doivent être rangée dans un dossier pour chaque épisodes :\ns'il y a 25 épisodes alors il faudra 25 dossiers avec des polices dans chacun d'entre eux.")
        print("Attention, vous ne devez pas ajouter vous même les polices dans le mkv, les attachements ne doivent pas contenir de police contenu dans ces dossiers sous peine de doublons.")
        print("Si vous avez un doute, supprimez le batch et relancez le script" + Style.RESET_ALL)
    else:
        print("Eng Ver")
        print("Fonts must be in a folder for each episode: \nif there's 25 ep then you must have 25 folders with fonts in it")
        print("Be aware that you don't need to include fonts in the mkv, attachements must not contain fonts located in theses folder or they will be duplicated.")
        print("If you have any doubt, delete the batch and launch the script again")

def font_attachment(fonts : List[str]) -> str:
    line : str = ""
    std_ttf = ' --attachment-name ^"{}^" --attachment-mime-type application/x-truetype-font --attach-file ^"{}^"'
    std_otf = ' --attachment-name ^"{}^" --attachment-mime-type application/vnd.ms-opentype --attach-file ^"{}^"'
    std_ttc = ' --attachment-name ^"{}^" --attachment-mime-type font/collection --attach-file ^"{}^"'

    for font in fonts:
        if font.lower().endswith(".ttf"):
            line += std_ttf.replace("{}", os.path.basename(font), 1).replace("{}", font, 1)
        if font.lower().endswith(".otf"):
            line += std_otf.replace("{}", os.path.basename(font), 1).replace("{}", font, 1)
        if font.lower().endswith(".ttc"):
            line += std_ttc.replace("{}", os.path.basename(font), 1).replace("{}", font, 1)

    if SYSTEM != "Windows":
        line = line.replace('^', '')
    return line

def get_attachments(folder : str) -> List[str]:
    print_message()
    dirs : list[str] = os.listdir(folder) # I see you little linux nerd
    dirs = list(map(lambda file : os.path.join(folder, file), dirs))
    attachments : list[str] = list()
    for dir in dirs:
        if not os.path.isdir(dir):
            continue
        sub : list[str] = os.listdir(dir)
        fonts : list[str] = [os.path.join(dir, file) for file in sub
                             if file.lower().endswith(".ttf")
                             or file.lower().endswith(".otf")
                             or file.lower().endswith(".ttc")]
        if fonts:
            attachments.append(font_attachment(fonts))
    return attachments

def get_command() -> str:
    command : str = ""
    while True:
        command = pyperclip.paste()
        if "mkvmerge" in command:
            break
        input("It seem's that you have not copied the commande line. Press Enter when you're done.\n")
    return command

def parse_command(command : str) -> Source:
    """
    Returns a dict with all inputs, output, chapter and title in the command line
    """
    args : list = sh_split(command)
    source : Source = Source()
    for c,i in enumerate(args):
        if i == "--output":
            source.source["output"] = args[c + 1][1:-1] if "^" in args[c + 1] else args[c + 1]
            source.source["inputs"] = list()
            source.order.append(Order.OUTPUT)

        if i == '(' or i == "^^(^":
            source.source["inputs"].append(args[c + 1][1:-1] if "^" in args[c + 1] else args[c + 1])
            source.order.append(Order.INPUT)

        if i == "--chapters":
            source.source["chapter"] = args[c + 1][1:-1] if "^" in args[c + 1] else args[c + 1]
            source.order.append(Order.CHAPTER)

        if i == "--title" and len(args[c + 1]) != 0 and args[c + 1] != "^^":
            source.source["title"] = args[c + 1][1:-1] if "^" in args[c + 1] else args[c + 1]
            source.order.append(Order.TITLE)

    if not source.source:
        raise NotACommandLine(command)

    source.check_all()

    return source

def remove_source(command : str, source : dict) -> str:
    """
    Returns command with inputs and output removed from command
    """
    for i in source:
        if i == "inputs":
            for j in source[i]:
                command = command.replace(j, "{}")
            continue
        command = command.replace(source[i], "{}")
    return command

def regex_name(path : str):
    print(Fore.RED + f"File : \"{path}\" does not fit any regex pattern." + Style.RESET_ALL)
    print("If the file is named proprely, please create an issue with the name of the file.")
    raise RegexNameException()

def get_regex_result(path : str) -> Tuple[str, int]:
    """
    Returns the first result of the matching regex and the enum assossiated.
    Throws RegexNameException when no regex is found
    """
    if re.search(re_pattern_seasons, path):
        return re.findall(re_pattern_seasons, path)[0], RegexType.SEASON
    if re.search(re_pattern_general, path):
        return re.findall(re_pattern_general, path)[0], RegexType.GENERAL
    if re.search(re_pattern_shitier, path):
        return re.findall(re_pattern_shitier, path)[0], RegexType.SHITTIER
    if re.search(re_pattern_lazynes, path):
        tmp = re.findall(re_pattern_lazynes, path)[0]
        if tmp == path[:path.rfind('.')]:
            return tmp, RegexType.LAZYNESS
        regex_name(path)
    regex_name(path)

def count_times(input_file : str) -> int:
    """
    Messy but fonctionnal, return the number of time the command line will be duplicated
    """
    file : str = os.path.basename(input_file).replace('^', '')
    index : str = get_regex_result(file)[0]
    dir : list[str] = os.listdir(os.path.dirname(input_file.replace('^', '')))
    extension : str = file[file.rfind('.'):]
    left : str = file[:file.find(index)].replace(os.path.dirname(file) + '\\', '')
    right : str = file[file.find(index) + len(index):]
    first_pass : list[str] = [i for i in dir if extension in i]
    count : int = 0
    for i in first_pass:
        if left in i and right in i:
            count += 1
    return count

def write_batch(lines : List[str], args : Args) -> None:
    name : str = "batch.bat" if SYSTEM == "Windows" else "batch.sh"
    with open(name, 'a', encoding="utf-8") as f:
        if name.endswith(".bat"):
            f.write("chcp 65001 >nul\n")
        if args.folder:
            attachments : list[str] = get_attachments(args.folder)
            if len(attachments) != len(lines):
                print(Fore.RED + "Mix match length for attachments and mkvtoolnix command line, there are more attachments than files to mux or vise versa" + Style.RESET_ALL)
            for line, att in zip(lines, attachments):
                f.write(line + ' ' + att + '\n')
        else:
            for line in lines:
                f.write(line + '\n')

def next_file(path : str, incr : int, check : bool = True, chapter : bool = False) -> str:
    if not incr:
        return path

    dir : str = os.path.dirname(path)
    file : str = os.path.basename(path)

    if chapter:
        try:
            match, type = get_regex_result(file)
        except RegexNameException:
            return file

    match, type = get_regex_result(file)
    res : str = ""
    
    if type == RegexType.SEASON:
        res = match[:4] + str(int(match[4:]) + incr).zfill(len(match) - 4)

    elif type == RegexType.GENERAL:
        res = match[0] + str(int(match[1:-1]) + incr).zfill(len(match) - 2) + match[-1]

    elif type == RegexType.SHITTIER:
        res = match[:match.find('x') + 1] + str(int(match[match.find('x') + 1:]) + incr).zfill(len(match) - len(match[:match.find('x') + 1]))

    elif type == RegexType.LAZYNESS:
        res = str(int(match) + incr).zfill(len(match))

    next : str = os.path.join(dir, file.replace(match, res))
    global WARNING
    if check and not os.path.exists(next.replace('^', '')):
        if WARNING:
            print(Fore.YELLOW + "The following file either does not exist or is not name proprely:")
            WARNING = False
        print(Fore.YELLOW + next + Style.RESET_ALL)
    return next

def make_lines(source : Source, model : str, times : int) -> List[str]:
    lines : List[str] = list()
    remaining : int = times
    while remaining:
        line : str = copy.copy(model)
        input_count : int = 0

        for order in source.order:
            if order == Order.INPUT and input_count < len(source.source["inputs"]):
                line = line.replace("{}", next_file(source.source["inputs"][input_count], times - remaining), 1)
                input_count += 1

            if order == Order.OUTPUT:
                line = line.replace("{}", next_file(source.source["output"], times - remaining, False), 1)

            if order == Order.TITLE:
                line = line.replace("{}", next_file(source.source["title"], times - remaining, False, True), 1)

            if order == Order.CHAPTER:
                line = line.replace("{}", next_file(source.source["chapter"], times - remaining), 1)

        lines.append(line)
        remaining -= 1
    return lines

def main():
    args : Args = arg_parse()
    command : str = get_command()
    source : Source = parse_command(command)
    model : str = remove_source(command, source.source)
    times : int = count_times(source.source["inputs"][0])
    if times:
        lines : list[str] = make_lines(source, model, times)
        write_batch(lines, args)
        print(Fore.GREEN + str(times) + Style.RESET_ALL)

if __name__ == '__main__':
    start = time.perf_counter()
    main()
    print(time.perf_counter() - start)
