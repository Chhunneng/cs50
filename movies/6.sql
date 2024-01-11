SELECT AVG(rating) FROM movies WHERE year = 2012;

SELECT AVG(rating) FROM ratings JOIN movies ON ratings.movie_id = movies.id;
