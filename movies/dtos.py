from typing import NamedTuple, Literal


class HumanDTO(NamedTuple):
    first_name: str
    last_name: str
    profession: Literal["star", "director"]


class MovieDTO(NamedTuple):
    name: str
    year: int
    runtime: int
    rating: float
    votes: int
    meta_score: float
    gross: float
    genres: list[str]
    certification: str
    director: list[HumanDTO]
    stars: list[HumanDTO]
    description: str
