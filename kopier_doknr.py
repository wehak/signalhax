import re
import win32clipboard

################
# instillinger #
################

separator = "," # hvilken separator som skal brukes i output-streng
search_str_list = [
    "[A-Z]{3}.[0-9]{2}.[A-Z].[0-9]{5}",  # leter etter prosjektnr, feks MIP-00-A-12345
#    "BE-[0-9]{6}",
#    "EH-[0-9]{6}",
#    "EL-[0-9]{6}",
    "KO-[0-9]{6}-{0,1}[0-9]{0,3}", # overbygning, feks skiltplantabell
#    "KU-[0-9]{6}",
    "SA-[0-9]{6}[-\d]{0,4}", # leter etter signaltegning, feks SA-123456
#    "TE-[0-9]{6}",
    "S.[0-9]{6}-{0,1}[0-9]{0,3}" # leter etter gammelt signalnr, feks S.123456
    ]


# henter data fra utklippstavlen og filrerer ut gyldige tegningsnr
def filter_and_list():
    input("Data hentes i fra utklippstavlen. Kopiér tekst og trykk ENTER for å fortsette...")
    
    # input hentes fra utklippstavle
    win32clipboard.OpenClipboard()
    input_str = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    
    # finner all tekst definert i "search_str_list"
    # se dokumentasjon for re.findall() for forklaring: https://docs.python.org/3/howto/regex.html#regex-howto
    f = lambda x : re.findall(x, input_str, re.I)
    return [y for y in (f(x) for x in search_str_list) if len(y) > 0]

# setter inn bindestrek i prosjektnr
def clean_hyphen(lst):
    for series in lst:
        print(series[0])
        if re.search("[A-Z]{3}", series[0], re.I):
            series = insert_hyphen(series)
    return lst

def insert_hyphen(lst):
    # new_list = []
    # for string in lst:
    new_list = ["{}-{}-{}-{}" .format(string[:3], string[4:6], string[7:8], string[9:]) for string in lst]
    #     new_list.append("{}-{}-{}-{}".format(string[:3], string[4:6], string[7:8], string[9:]))
    return new_list


############
# program #
############

# meny
user_choice = ""
docnr_list = []

while True:    
    docnr_list = filter_and_list()
    while len(docnr_list) == 0:
        print("Ingen verdier funnet.")
        docnr_list = filter_and_list()
    
    docnr_list = clean_hyphen(docnr_list)
      
    while True:
        for i, output_list in enumerate(docnr_list, 1):
            print("---------------------------------------------------")
            print("Liste #{}, {} nummer funnet ({} unike):" .format(i, len(output_list), len(set(output_list))))
            print(separator.join(output_list))
        
        print("---------------------------------------------------")
        print("Velg et tall for å kopiere liste til utklippstavle.")
        print("'N' for å laste inn en ny liste.")
        print("'Q' for å avslutte.")
        
        user_choice = input()
            
        if user_choice == "Q" or user_choice == "q":
            raise SystemExit
        if user_choice == "N" or user_choice == "n":
            break
        else:
            try:
                user_choice = int(user_choice)
            except:
                print("Feil: '{}' er ikke et gyldig valg." .format(user_choice))
                continue
            
            if user_choice <= len(docnr_list) and user_choice > 0:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(separator.join(docnr_list[user_choice-1]))
                win32clipboard.CloseClipboard()
                print("Kopiert OK.")
            else: 
                print("Feil: Må være et tall mellom 1 og {}." .format(len(docnr_list)))