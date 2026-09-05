from abc import ABC, abstractmethod
from typing import Literal
from .data.dto.genre_dto import GenreDTO
from .data.dto.movie_dto import MovieDTO
from .data.dto.add_movie_dto import AddMovieDTO

class Service(ABC):
  
  
  """
  존재하는 모든 영화리스트 (list[MovieDTO])를 반환합니다.
  """
  # 영화 전체 탐색
  @abstractmethod
  def get_all_movies(self) -> list[MovieDTO]:
    pass

  """
  문자열을 넣으면 그 문자열을 포함하는 영화리스트 (list[MovieDTO])를 반환합니다.
  """
  # 영화 제목 탐색
  @abstractmethod
  def search_movie_by_title(self, keyword: str) -> list[MovieDTO]:
    pass

  """
  AddMovieDTO를 넣으면 해당 영화가 생성됩니다. (available된 상태로)
  """
  # 영화 추가
  @abstractmethod
  def add_movie(self, movie: AddMovieDTO) -> MovieDTO:
    pass

  """
  삭제할 영화의 pk(자연수)를 입력하면 삭제(논리적 삭제)된 영화객체 (MovieDTO)를 반환합니다.
  """
  # 영화 삭제
  @abstractmethod
  def delete_movie(self, pk: int) -> MovieDTO:
    pass

  """
  모든 장르의 정보를 반환합니다.
  """
  # 장르 전체 출력
  @abstractmethod
  def get_all_genres(self) -> list[GenreDTO]:
    pass

  """
  활성화 되어있는 모든 장르의 pk 반환합니다.
  """
  # 장르 전체 출력
  @abstractmethod
  def get_all_genres(self) -> list[int]:
    pass

  """
  장르의 pk과 설정 여부 (available 또는 unavailable)를 인자로 넣어 변경된 장르 객체 (GenreDTO)를 반환합니다. 
  """
  # 장르 활성화 여부 변경
  @abstractmethod
  def change_genre_status(self, pk: int, status: Literal["available", "unavailable"]) -> GenreDTO:
    pass