CREATE TABLE player (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    class VARCHAR(100) NOT NULL,
    level INT DEFAULT 1,
    xp INT DEFAULT 0
);

CREATE TABLE skill (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    level INT DEFAULT 1
);

CREATE TABLE quest (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    xp INT NOT NULL,
    summary TEXT
);

CREATE TABLE quest_skill (
    quest_id INT,
    skill_id INT,
    PRIMARY KEY (quest_id, skill_id),
    FOREIGN KEY (quest_id) REFERENCES quest(id),
    FOREIGN KEY (skill_id) REFERENCES skill(id)
);

CREATE TABLE player_skill (
    player_id INT,
    skill_id INT,
    PRIMARY KEY (player_id, skill_id),
    FOREIGN KEY (player_id) REFERENCES player(id),
    FOREIGN KEY (skill_id) REFERENCES skill(id)
);
