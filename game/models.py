from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    room_id = models.SlugField(primary_key=True, editable=False, unique=True)
    game = models.CharField(max_length=5, default=None, null=True)
    round_no = models.PositiveIntegerField(default=1)
    current_player = models.PositiveIntegerField(null=True)
    changes = models.PositiveIntegerField(default=0)

    def players(self):
        return list(Player.objects.filter(room=self).order_by("index"))

    def pile(self):
        return list(
            Card.objects.filter(room=self)
            .exclude(played_index=None)
            .order_by("played_index")
        )


class Player(models.Model):
    index = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=40, default=None, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    current_bet = models.PositiveIntegerField(default=None, null=True)
    tricks_won = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)

    AVATARS = [
        f"images/avatars/{name}.jpg"
        for name in [
            "anna",
            "elsa",
            "fire_spirit",
            "hans",
            "kristoff",
            "olaf",
            "sven",
            "troll",
            "yelana",
            "young_anna",
        ]
    ]

    def hand(self):
        cards = list(Card.objects.filter(owned_by=self, played_index=None))
        return sorted(cards)


class Card(models.Model):
    suit = models.IntegerField(default=None, null=True)
    rank = models.IntegerField(default=None, null=True)
    owned_by = models.ForeignKey(Player, on_delete=models.CASCADE)
    played_index = models.PositiveIntegerField(default=None, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    SUITS = ["diamonds", "clubs", "hearts", "spades"]
    RANKS = ["7", "8", "9", "jack", "queen", "king", "10", "ace"]

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def higher_than(self, other):
        if self.suit == other.suit:
            return self.rank > other.rank

        return self.suit == 3

    def __lt__(self, other):
        if self.suit == other.suit:
            return self.rank < other.rank

        return self.suit < other.suit

    def __str__(self):
        return self.SUITS[self.suit]

    def image(self):
        return f"images/cards/{self.RANKS[self.rank]}_of_{self.SUITS[self.suit]}.png"
