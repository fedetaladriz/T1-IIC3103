from django.http import HttpResponse
from django.shortcuts import render
import requests

# Create your views here.

def home_view(request):

    response = dict()
    response["better_call_saul"] = requests.get("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Better+Call+Saul").json()
    response["breaking_bad"] = requests.get("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Breaking+Bad").json()
    
    seasons = dict()

    for serie, episodes in response.items():
        

        serie_seasons = set()
        for episode in episodes:
            serie_seasons.add(episode["season"])
        
        seasons[serie] = sorted(list(serie_seasons))


    return render(request, "home.html", seasons)


def season_view(request, serie, season):

    if serie == "breaking_bad":
        episodes = requests.get("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Breaking+Bad").json()
        serie = "Breaking Bad"

    elif serie == "better_call_saul":
        episodes = requests.get("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Better+Call+Saul").json()
        serie = "Better Call Saul"
    else: 
        raise ValueError("Serie not found")

    season_episodes = []
    for episode in episodes:
        if int(episode["season"]) == int(season):
            season_episodes.append({k:episode[k] for k in ["episode", "title", "episode_id"]})


    context = {
        "serie": serie,
        "season": season,
        "episodes": season_episodes
    }


    return render(request, "season.html", context)


def episode_view(request, episode_id):

    episode = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/episodes/{episode_id}").json()[0]

    # characters = []
    
    # for character in episode["characters"]:
    #     full_character = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/characters?name={character.replace(' ', '+')}").json()[0]
    #     characters.append({k:full_character[k] for k in ["char_id", "name"]})
    
    # episode["characters"] = characters

    print(episode)
    return render(request, "episode.html", episode)


def character_view(request, character_name):

    character = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/characters?name={character_name.replace(' ', '+')}").json()[0]
    quotes = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/quote?author={character_name.replace(' ', '+')}").json()

    context = {
        "character": character,
        "quotes": quotes,
    }

    return render(request, "character.html", context)
    


def search_view(request):

    s = request.GET.get('s', '').strip()
    results = list()

    if s:

        formated_s = s.replace(' ', '+')


        result = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/characters?name={formated_s}").json()
        results.extend(result)

        i = 10

        while len(result) == 10:
            result = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/characters?name={formated_s}&limit={i}&offset=10").json()
            
            results.extend(result)
            i += 10


    context = {
        "s": s,
        "result": results
    }

    return render(request, "search.html", context)
    

    
    



# def character_search_result(request, search):
