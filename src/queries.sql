
select noLines, count(*) as noCharacters
from
(select character_name, count(*) as noLines
from scripts
group by character_name
order by count(*) desc) as a
group by noLines;

select file_no, scene_name, s.character_name, count(*) as noLines
from scripts as s
join (select character_name, count(*) as noLines
from scripts
where character_name <> 'action'
group by character_name
having noLines >= 100
) as c on s.character_name = c.character_name
where s.character_name <> 'action' and s.character_name in ('NEWMAN','STEINBRENNER')
group by file_no, scene_name, character_name;

select character_name, count(*) as noLines
from scripts
where character_name <> 'action'
group by character_name
having noLines > 10;

select character_name, min(file_no), max(file_no), count(*)
from scripts
group by character_name
order by character_name;

update scripts
set character_name = 'TARTABULL'
where character_name IN ('TARTBULL');