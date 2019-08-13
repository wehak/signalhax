# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:49:39 2019

@author: WEYHAK

Program for å sammenligne to eller flere tegningslister

"""

import re
import win32clipboard

##########
# config #
##########

separator = "," # hvilken separator som skal brukes i output-streng
#search_str_list = [
#    "[A-Z]{3}-[0-9]{2}-[A-Z]-[0-9]{5}",  # leter etter prosjektnr, feks MIP-00-A-12345
##    "BE-[0-9]{6}",
##    "EH-[0-9]{6}",
##    "EL-[0-9]{6}",
#    "KO-[0-9]{6}", # overbygning, feks skiltplantabell
##    "KU-[0-9]{6}",
#    "SA-[0-9]{6}", # leter etter signaltegning, feks SA-123456
##    "TE-[0-9]{6}",
#    "S.[0-9]{6}" # leter etter gammelt signalnr, feks S.123456
#    ]
new_doknr = "SA-[0-9]{6}[-\d]{0,4}" # leter etter signaltegning, feks SA-123456
old_doknr = "S.[0-9]{6}-{0,1}[0-9]{0,3}" # leter etter gammelt signalnr, feks S.123456

############
# function #
############

class Document_set():
    def __init__(self, document_set, alias):
        self.document_set = document_set
        self.alias = alias

def get_document_set():
    while True:
        # instruksjoner til bruker
        print("Kopiér kolonne fra Excel. Data hentes i fra utklippstavlen.")
        input("ENTER for å fortsette ...")
        
        # input hentes fra utklippstavle
        win32clipboard.OpenClipboard()
        input_str = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        
        doknr_list = re.findall(old_doknr, input_str, re.I)
        doknr_list = [item.replace("S.", "SA-") for item in doknr_list]
            
        for item in re.findall(new_doknr, input_str, re.I):
            doknr_list.append(item)
        print(doknr_list)
        
#        # konverterer streng til liste. separerer strenger delt av mellomrom eller newline
#        input_list = input_str.split()
#        
#        # løkke for å søke etter hver av strengene definert i search_str_list
#        for search_str in search_str_list: 
#            
#            # løkke for å søke gjennom alle rader i input-lista
#            temp_list = []
#            for row in input_list:
#                
#                # skriver verdier over i output-liste dersom de matcher søkebetingelser
#                if re.match(search_str, row.upper()):
#                    temp_list.append(row)
                    
            # konverterer liste til sett for å fjerne dupliserte verider
        if len(doknr_list) > 0:
            print("{} verdier funnet ({} unike)" .format(len(doknr_list), len(set(doknr_list))))
            user_input = input("Navn på tegningslisten? ")
            temp_set_obj = Document_set(set(doknr_list), user_input)
            return temp_set_obj
        else:
            print("Ingen verdier funnet.")

def print_report(input_set_obj, input_set_list):
    print("*******************")
    print("Tegningsliste: {}" .format(input_set_obj.alias))
    for document_set in input_set_list:
        if document_set.alias == input_set_obj.alias:
            continue
        else:
            print("{} av {} nummer funnet i {}:" .format(
                    len(input_set_obj.document_set.intersection(document_set.document_set)),
                    len(input_set_obj.document_set),
                    document_set.alias
                    ))
            print(separator.join(
                    input_set_obj.document_set.intersection(
                            document_set.document_set
                            )))    

############
# program #
############

# henter 2 eller flere tegingslister fra bruker
documents_set_list = []
documents_set_list.append(get_document_set())        
while True:
    documents_set_list.append(get_document_set())
    if input("Ny liste? Y/N ").upper() == "Y":
        continue
    else:
        break

# oppsummerer stats per tegningsliste
for documents_set in documents_set_list:
    print_report(documents_set, documents_set_list)

# finner nummer som går igjen i alle listene
print("*******************")
temp_tuple = documents_set_list[0].document_set.intersection(documents_set_list[1].document_set)
for i, documents_set in enumerate(documents_set_list, 1):
    if i + 1 < len(documents_set_list):
        temp_tuple = set(temp_tuple).intersection(documents_set_list[i+1].document_set)
    else:
        break
print("{} nummer funnet i alle tegningslistene:" .format(len(temp_tuple)))
print(separator.join(temp_tuple))

# unngå at terminal lukkes umiddelbart
print("*******************")
input("Trykk ENTER for å avslutte")