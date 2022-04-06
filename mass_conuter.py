import time
import json
import os
# import jellyfish
from unit_changer import *

# TODO: wczytać ffodcentral plik ddo listy słownika z listami
# TODO: stworzyć listę z rozsądnymi unitami i pozmieniać błędne/zastanowić się co z resztą
# TODO: wczytać new_recipes i tam gdzie będzie pasowało obliczyc i dodac masę
# TODO: zastanowić się co z resztą vol.2

# a = jellyfish.levenshtein_distance(u'jellyfish', u'smellyfish')
# b = jellyfish.jaro_distance(u'jellyfish', u'smellyfish')
# c = jellyfish.damerau_levenshtein_distance(u'jellyfish', u'jellyfihs')

# print(a)
# print(b)
# print(c)

unique_units = set()

fc = read_json('foodcentral.json')

for food in fc:
    for i in food['foodPortions']:
        unique_units.add(i['portionDescription'])
        
save_json('unique_units_foodcentral.json', list(unique_units))