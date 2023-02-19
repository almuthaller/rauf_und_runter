from random import shuffle
from django.shortcuts import render
from game.models import *
from game.forms import *


def deal(room):
    deck = []
    for i in range(4):
        for j in range(8):
            deck.append((i, j))
            deck.append((i, j))
    shuffle(deck)

    for _ in range(room.round_no):
        for player in room.players():
            suit, rank = deck.pop()
            card = Card(suit=suit, rank=rank, owned_by=player, room=room)
            card.save()

    if room.game == "rauf":
        room.current_player = room.players()[room.round_no % 4 - 1].id
        room.save()
    elif room.game == "runter":
        room.current_player = room.players()[-(room.round_no % 4)].id
        room.save()


def next_player(room):
    for p in room.players():
        if p.id == room.current_player:
            player_index = room.players().index(p)
            break

    if player_index == 3:
        room.current_player = room.players()[0].id
    else:
        room.current_player = room.players()[player_index + 1].id
    room.save()


def place_bet(request, room, player):
    form = PlaceBet(request.POST)
    if form.is_valid():
        current_bet = form.cleaned_data["bet"]
        sum_so_far = sum(
            p.current_bet for p in room.players() if p.current_bet is not None
        )

        if (
            room.round_no > 4
            and all(p.current_bet is not None for p in room.players() if p != player)
            and sum_so_far + current_bet == room.round_no
        ):
            return f"Ha, you think it's going to be that easy? Say something other than {room.round_no - sum_so_far}."

        player.current_bet = current_bet
        player.save()
        next_player(room)

        if all(p.current_bet is not None for p in room.players()):
            play_card(request, room, player)

        room.changes += 1
        room.save()


def _determine_trick_winner(room):
    pile = room.pile()
    highest = pile[0]
    for card in pile[1:]:
        if card.higher_than(highest):
            highest = card

    return highest.owned_by


def play_card(request, room, player):
    form = PlayCard(request.POST)
    if form.is_valid():
        chosen_card = player.hand()[form.cleaned_data["card"]]

        pile = room.pile()
        if len(pile) > 0:
            trick_suit = pile[0].suit
            if chosen_card.suit != trick_suit and any(
                c.suit == trick_suit for c in player.hand()
            ):
                return f"Na-a-a, no cheating! I know you can play {room.pile()[0]}!"

        chosen_card.played_index = len(pile)
        chosen_card.save()

        if len(room.pile()) < 4:
            next_player(room)
        else:
            room.current_player = _determine_trick_winner(room).id
            room.save()

        room.changes += 1
        room.save()


def clean_pile(room, player):
    trick_winner = _determine_trick_winner(room)
    trick_winner.tricks_won += 1
    trick_winner.save()
    Card.objects.exclude(played_index=None).delete()

    if len(player.hand()) == 0:
        end_round(room)

    room.changes += 1
    room.save()


def end_round(room):
    for player in room.players():
        if player.current_bet == player.tricks_won:
            player.score += 5 + player.current_bet
            player.save()
        else:
            player.score -= abs(player.current_bet - player.tricks_won) * 2
            player.save()

        player.current_bet = None
        player.tricks_won = 0
        player.save()

    if room.game == "rauf":
        room.round_no += 1
        room.save()
        if room.round_no <= 16:
            deal(room)

    elif room.game == "runter":
        room.round_no -= 1
        room.save()
        if room.round_no >= 1:
            deal(room)


def render_game(request, room, player, warning):
    pile = room.pile()

    show_bet_input = player.id == room.current_player and player.current_bet is None
    show_card_input = (
        player.id == room.current_player
        and player.current_bet is not None
        and len(pile) < 4
    )
    show_clean_table = len(pile) == 4 and player.id == room.current_player

    players = room.players()

    tricks_total = sum(p.current_bet for p in players if p.current_bet is not None)
    show_tricks_won = all(p.current_bet is not None for p in players)
    trick_winner = (
        _determine_trick_winner(room).user.username if len(pile) == 4 else None
    )

    players_positioned = players[:]
    while players_positioned.index(player) != 3:
        x = players_positioned.pop(0)
        players_positioned.append(x)

    player_stats = [
        (
            p.user.username,
            "active" if p.id == room.current_player else "waiting",
            p.tricks_won,
            p.current_bet,
            p.avatar,
        )
        for p in players_positioned
    ]

    scores = [(p.user.username, p.score) for p in players]
    hand = [card.image() for card in player.hand()]
    pile = [(card.image(), card.owned_by.user.username) for card in pile]

    context = {
        "title": room.game.capitalize(),
        "round": room.round_no,
        "tricks_total": tricks_total,
        "place_bet_form": PlaceBet,
        "play_card_form": PlayCard,
        "show_bet_input": show_bet_input,
        "show_card_input": show_card_input,
        "show_tricks_won": show_tricks_won,
        "show_clean_table": show_clean_table,
        "trick_winner": trick_winner,
        "players": player_stats,
        "scores": scores,
        "hand": hand,
        "pile": pile,
        "warning": warning,
        "changes_url": "changes?room_id=" + room.room_id,
        "initial_count": str(room.changes),
    }

    return render(request, "playing.html", context)
