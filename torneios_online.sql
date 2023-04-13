CREATE DATABASE chess;

USE chess;

CREATE TABLE player (
	player_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    elo_blitz INT NOT NULL default 1000,
    elo_rapid INT NOT NULL default 1000,
    elo_bullet INT NOT NULL default 1000,
    elo_classical INT NOT NULL default 1000,
	PRIMARY KEY (player_id),
    UNIQUE (username)
);

CREATE TABLE elo (
	elo_id INT NOT NULL AUTO_INCREMENT,
    player_id INT NOT NULL,
    type_of_time_control VARCHAR(20),
	rating INT NOT NULL,
    update_date DATE,
    PRIMARY KEY (elo_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);

CREATE TABLE tournament (
	tournament_id INT NOT NULL AUTO_INCREMENT,
    event_name VARCHAR(50) NOT NULL,
    event_date DATETIME NOT NULL,
    time_control VARCHAR(10) NOT NULL,
    type_of_time_control VARCHAR(10) NOT NULL,
    UNIQUE (tournament_id),
    PRIMARY KEY (event_name)
);

CREATE TABLE player_tournament (
	player_id INT NOT NULL,
    tournament_id INT NOT NULL,
    PRIMARY KEY (player_id, tournament_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id)
);

CREATE TABLE round (
	round_id INT NOT NULL AUTO_INCREMENT,
    tournament_id INT NOT NULL,
    round_number INT NOT NULL,
    PRIMARY KEY (round_id),
    UNIQUE (tournament_id, round_number),
    FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id)
);

CREATE TABLE game (
	game_id INT NOT NULL AUTO_INCREMENT,
    round_id INT NOT NULL,
	white_player_id INT NOT NULL,
    black_player_id INT NOT NULL,
    tournament_id INT NOT NULL,
    result VARCHAR(10) NOT NULL,
    game_link VARCHAR(128) NOT NULL,
    UNIQUE (game_id),
    PRIMARY KEY (game_link),
    FOREIGN KEY (round_id) REFERENCES round(round_id),
    FOREIGN KEY (white_player_id) REFERENCES player(player_id),
    FOREIGN KEY (black_player_id) REFERENCES player(player_id),
    FOREIGN KEY (tournament_id) REFERENCES tournament(tournament_id)
);

CREATE TABLE player_round (
	player_id INT NOT NULL,
    round_id INT NOT NULL,
    score DECIMAL(5,1) NOT NULL DEFAULT 0,
    PRIMARY KEY (player_id, round_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (round_id) REFERENCES round(round_id)
);

SELECT * FROM tournament;
SELECT * FROM elo;
SELECT * FROM player;
SELECT * FROM round;
SELECT * FROM player_round;
SELECT * FROM player_tournament;
SELECT * FROM game;

SELECT * FROM elo WHERE type_of_time_control = "Blitz" ORDER BY rating DESC;

SELECT result FROM game WHERE white_player_id = 14 and tournament_id = 2;

SELECT * FROM game G, round R, player_round PR WHERE PR.player_id = 14 and PR.round_id = R.round_id and G.round_id = R.round_id and G.tournament_id = 2 and G.white_player_id = 14;

SELECT black_player_id FROM game where white_player_id = 1 and tournament_id = 1
UNION
SELECT white_player_id FROM game where black_player_id = 1 and tournament_id = 1;

SELECT rating FROM elo where player_id = 14 and type_of_time_control = "Blitz" ORDER BY update_date DESC LIMIT 1;

INSERT INTO elo (player_id, type_of_time_control, rating, update_date) VALUES (14, "Blitz", 1024, "2023-02-02");

SELECT * FROM player P, elo E where E.type_of_time_control = "Blitz" ORDER BY rating DESC;

SELECT player_id, username, elo_blitz FROM player ORDER BY elo_blitz DESC;

-- SELECT * FROM player P, game G WHERE G.white_player_id = P.player_id or G.black_player_id = P.player_id and P.player_id = G.white_player_id and P.player_id = G.black_player_id ORDER BY P.elo_blitz DESC;

DROP DATABASE chess;