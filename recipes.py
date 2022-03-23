from bs4 import BeautifulSoup, element
import time
import json
import os
import requests
from multiprocessing.dummy import Pool as ThreadPool

# TODO: w pętli tworzyć dla każdej strony słownik, appendować go do jsona, jeżeni nic w nim nie ma (chyba nie trzeba sprytniej...)
# TODO: uładnianie i unifikowanie danych (usuwanie dziwnych znaków, może same małe litery itd)
# TODO: dodać error handling, bo przy 10000 przepisów na penwo coś się spierdoli

start_time = time.perf_counter()

# urls range
base_url = r"https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/"
start_id = 10000
end_id = 99989

# to prettify strings
delchars = "!@#$%^&*_+-=~`{}|[]:\"\\;'<>?/\t\r\n"


# fetching html from url
def fetch(url):
    response = requests.get(url=url)
    html = response.text
    return html


# parsing html and extracting wanted info
def parse(url_id):
    url = (base_url + str(url_id))
    try:
        html = fetch(url=url)
    except Exception as e:
        print(e)  # trzeba pewnie rozwinąć
    else:
        soup = BeautifulSoup(html, 'lxml')
        recipe_title = soup.find('h3', attrs={"style": "font-family: Helvetica;"})
        recipe_ingridients_table = soup.find('table', attrs={"id": "myTable"}).find_all('tr')
        recipe_instructions = soup.find('div', attrs={"id": "steps"})

        recipe_dict = create_recipe_dict(url_id=url_id, title=recipe_title,
                                         ingridients=recipe_ingridients_table,
                                         instuctions=recipe_instructions)
        return recipe_dict


def check_if_json_exists():
    if not os.path.exists('recipes.json'):
        f = open('recipes.json', 'w')
        f.write('[]')
        f.close()
        print('Created .json file')
    else:
        print('.json file exists')
        f = open('recipes.json', 'w')
        f.write('[]')
        f.close()


def create_recipe_dict(url_id: int, title: element.Tag, ingridients: list, instuctions: element.Tag) -> dict:
    recipe = {'url_id': url_id,
              'title': title.text,
              'ingridients': [],
              'instructions': instuctions.text.translate(str.maketrans('', '', delchars)).strip()}

    for ingridient_info in ingridients[1:]:
        infos = ingridient_info.find_all('td')[0:3]
        name = infos[0].text
        quantity = infos[1].text
        unit = infos[2].text

        recipe['ingridients'].append({'name': name, 'quantity': quantity, 'unit': unit})

    return recipe


def add_recipe_to_json(recipe: dict):
    with open('recipes.json', "r+") as file:
        data = json.load(file)
        print(len(data))
        data.append(recipe)
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()
        
        
def main():
    task_ids = []
    for url_id in range(start_id, end_id+1):
        task_ids.append(url_id)
    
    pool = ThreadPool(1000)

    results = pool.map(parse, task_ids)

    pool.close()
    pool.join()
    
    add_recipe_to_json(results)


if __name__ == "__main__":
    # self-explanatory
    check_if_json_exists()
    
    # main runner
    main()

    # feel the speed
    print(f"\ntime elapsed:  {time.perf_counter() - start_time}")
