#!/bin/bash
curl -X DELETE "localhost:9200/film_db"

# The index mapping will be automatically created on insertion. 
curl -X POST "localhost:9200/film_db/film" -H 'Content-Type: application/json' -d '
{
  "title": "The Matrix",
  "directors": [
    "Lana Wachowski",
    "Lilly Wachowski"
  ],
  "release": "1999-03-31",
  "day": "31",
  "month": "03",
  "year": "1999",
  "genres": [
    "Action",
    "Sci-Fi"
  ],
  "keywords": "simulated reality,artificial reality,w\nar with machines,computer hacker,post apocalypse",
  "description": "The Matr\nix is a movie starring Keanu Reeves, Laurence Fishburne, and Carrie-Anne Mo\nss. A computer hacker learns from mysterious rebels about the true nature o\nf his reality and his role in the war against its controllers.",
  "actors": [
    "Keanu Reeves",
    "Laurence Fishburne",
    "Carrie-Anne Moss",
    "Hugo Weaving"
  ]
}
'
