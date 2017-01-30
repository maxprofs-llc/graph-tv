CREATE DATABASE IF NOT EXISTS seinfeld;

USE seinfeld;

-- episodes

DROP TABLE IF EXISTS episodes;

CREATE TABLE episodes (
    overall_no  int,
    season_no   int,
    episode_no  int,
    title   text,
    directors text,
    writers text,
    air_date  date,
    production_code int,
    us_viewers  decimal(5,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOAD DATA LOCAL INFILE 'EpisodeMetadata.txt' 
INTO TABLE episodes 
FIELDS TERMINATED BY '|' 
OPTIONALLY ENCLOSED BY '\"' 
IGNORE 1 LINES;

-- characters

DROP TABLE IF EXISTS characters;

CREATE TABLE characters (
    character_id    int,
    real_name   text,
    character_name  text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- scenes

DROP TABLE IF EXISTS scenes;

CREATE TABLE scenes (
    overall_no int,
    scene_id    int,
    scene_name  text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- scripts

DROP TABLE IF EXISTS scripts;

CREATE TABLE scripts (
    id int not null auto_increment,
    overall_no  int,
    file_no text,
    scene_id    int,
    scene_name  text,
    character_id    int,
    character_name text,
    scriptline   text,
    primary key (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOAD DATA LOCAL INFILE '/Users/ompatel/Dropbox/seinfeld/data/processed/script_lines.txt'
INTO TABLE scripts 
FIELDS TERMINATED BY '|' 
IGNORE 1 LINES 
(file_no, scene_name, character_name, scriptline);




select character_name, count(*), min(scriptline)
from scripts
group by character_name
order by count(*) desc;