from flask import Flask, render_template, request, redirect
import requests
import random
import new

app = Flask(__name__)
app.use_static_for_assets = True

base_url = "https://pokeapi.co/api/v2/pokemon/"
new.clean_pokemon()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        search_term = request.form['query']
        
        api_url = base_url + search_term.lower()

        response = requests.get(api_url)
        data = response.json()

        if 'detail' in data:
            error = data['detail']
            return render_template('results.html', error=error)
        pokemon_name = data['name'].capitalize()
        static_sprite_url = data['sprites']['front_default']
        animated_sprite_url = data['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
        abilities = [ability['ability']['name'].capitalize() for ability in data['abilities']]
        return render_template('results.html', pokemon_name=pokemon_name, static_sprite_url=static_sprite_url, animated_sprite_url=animated_sprite_url, abilities=abilities)
    
    else:
        return "Wrong HTTP method", 400




@app.route('/add_pokemon')
def add_pokemon():
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1118')
    data = response.json()
    pokemon_names = [pokemon['name'] for pokemon in data['results']]
    pokemon_name = random.choice(pokemon_names)
    new.add_pokemon_to_base_html('templates/index.html', pokemon_name)
    return redirect("/")

@app.route('/clean_pokemon')
def remove_pokemon():
    new.clean_pokemon()
    return redirect("/")

@app.route('/reload_pokemon')
def refresh_pokemon():
    new.replace_pokemon('templates/index.html')
    return redirect("/")