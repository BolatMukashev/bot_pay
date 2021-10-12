from pydantic import BaseModel, ValidationError
from typing import List, Optional


class School(BaseModel):
    school_name: str
    country: str
    city: str
    phones: Optional[List[str]] = None
    emails: Optional[List[str]] = None
    instagram: Optional[str] = None


class SchoolsFile(BaseModel):
    __root__: List[School]


def parse_schools_from_json_file(filename: str) -> object:
    """
    Парсит локальный файл в объект
    :param filename: Название файла
    :return: объект со списоком автошкол
    """
    try:
        schools = SchoolsFile.parse_file(filename).__root__
    except ValidationError as e:
        print(e.json())
    else:
        return schools


def parse_schools_from_object(schools_from_docs: List[dict]) -> object:
    """
    Парсит присланный файл в объект
    :param schools_from_docs: список со школами
    :return: объект со списоком автошкол
    """
    try:
        new_schools = SchoolsFile.parse_obj(schools_from_docs).__root__
    except ValidationError as e:
        print(e.json())
    else:
        return new_schools
