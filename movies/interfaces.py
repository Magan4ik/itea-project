from abc import ABCMeta, abstractmethod
from typing import Literal, Optional

from movies.dtos import MovieDTO, HumanDTO

class HumanRepositoryInterface(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_human_by_full_name(cls, full_name: str, prof: Literal["star", "director"]) -> Optional[HumanDTO]:
        pass

    @classmethod
    @abstractmethod
    def create_human(cls, human_dto: HumanDTO) -> HumanDTO:
        pass

    @classmethod
    @abstractmethod
    def delete_all_humans(cls):
        pass

class GenreRepositoryInterface(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_genre_by_name(cls, name: str) -> Optional[str]:
        pass

    @classmethod
    @abstractmethod
    def create_genre(cls, genre: str) -> str:
        pass

    @classmethod
    @abstractmethod
    def delete_all_genres(cls):
        pass

class MovieRepositoryInterface(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_movie_by_name(cls, name: str) -> Optional[MovieDTO]:
        pass

    @classmethod
    @abstractmethod
    def movie_exist(cls, movie_dto: MovieDTO) -> bool:
        pass

    @classmethod
    @abstractmethod
    def create_movie(cls, movie_dto: MovieDTO):
        pass

    @classmethod
    @abstractmethod
    def add_star(cls, star: HumanDTO, movie_name: str):
        pass

    @classmethod
    @abstractmethod
    def add_director(cls, director: HumanDTO, movie_name: str):
        pass

    @classmethod
    @abstractmethod
    def add_genre(cls, genre_name: str, movie_name: str):
        pass

    @classmethod
    @abstractmethod
    def delete_all_movies(cls):
        pass

class MovieReaderInterface(metaclass=ABCMeta):

    @abstractmethod
    def get_movie_dto_list(self) -> list[MovieDTO]:
        pass
