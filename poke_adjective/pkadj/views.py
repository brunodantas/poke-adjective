from concurrent.futures import ThreadPoolExecutor
from functools import cache
import os
import random
import string

import pokebase as pb
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader


@cache
def get_adjectives(letter):
    with open(os.path.join(settings.BASE_DIR, "english-adjectives.txt")) as f:
        return [adj for adj in f.readlines() if adj[0] == letter]


def poke_adj(request, letter):
    if not isinstance(letter, str) or len(letter) != 1 or not letter.isalpha():
        return redirect("poke_adj", letter=random.choice(string.ascii_lowercase))

    pokemon_list = [
        pkmn.pokemon_species
        for pkmn in pb.pokedex("national").pokemon_entries
        if pkmn.pokemon_species.name[0] == letter.lower()
    ]

    def get_artwork(pkmn):
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pkmn.id_}.png"

    pokemon_tuples = [
        (
            pkmn,
            get_artwork(pkmn),
            random.choice(get_adjectives(letter.lower())),
        )
        for pkmn in pokemon_list
    ]
    template = loader.get_template("index.html")
    context = {
        "pokemon_list": pokemon_tuples,
        "letters": string.ascii_uppercase,
    }
    return HttpResponse(template.render(context, request))


def index(request):
    return redirect("poke_adj", letter=random.choice(string.ascii_lowercase))
