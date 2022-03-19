from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time

# TODO: zrobić do wysyłania zapytań i parsowania funkcję asynchroniczną!!!
# TODO: zastanowić się, czy starcza nam takie proste przejście po każdym indeksie, czy coś lepszego co uruchamia selenium
# TODO: wyciągnąć z każdej strony 1) nazwę, 2) listę ze składnikami, 3) instrukcję, 4) coś jeszcze?
# TODO: w pętli tworzyć dla każdej strony słownik, appendować go do jsona, jeżeni nic w nim nie ma (chyba nie trzeba sprytniej...)
# TODO: uładnianie i unifikowanie danych (usuwanie dziwnych znaków, może same małe litery itd)
# TODO: dodać error handling, bo przy 10000 przepisów na penwo coś się spierdoli

'''
generalnie to wszystkie przepisy zawierają się w tym zakresie (chyba)
prawdopodobnie nie trzeba będzie uruchomić selenium, 
bo dane są ukryte za html, a js je odkrywa, a nie są dodatkowo ściągane z serwera.
po przemyśleniu też raczej nie trzeba zaczynać z scrapy, bo to jakieś za potężne narzędzie
'''

start_time = time.perf_counter()

# urls range
base_url = r"https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/"
start_id = 10000
end_id = 99989

# to prettify strings
delchars = "!@#$%^&*()_+-=~`{}|[]:\"\\;'<>?/\t\r\n"


# fetching html from url
async def fetch(session, url):
    response = await session.get(url)
    response.raise_for_status()
    html = await response.text()
    return html


# parsing html and extracting wanted info
async def parse(session, url):
    try:
        html = await fetch(session=session, url=url)
    except Exception as e:
        print(e) # trzzeba pewnie rozwinąć
    else:
        soup = BeautifulSoup(html, 'lxml')
        recipe_title = soup.find('h3', attrs={"style": "font-family: Helvetica;"})
        print(recipe_title.text)

        recipe_ingridients_table = soup.find('table', attrs={"id": "myTable"}).find_all('tr')

        for ingridient_info in recipe_ingridients_table[1:]:
            infos = ingridient_info.find_all('td')[0:3]
            ingridient = infos[0].text
            quantity = infos[1].text
            unit = infos[2].text
            
            print(f"{quantity} {unit} of {ingridient}")
            
        recipe_instructions = soup.find('div', attrs={"id": "steps"})
        print(recipe_instructions.text.translate(str.maketrans('', '', delchars)).strip()) # brzydkie dziwne znaki i odstępy, może regex? xd

        return [recipe_title, recipe_ingridients_table, recipe_instructions]


# async function made to run all other async functions in "__main__"
async def async_main():
    async with aiohttp.ClientSession() as session:
        # makes list fo "tasks" to do asynchronously
        tasks = []
        
        for i in range(start_id, start_id+10):
            url = base_url + str(i)
            tasks.append(asyncio.ensure_future(parse(session, url)))

        await asyncio.gather(*tasks)
        

if __name__ == "__main__":
    # some windows error handling
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # main runner
    asyncio.run(async_main())
    
    # feel the speed
    print(f"\ntime elapsed:  {time.perf_counter() - start_time}")
