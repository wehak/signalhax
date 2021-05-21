
import re
import win32clipboard

from doknr_searcher import filter_and_list
from doknr_searcher import clean_hyphen
from doknr_searcher import old_to_new_s

separator = "," # hvilken separator som skal brukes i output-streng

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
    
    # vasker protek nummer
    docnr_list = clean_hyphen(docnr_list)

    # S. til SA-
    docnr_list = old_to_new_s(docnr_list)
      
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