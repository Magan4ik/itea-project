from typing import Literal

import pandas as pd

from movies.dtos import MovieDTO, HumanDTO
from movies.interfaces import MovieReaderInterface


class MovieCSVReader(MovieReaderInterface):
    def __init__(self, csv_name: str):
        self.df = pd.read_csv(csv_name)

    def get_movie_dto_list(self) -> list[MovieDTO]:
        self._fill_nan_values()
        movie_list = list()
        for index in range(len(self.df)):
            movie_list.append(self._parse_csv_to_dto_by_index(index=index))

        return movie_list

    def _fill_nan_values(self):
        self.df["Certification"].fillna("Not Rated", inplace=True)
        self.df["MetaScore"].fillna(-1., inplace=True)
        self.df["Gross"].fillna(-1., inplace=True)

    def _parse_csv_to_dto_by_index(self, index: int):
        return MovieDTO(
            name=self.df["Movie Name"][index],
            year=self.df["Year of Release"][index],
            runtime=self.df["Run Time in minutes"][index],
            rating=self.df["Movie Rating"][index],
            votes=self.df["Votes"][index],
            meta_score=self.df["MetaScore"][index],
            gross=self.df["Gross"][index],
            genres=self._convert_str_list_to_python_list("Genre", index=index),
            certification=self.df["Certification"][index],
            director=self._get_human_dto_list(prof="Director", index=index),
            stars=self._get_human_dto_list(prof="Stars", index=index),
            description=self._get_description(index=index)
        )

    def _convert_str_list_to_python_list(self, column: str, index: int) -> list[str]:
        col: str = self.df[column][index]
        col = col.replace("['", "")
        col = col.replace("']", "")
        if "," in col:
            col_list = col.split("', '")
        else:
            col_list = [col]

        for i in range(len(col_list)):
            col_list[i] = col_list[i].strip()
        return col_list

    def _get_human_dto_list(self, prof: Literal["Stars", "Director"], index: int) -> list[HumanDTO]:
        human_list = self._convert_str_list_to_python_list(prof, index=index)
        dto_list = list()
        for h in human_list:
            name = h.split(" ")
            first_name = name[0]
            if len(name) == 1:
                last_name = ""
            else:
                last_name = name[1]

            if prof == "Stars":
                profession: Literal["star"] = "star"
            else:
                profession: Literal["director"] = "director"
            dto = HumanDTO(
                first_name=first_name,
                last_name=last_name,
                profession=profession
            )
            dto_list.append(dto)

        return dto_list

    def _get_description(self, index: int):
        word_list = self._convert_str_list_to_python_list(column="Description", index=index)
        return ' '.join(word_list)

