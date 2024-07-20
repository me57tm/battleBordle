import pycountry
from django.db import models

COUNTRY_CHOICES = []
for c in pycountry.countries:
    COUNTRY_CHOICES.append((c.alpha_2, c.name))
COUNTRY_CHOICES.sort(key=lambda x: x[1])

BEST_FINISH_CHOICES = [
    (1, "Champion"),
    (2, "Runner Up"),
    (4, "Semi-Finalist"),
    (8, "Quarter-Finalist"),
    (16, "Round of 16"),
    (32, "Round of 32"),
    (64, "Qualifiers"),
    (128, "Alternate")
]

WEAPON_TYPE_CHOICES = [
    ("NM", "Meltybrain"),

    ("HH", "Horizontal Spinner"),
    ("HU", "Undercutter"),
    ("HO", "Overhead Spinner"),
    ("HS", "Shell Spinner"),
    ("HR", "Ring Spinner"),

    ("VV", "Vertical Spinner"),
    ("VD", "Drum Spinner"),
    ("VE", "Eggbeater"),

    ("SP", "Propeller Spinner"),
    ("SN", "Angled Spinner"),
    ("SR", "Articulated Spinner"),

    ("AA", "Axe"),
    ("AH", "Horizontal Axe"),
    ("AS", "Hammersaw"),

    ("ES", "Spear"),
    ("EC", "Cannon"),

    ("LL", "Lifter"),
    ("GG", "Grabber"),
    ("GH", "Horizontal Grabber"),
    ("GL", "Grabber-Lifter"),
    ("CC", "Crusher"),
    ("CH", "Horizontal Crusher"),

    ("FR", "Flipper"),
    ("FF", "Front-Hinged Flipper"),
    ("FS", "Side-Hinged Flipper"),

    # M Misc - now actually abrasive things
    ("MS", "Saw"),
    ("MN", "Chainsaw"),
    ("MD", "Drill"),

    ("IM", "Interchangeable / Multibot"),

]


class BattleBot(models.Model):
    name = models.CharField(blank=False, max_length=255)
    image = models.ImageField(upload_to='images', blank=True)
    debut = models.PositiveSmallIntegerField(blank=False)
    weapon_type = country = models.CharField(max_length=2, choices=WEAPON_TYPE_CHOICES, blank=False)
    best_finish = models.PositiveSmallIntegerField(choices=BEST_FINISH_CHOICES, blank=False)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=False, default="US")
    primaryColour = models.CharField(blank=False, max_length=20)
    secondaryColour = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.name
