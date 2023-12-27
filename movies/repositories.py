from typing import Optional, Literal

from movies.interfaces import HumanRepositoryInterface, GenreRepositoryInterface, MovieRepositoryInterface
from movies.models import Human, Genre, Movie
from movies.dtos import MovieDTO, HumanDTO


class HumanDjangoORMRepository(HumanRepositoryInterface):

    @classmethod
    def get_human_by_full_name(cls, full_name: str, prof: Literal["star", "director"]) -> Optional[HumanDTO]:
        first_name, last_name = full_name.split(" ")
        human = Human.objects.filter(first_name=first_name, last_name=last_name, profession=prof).first()
        if not human:
            return None
        return cls._map_model_to_dto(human=human)

    @classmethod
    def _map_model_to_dto(cls, human: Human):
        return HumanDTO(
            first_name=human.first_name,
            last_name=human.last_name,
            profession=human.profession
        )

    @classmethod
    def create_human(cls, human_dto: HumanDTO) -> HumanDTO:
        human = Human.objects.create(**human_dto._asdict())
        return cls._map_model_to_dto(human=human)

    @classmethod
    def delete_all_humans(cls):
        humans = Human.objects.all()
        for human in humans:
            human.delete()


class GenreDjangoORMRepository(GenreRepositoryInterface):

    @classmethod
    def get_genre_by_name(cls, name: str) -> Optional[str]:
        genre = Genre.objects.filter(genre=name).first()
        if not genre:
            return None
        return genre.genre

    @classmethod
    def create_genre(cls, genre: str) -> str:
        gen = Genre.objects.create(genre=genre)
        return gen.genre

    @classmethod
    def delete_all_genres(cls):
        genres = Genre.objects.all()
        for genre in genres:
            genre.delete()


class MovieDjangoORMRepository(MovieRepositoryInterface):

    @classmethod
    def get_movie_by_name(cls, name: str) -> Optional[MovieDTO]:
        movie = Movie.objects.filter(name=name).first()
        if not movie:
            return None
        return cls._map_model_to_dto(movie=movie)

    @classmethod
    def movie_exist(cls, movie_dto: MovieDTO) -> bool:
        movie_dict = movie_dto._asdict()
        movie_dict.pop("genres", None)
        movie_dict.pop("director", None)
        movie_dict.pop("stars", None)
        return Movie.objects.filter(**movie_dict).exists()

    @classmethod
    def _map_model_to_dto(cls, movie: Movie) -> MovieDTO:
        genre_list = list()
        for genre in movie.genres.all():
            genre_list.append(genre.genre)

        star_list = list()
        for star in movie.stars.all():
            human = HumanDTO(
                first_name=star.first_name,
                last_name=star.last_name,
                profession=star.profession
            )
            star_list.append(human)

        director_list = list()
        for director in movie.director.all():
            human = HumanDTO(
                first_name=director.first_name,
                last_name=director.last_name,
                profession=director.profession
            )
            director_list.append(human)

        return MovieDTO(
            name=movie.name,
            year=movie.year,
            runtime=movie.runtime,
            rating=movie.rating,
            votes=movie.votes,
            meta_score=movie.meta_score,
            gross=movie.gross,
            genres=genre_list,
            certification=movie.certification,
            director=director_list,
            stars=star_list,
            description=movie.description
        )

    @classmethod
    def create_movie(cls, movie_dto: MovieDTO):
        movie_dict = movie_dto._asdict()
        movie_dict.pop("genres", None)
        movie_dict.pop("director", None)
        movie_dict.pop("stars", None)
        Movie.objects.create(**movie_dict)

    @classmethod
    def add_star(cls, star: HumanDTO, movie_name: str):
        star = Human.objects.filter(**star._asdict()).first()
        movie = Movie.objects.filter(name=movie_name).first()
        if star not in movie.stars.all():
            movie.stars.add(star)

    @classmethod
    def add_director(cls, director: HumanDTO, movie_name: str):
        director = Human.objects.filter(**director._asdict()).first()
        movie = Movie.objects.filter(name=movie_name).first()
        if director not in movie.director.all():
            movie.director.add(director)

    @classmethod
    def add_genre(cls, genre_name: str, movie_name: str):
        genre = Genre.objects.filter(genre=genre_name).first()
        movie = Movie.objects.filter(name=movie_name).first()
        if genre not in movie.genres.all():
            movie.genres.add(genre)

    @classmethod
    def delete_all_movies(cls):
        movies = Movie.objects.all()
        for movie in movies:
            movie.delete()
