SELECT AVG(rating) FROM movies
Join ratings ON ratings.movie_id = movies.id
WHERE year = 2012;