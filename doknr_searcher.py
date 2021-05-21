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
    for i in range(len(lst)):
        if re.search("[A-Z]{3}", lst[i][0], re.I):
            lst[i] = insert_hyphen(lst[i])
    return lst

def insert_hyphen(lst):
    new_list = ["{}-{}-{}-{}" .format(string[:3].upper(), string[4:6], string[7:8].upper(), string[9:]) for string in lst]
    return new_list


# konverterer gammel til nytt s-nr
def old_to_new_s(master_list):
    
    new_master_list = list()
    new_sub_list = list()
    has_new = (False, None)
    has_old = (False, None)
    
    # se gjennom hvert element i listen
    while master_list:
        sub_list = master_list.pop()
        # gammelt s-nr?
        if re.search("s.[0-9]{6}", sub_list[0], re.I):
            new_sub_list = ["SA-{}" .format(string[2:]) for string in sub_list] # ny liste med SA-
            has_old = (True, len(new_master_list))
        else:
            new_sub_list = sub_list
            if re.search("sa-[0-9]{6}", sub_list[0], re.I):
                has_new = (True, len(new_master_list))

        new_master_list.append(new_sub_list)

    # hvis master har både gamle og nye, slå de i sammen
    if has_new[0] and has_old[0]:
        new = new_master_list.pop(has_new[1])
        old = new_master_list.pop(has_old[1])

        new_master_list.append(new + old)
    
    return new_master_list