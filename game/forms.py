from django import forms


class PlaceBet(forms.Form):
    bet = forms.IntegerField(label="bet")


class PlayCard(forms.Form):
    card = forms.IntegerField(label="card")
