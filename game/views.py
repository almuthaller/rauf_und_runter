from random import choice
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from game.forms import *
from game.helper_funcs import *
from game.models import *


def index(request):
    if request.user.is_authenticated:
        return redirect("/create_room")

    return render(request, "index.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("/create_room")

    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/create_room")
        return render(
            request,
            "register.html",
            {"form": form},
        )

    form = UserCreationForm()
    return render(
        request,
        "register.html",
        {"form": form},
    )


def signin(request):
    next_param = request.GET.get("next")

    if request.user.is_authenticated:
        return redirect("/create_room")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if next_param:
                return redirect(next_param)
            return redirect("/create_room")
        else:
            return render(
                request,
                "signin.html",
                {"form": form},
            )

    form = AuthenticationForm()
    return render(
        request,
        "signin.html",
        {"form": form},
    )


def signout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect("/")


@login_required
def create_room(request):
    return render(request, "create_room.html")


@login_required
def create_rauf(_):
    room = Room(room_id=get_random_string(12), game="rauf")
    room.save()

    return redirect("/game?room_id=" + room.room_id)


@login_required
def create_runter(_):
    room = Room(room_id=get_random_string(12), game="runter", round_no=16)
    room.save()

    return redirect("/game?room_id=" + room.room_id)


@login_required
def game(request):
    room_id = request.GET.get("room_id")
    room = Room.objects.get(room_id=room_id)

    warning = None

    try:
        player = Player.objects.get(room=room, user=request.user)
    except Player.DoesNotExist:
        if len(room.players()) == 4:
            return HttpResponse("This room is already full, sorry.")

        avatar = choice(Player.AVATARS)
        while avatar in [p.avatar for p in room.players()]:
            avatar = choice(Player.AVATARS)

        player = Player(
            room=room, user=request.user, index=len(room.players()), avatar=avatar
        )
        player.save()
        room.changes += 1
        room.save()

        if len(room.players()) == 4:
            deal(room)
            room.current_player = room.players()[0].id
            room.save()

        room.changes += 1
        room.save()

    if request.method == "POST":
        if "bet" in request.POST:
            warning = place_bet(request, room, player)

        elif "card" in request.POST:
            warning = play_card(request, room, player)

        else:
            clean_pile(room, player)

        if not warning:
            return redirect("/game?room_id=" + room_id)

    if len(room.players()) < 4:
        return render(
            request,
            "waiting.html",
            {
                "link": "http://94.255.201.217:28000/game?room_id=" + str(room.room_id),
                "no_of_players": len(room.players()),
                "players": room.players(),
                "changes_url": "changes?room_id=" + room.room_id,
                "initial_count": str(room.changes),
            },
        )

    if (
        any((room.game == "rauf", room.game is None))
        and room.round_no > 16
        or room.game == "runter"
        and room.round_no < 1
    ):
        max_score = max(p.score for p in room.players())
        winners = [p.user.username for p in room.players() if p.score == max_score]
        winner_str = " and ".join(winners)

        return render(
            request,
            "finished.html",
            {
                "winner": winner_str,
                "scores": [(p.user.username, p.score) for p in room.players()],
            },
        )

    return render_game(request, room, player, warning)


def changes(request):
    room_id = request.GET.get("room_id")
    room = Room.objects.get(room_id=room_id)

    return HttpResponse(room.changes)
