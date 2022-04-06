import time
from jellyfish import damerau_levenshtein_distance, jaro_similarity, jaro_winkler_similarity
from unit_changer import *
import pandas as pd
from tqdm import tqdm

# TODO: wczytać ffodcentral plik ddo listy słownika z listami
# TODO: stworzyć listę z rozsądnymi unitami i pozmieniać błędne/zastanowić się co z resztą
# TODO: wczytać new_recipes i tam gdzie będzie pasowało obliczyc i dodac masę
# TODO: zastanowić się co z resztą vol.2

start_time = time.perf_counter()


def name_match(name, names_dictionary):
    best_match_l = {"name": names_dictionary[0], "score": damerau_levenshtein_distance(name, names_dictionary[0])}
    best_match_j = {"name": names_dictionary[0], "score": jaro_similarity(name, names_dictionary[0])}
    best_match_jw = {"name": names_dictionary[0], "score": jaro_winkler_similarity(name, names_dictionary[0])}
        
    for ith_name in names_dictionary:
        damlev = damerau_levenshtein_distance(name, ith_name)
        jaro = jaro_similarity(name, ith_name)
        jaro_wink = jaro_winkler_similarity(name, ith_name)
        
        if best_match_l["score"] > damlev:
            best_match_l["score"] = damlev
            best_match_l["name"] = ith_name
        
        if best_match_j["score"] < jaro:
            best_match_j["score"] = jaro
            best_match_j["name"] = ith_name
            
        if best_match_jw["score"] < jaro_wink:
            best_match_jw["score"] = jaro_wink
            best_match_jw["name"] = ith_name
        
            
    # print(f"Name to match: {name}\n")    
    # print(f"Best match using damerau_levenshtein_distance: {best_match_l}")
    # print(f"Best match using jaro_similarity: {best_match_j}")
    # print(f"Best match using jaro_winkler_similarity: {best_match_jw}")
    
    return_stats = {"name": name, "best_damlev": best_match_l["name"], "best_damlev_score": best_match_l["score"],
                    "best_jaro": best_match_j["name"], "best_jaro_score": best_match_j["score"],
                    "best_jaro_wink": best_match_jw["name"], "best_jaro_wink_score": best_match_jw["score"]}
    
    return return_stats


def match_two_namelists(nameslist_one, namelist_two, threshold=0.6):
    names_matches = []
    
    for name in tqdm(nameslist_one, desc="Matched names"):
        match = name_match(name, namelist_two)
        
        if match["best_jaro_score"] > threshold and match["best_jaro_wink_score"] > threshold:
            names_matches.append(match)
    
    return names_matches


def save_dic_as_csv(dict, filename):
    df = pd.DataFrame(dict)
    df.to_csv(filename + ".csv")
    
        
if __name__ == "__main__":
    names_foodcentral = list(read_json('data/unique_names_foodcentral.json'))
    names_recipes = list(read_json('data/unique_names_recipes.json'))
    
    names_matches = match_two_namelists(names_recipes, names_foodcentral, threshold=0.8)
    save_dic_as_csv(names_matches, "data/names_matches2")
    
    units_foodcentral = list(read_json('data/unique_units_foodcentral.json'))
    units_recipes = list(read_json('data/unique_units_recipes.json'))
    
    unit_matches = match_two_namelists(units_recipes, units_foodcentral, threshold=0.8)
    save_dic_as_csv(unit_matches, "data/units_matches2")
    
    # feel the speed
    print(f"\nTime elapsed:  {time.perf_counter() - start_time}s")
