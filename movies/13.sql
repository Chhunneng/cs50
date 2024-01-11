SELECT DISTINCT people.name FROM people
JOIN stars AS s1 ON people.id = s1.person_id
JOIN movies ON s1.movie_id = movies.id
WHERE movies.id IN (
    SELECT movie_id FROM stars
    JOIN people ON stars.person_id = people.id
    WHERE people.name = 'Kevin Bacon' AND people.birth = 1958
)
AND people.name != 'Kevin Bacon';
