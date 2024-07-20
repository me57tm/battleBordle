from django.conf import settings
from django.http import JsonResponse

from bbguessinggame.models import *

from django.shortcuts import render

from django.utils import timezone

from math import log2

WEAPON_TYPE_SIMILARITY = {
    "AH": ["AA", "GH", "CH"],
    "AS": ["AA", "AH", "MS"],
    "LL": ["GL"],
    "GG": ["GH", "GL", "CC", "CH"],
    "GH": ["GG", "CC", "CH", "AH"],
    "GL": ["GG", "LL"],
    "CC": ["GH", "GG", "CH"],
    "CH": ["GH", "GG", "CC", "AH"],
    "MS": ["MN", "MD", "AS"]
}


def setBotOfTheDay():
    global botOfTheDay
    global today
    botOfTheDay = BattleBot.objects.all().order_by("?")[0]
    today = timezone.now().day
    savedBotFile = open(settings.MEDIA_URL[1:] + "hiddenBotOfTheDay.txt", "w")
    savedBotFile.write(str(botOfTheDay.id))
    savedBotFile.close()


today = timezone.now().day
savedBotFile = open(settings.MEDIA_URL[1:] + "hiddenBotOfTheDay.txt", "r")
savedBot = savedBotFile.readline()
savedBotFile.close()
try:
    botOfTheDay = BattleBot.objects.get(pk=int(savedBot))
except (ValueError, BattleBot.DoesNotExist):
    setBotOfTheDay()


def indexView(request):
    guessed = request.COOKIES["guessed"].split(",")
    colourGrid = [[None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6]
    bbNames = []
    for i in range(len(guessed)):
        matchResults = match(guessed[i])
        bbNames.append(BattleBot.objects.get(id=guessed[i]).name)
        j = 0
        for x in ["letter", "debut", "weapon", "finish", "colour", "country"]:
            colourGrid[i][j] = "green" if matchResults[x] == "match" else "yellow" if matchResults[
                                                                                          x] == "close" else "red"
            j += 1

    return render(request, "bbGuessGame/game.html", {"colourGrid": colourGrid, "bbNames": bbNames})


def match(pk):
    global botOfTheDay
    global today
    guess = BattleBot.objects.get(id=pk)

    if today != timezone.now().day:
        setBotOfTheDay()

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
    return response


def matchView(request):
    return JsonResponse(match(request.GET["id"]), status=200)


def getByNameView(request):
    name = request.GET.get("name")
    '''name = name.replace("-", " ")
    name = name.replace("#", " ")
    name = name.replace(":", "")
    name = name.replace("'", "")
    name = name.replace("?", "")'''
    # Ragnarök
    # RotatoЯ
    # Jäger
    name = name.lower()
    name = name.replace("jag", "Jäg")
    name = name.replace("ock j", "ock-j")
    name = name.replace("er the", "er: the")
    name = name.replace(" o ", " o' ")
    name = name.replace("disko i", "disk o' i")
    name = name.replace("rotator", "RotatoЯ")
    name = name.replace("ragnarok", "Ragnarök")
    name = name.replace("war e", "war? e")
    name = name.replace("? ez", "? ez!")
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
