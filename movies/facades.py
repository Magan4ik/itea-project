from typing import Type

from django.db import transaction

from movies.dtos import MovieDTO
from movies.interfaces import (HumanRepositoryInterface,
                               GenreRepositoryInterface,
                               MovieRepositoryInterface,
                               MovieReaderInterface
                               )

import init_django_orm
from movies.parser_csv import MovieCSVReader
from movies.repositories import HumanDjangoORMRepository, GenreDjangoORMRepository, MovieDjangoORMRepository

from tqdm import tqdm


class MovieFacade:
    def __init__(self, human_repository: Type[HumanRepositoryInterface],
                 genre_repository: Type[GenreRepositoryInterface],
                 movie_repository: Type[MovieRepositoryInterface],
                 movie_parser: MovieReaderInterface):
        self._human_repository = human_repository
        self._genre_repository = genre_repository
        self._movie_repository = movie_repository
        self._movie_parser = movie_parser

    @transaction.atomic
    def import_movies(self, index: int = None):
        movie_dto_list = self._movie_parser.get_movie_dto_list()
        if not index:
            for movie_dto in tqdm(movie_dto_list):
                self._import_movie_from_dto(movie_dto=movie_dto)
        else:
            self._import_movie_from_dto(movie_dto=movie_dto_list[index])

    def _import_movie_from_dto(self, movie_dto: MovieDTO):
        if self._movie_repository.movie_exist(movie_dto=movie_dto):
            return
        self._movie_repository.create_movie(movie_dto=movie_dto)

        for star in movie_dto.stars:
            star_dto = self._human_repository.get_human_by_full_name(
                full_name=f"{star.first_name} {star.last_name}", prof="star"
            )
            if not star_dto:
                star_dto = self._human_repository.create_human(human_dto=star)
            self._movie_repository.add_star(star=star_dto, movie_name=movie_dto.name)

        for director in movie_dto.director:
            director_dto = self._human_repository.get_human_by_full_name(
                full_name=f"{director.first_name} {director.last_name}", prof="director"
            )
            if not director_dto:
                director_dto = self._human_repository.create_human(human_dto=director)
            self._movie_repository.add_director(director=director_dto, movie_name=movie_dto.name)

        for genre in movie_dto.genres:
            genre_name = self._genre_repository.get_genre_by_name(name=genre)
            if not genre_name:
                genre_name = self._genre_repository.create_genre(genre=genre)
            self._movie_repository.add_genre(genre_name=genre_name, movie_name=movie_dto.name)

    @transaction.atomic
    def clear_movies(self):
        self._movie_repository.delete_all_movies()
        self._human_repository.delete_all_humans()
        self._genre_repository.delete_all_genres()


if __name__ == '__main__':
    movie_facade = MovieFacade(
        human_repository=HumanDjangoORMRepository,
        genre_repository=GenreDjangoORMRepository,
        movie_repository=MovieDjangoORMRepository,
        movie_parser=MovieCSVReader(csv_name="movies.csv")
    )
    movie_facade.import_movies()
