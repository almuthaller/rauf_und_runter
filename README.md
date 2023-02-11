# Rauf und Runter
This is my **final project** for the Python course I took at Beetroot Academy. I chose to make an online version of a card game I used to play with my family. For development I used Python and Django.

## Example game
![Screenshot](screenshot.png)

## This project's future
The next step for this project will be to make it actually asynchronous. At the moment I have a short time solution that works but is not ideal. I use a hidden view that returns a count of changes, meaning every time a player makes a move or something happens in the game, the counter will count up. This view is called once when rendering the game, and then additionally from inside my html template with a timer every second. I then compare the counter values to each other and if they are not equal, the page will be reloaded. Disadvantages with this concept are for one, there is a maximum delay of 1s for every player to be up to date, but most of all this logic causes a lot of traffic on my server since this view function is called every second times four players times currently active game rooms. Which is why the next step would be to replace this concept with websockets that will listen to event streams and update everyone’s pages in real time. For that, I would use Django Channels.

## How to run this project
To get this project running on your pc you will need to 
- generate your own Django secret key and store it as an environment variable called DJANGO_SECRET_KEY

- if you want to play with users from other networks:
  - find out your public IP adress and store it as an environment variable called PUBLIC_IP 
  - on you wifi router, set up port forwarding from your public IP to your local one
- otherwise:
  - change line 154 in views.py to point to your local IP instead 

- export your environment variables
- in your Terminal, type 'python3 manage.py runserver 0.0.0:8000'
- open 'http://127.0.0.1:8000' in your favorite browser

## How to play
Four players are needed for this game. Follow the instructions on the website to create accounts and create a game. You can choose between “rauf” or “runter” mode, I suggest you start with a “rauf” game. Once four players are connected to the room, your game will automatically start.

Rauf und Runter is a trick guessing game, which means in the beginning of each round you take turns placing bets on how many tricks you will win. From round 5 upwards the total sum of bidden tricks is not allowed to be equal to the number of hand cards (= round number), meaning the last player placing their bet will get a warning if they try to do so. 

Rauf und Runter is played with two 32-card Piquet decks with the following rank order: 7, 8, 9, J, Q, K, 10, A. Spades is always the trump suit. In the case of two identical cards the first one played will beat the second one. Players are required to follow suit. 

At the end of each round, the score table will be updated as follows: 
- Right bet: + 5 points + number of bidden tricks
- Wrong bet: - 2 points for each trick different from the placed bet
