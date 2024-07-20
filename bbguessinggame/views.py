import datetime

from django.http import JsonResponse

from bbguessinggame.models import *

from django.shortcuts import render

from math import log2

botOfTheDay = None

WEAPON_TYPE_SIMILARITY = {
    "AH": ["AA","GH","CH"],
    "AS": ["AA", "AH", "MS"],
    "LL": ["GL"],
    "GG": ["GH","GL","CC","CH"],
    "GH": ["GG","CC","CH","AH"],
    "GL": ["GG","LL"],
    "CC": ["GH","GG","CH"],
    "CH": ["GH","GG","CC","AH"],
    "MS": ["MN","MD","AS"]
}

def setBotOfTheDay():
    global botOfTheDay
    global today
    botOfTheDay = BattleBot.objects.all().order_by("?")[0]
    today = datetime.date.today()


def indexView(request):
    return render(request, "bbGuessGame/game.html")


def match(request):
    global botOfTheDay
    global today
    guess = BattleBot.objects.get(id=request.GET["id"])

    if botOfTheDay is None or today != datetime.date.today():
        setBotOfTheDay()
    print(botOfTheDay)

    if guess.primaryColour == botOfTheDay.primaryColour or guess.primaryColour == botOfTheDay.secondaryColour:
        if guess.secondaryColour == botOfTheDay.primaryColour or guess.secondaryColour == botOfTheDay.secondaryColour:
            colour = "match"
        else:
            colour = "close"
    else:
        if guess.secondaryColour == botOfTheDay.primaryColour or guess.secondaryColour == botOfTheDay.secondaryColour:
            colour = "close"
        else:
            colour = "fail"

    if guess.debut == botOfTheDay.debut:
        debut = "match"
    elif abs(guess.debut - botOfTheDay.debut) == 1:
        debut = "close"
    else:
        debut = "fail"

    if guess.weapon_type == botOfTheDay.weapon_type:
        weapon = "match"
    elif guess.weapon_type in WEAPON_TYPE_SIMILARITY.keys():
        if botOfTheDay.weapon_type in WEAPON_TYPE_SIMILARITY[guess.weapon_type]:
            weapon = "close"
        else:
            weapon = "fail"
    elif guess.weapon_type[0] == botOfTheDay.weapon_type[0]:
            weapon = "close"
    else:
        weapon = "fail"

    if guess.best_finish == botOfTheDay.best_finish:
        finish = "match"
    elif abs(log2(guess.best_finish) - log2(botOfTheDay.best_finish)) == 1:
        finish = "close"
    else:
        finish = "fail"

    response = {
        "victory": guess == botOfTheDay,
        "letter": "match" if guess.name[0] == botOfTheDay.name[0] else "fail",
        "debut": debut,
        "weapon": weapon,
        "finish": finish,
        "country": "match" if guess.country == botOfTheDay.country else "fail",
        "colour": colour,
    }
    return JsonResponse(response, status=200)


def getByName(request):
    name = request.GET.get("name")
    '''name = name.replace("-", " ")
    name = name.replace("#", " ")
    name = name.replace(":", "")
    name = name.replace("'", "")
    name = name.replace("?", "")'''
    #Ragnarök
    #RotatoЯ
    #Jäger
    name = name.lower()
    name = name.replace("jag","Jäg")
    name = name.replace("ock j", "ock-j")
    name = name.replace("er the", "er: the")
    name = name.replace(" o ", " o' ")
    name = name.replace("disko i", "disk o' i")
    name = name.replace("rotator", "RotatoЯ")
    name = name.replace("ragnarok","Ragnarök")
    robots = BattleBot.objects.filter(name__icontains=name).order_by("name")
    i = 0
    response = {"robots": []}
    if name == "":
        return JsonResponse(response, status=200)
    for r in robots:
        response["robots"].append({"id": r.id, "name": r.name, "image": r.image.url})
        i += 1
        if i == 3:
            break
    return JsonResponse(response, status=200)
