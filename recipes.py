from bs4 import BeautifulSoup
import requests

# TODO: zastanowić się, czy starcza nam takie proste przejście po każdym indeksie, czy coś lepszego co uruchamia selenium
# TODO: wyciągnąć z każdej strony 1) nazwę, 2) listę ze składnikami, 3) instrukcję, 4) coś jeszcze?
# TODO: w pętli tworzyć dla każdej strony słownik, appendować go do jsona, jeżeni nic w nim nie ma (chyba nie trzeba sprytniej...)

'''
generalnie to wszystkie przepisy zawierają się w tym zakresie (chyba)
prawdopodobnie nie trzeba będzie uruchomić selenium, 
bo dane są ukryte za html, a js je odkrywa, a nie są dodatkowo ściągane z serwera.
po przemyśleniu też raczej nie trzeba zaczynać z scrapy, bo to jakiś za potężne narzędzie
chociaż strasznie mnie kusi żeby to tak ładnie zrobić xdddd 
'''

base_url = r"https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/"
start_id = 10000
end_id = 99989

response = requests.get(base_url + str(start_id))
# print(response.text) # jprd ale syf mają xd

soup = BeautifulSoup(response.text, 'html.parser')
recipe_title = soup.find('h3', attrs={"style": "font-family: Helvetica;"})
print(recipe_title.text)

recipe_ingridients_table = soup.find('table', attrs={"id": "myTable"}).find_all('tr')

for ingridient_info in recipe_ingridients_table[1:]:
    print(ingridient_info.find_all('td')[0:2])
