from bs4 import BeautifulSoup, element
import asyncio
import aiohttp
import time
import json
import os

# TODO: w pętli tworzyć dla każdej strony słownik, appendować go do jsona, jeżeni nic w nim nie ma (chyba nie trzeba sprytniej...)
# TODO: uładnianie i unifikowanie danych (usuwanie dziwnych znaków, może same małe litery itd)
# TODO: dodać error handling, bo przy 10000 przepisów na penwo coś się spierdoli

'''
struktura json'a:
[
    dla każdego przepisu:
    {"id": ...,
    "title:...
    "instruction":...,
    "ingirdients": [{"name":..., "quantity":..., "unit":...}]},
]
'''

start_time = time.perf_counter()

# urls range
base_url = r"https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/"
start_id = 10000
end_id = 99989

# to prettify strings
delchars = "!@#$%^&*_+-=~`{}|[]:\"\\;'<>?/\t\r\n"


# fetching html from url
async def fetch(session, url):
    response = await session.get(url)
    response.raise_for_status()
    html = await response.text()
    return html



# parsing html and extracting wanted info
async def parse(session, url_id):
    url = base_url + str(url_id)
    try:
        html = await fetch(session=session, url=url)
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
        add_recipe_to_json(recipe_dict)
        return recipe_dict


# async function made to run all other async functions in "__main__"
async def async_main():
    async with aiohttp.ClientSession() as session:
        # makes list fo "tasks" to do asynchronously
        tasks = []

        for i in range(start_id, end_id):
            url_id = i
            tasks.append(asyncio.ensure_future(parse(session, url_id)))

        await asyncio.gather(*tasks)


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
        # json.dump(recipe, file)


if __name__ == "__main__":
    check_if_json_exists()

    # some windows error handling
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # main runner
    asyncio.run(async_main())

    # feel the speed
    print(f"\ntime elapsed:  {time.perf_counter() - start_time}")
