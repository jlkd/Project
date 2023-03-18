import requests, random
from bs4 import BeautifulSoup

def add_pokemon_to_base_html(base_path, pokemon_name):
    # Retrieve Pokemon data from PokeAPI
    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon_name.lower())
    pokemon_data = response.json()
    # Retrieve sprite image URL
    sprite_url = pokemon_data['sprites']['front_default']

    # Load base HTML file
    with open(base_path, 'r') as f:
        html = f.read()

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Create new li element
    li = soup.new_tag('li', **{'class': 'animating', 'style': 'opacity: 1; top: 0px; left: 0px; transform: matrix(1, 0, 0, 1, 0, 0);'})

    # Create figure element
    figure = soup.new_tag('figure')
    a = soup.new_tag('a', href="https://www.pokemon.com/us/pokedex/" + pokemon_name.lower())
    img = soup.new_tag('img', src=sprite_url)
    a.append(img)
    figure.append(a)

    # Create div element with Pokemon info
    div = soup.new_tag('div', **{'class': 'pokemon-info'})
    p = soup.new_tag('p', **{'class': 'id'})
    span = soup.new_tag('span', **{'class': 'number-prefix'})
    span.string = '#'
    p.append(span)
    p.append(str(pokemon_data['id']))
    div.append(p)
    h5 = soup.new_tag('h5')
    h5.string = pokemon_name.capitalize()
    div.append(h5)
    for t in pokemon_data['types']:
        ability_div = soup.new_tag('div', **{'class': 'abilities'})
        span = soup.new_tag('span', **{'class': 'pill'})
        span['class'].append('background-color-{t["type"]["name"]}')
        span.string = t['type']['name'].capitalize()
        ability_div.append(span)
        div.append(ability_div)

    li.append(figure)
    li.append(div)

    # Find the results ul element and append the new li element
    results_ul = soup.find('ul', {'class': 'results'})
    if results_ul:
        results_ul.append(li)
    else:
        print('Error: Could not find ul element with class "results" in HTML document')

    # Write updated HTML to file
    with open(base_path, 'w') as f:
        f.write(str(soup))

def clean_pokemon():
    with open("templates/index.html", "r") as f:
        contents = f.read()
    soup = BeautifulSoup(contents, "html.parser")
    li_tags = soup.find_all("li")
    for li in li_tags:
        li.decompose()
    with open("templates/index.html", "w") as f:
        f.write(str(soup))

def replace_pokemon(base_path):
    with open(base_path, "r") as f:
        contents = f.read()
    soup = BeautifulSoup(contents, "html.parser")
    li_tags = soup.find_all("li")
    count = 0
    for li in li_tags:
        li.decompose()
        count += 1
    with open(base_path, "w") as f:
        f.write(str(soup))
    for times in range(count):
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1118')
        data = response.json()
        pokemon_names = [pokemon['name'] for pokemon in data['results']]
        pokemon_name = random.choice(pokemon_names)
        add_pokemon_to_base_html(base_path, pokemon_name)
