SELECT title, rating FROM movies
WHERE year = 2010 AND rating IS NOT NULL
ORDER BY rating DESC, title;
