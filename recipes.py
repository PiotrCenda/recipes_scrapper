from bs4 import BeautifulSoup
import requests

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

# urls range
base_url = r"https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/"
start_id = 10000
end_id = 99989

# to prettify strings
delchars = "!@#$%^&*()_+-=~`{}|[]:\"\\;'<>?/\t\r\n"

response = requests.get(base_url + str(start_id))
# print(response.text) # jprd ale syf mają xd

# parsing html
soup = BeautifulSoup(response.text, 'lxml')
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
print(recipe_instructions.text.translate(str.maketrans('', '', delchars)).strip()) # brzydkie dziwne znaki i odstępy, najlepiej dodać jeden regex xd


# asynchronous solution
# loop = asyncio.get_event_loop()

# def do_thing(params):
#     async def get_rpc_info_and_do_chores(id):
#         # do things
#         response = perform_grpc_call(id)
#         do_chores(response)

#     async def get_httpapi_info_and_do_chores(id):
#         # do things
#         response = requests.get(URL)
#         do_chores(response)

#     async_tasks = []
#     for element in list(params.list_of_things):
#        async_tasks.append(loop.create_task(get_chan_info_and_do_chores(id)))
#        async_tasks.append(loop.create_task(get_httpapi_info_and_do_chores(ch_id)))

#     loop.run_until_complete(asyncio.gather(*async_tasks))