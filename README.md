# chess-web-scrapping

Lichess.org is an online chess website that anyone can use for free. There is a section in this website "Community" -> "Teams" that allows players to create
a team and make tournaments for members of that team. 

This mini-project makes mainly 3 things:

- Get all tournaments links and write it on a txt file (each tournament has it own link). You can find it on populate/getAllTournaments.py 
- Collects data from tournaments (based on the links provided in a txt file) and store it on a database for further exploration
- Uses the elo system to rank players based on the tournaments provided only (so it has it's own elo ecosystem that doesn't depend on lichess elo system) and creates tables in html with that information
