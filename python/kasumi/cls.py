from __future__ import annotations

'''
    This file contains the class for the Kasumi SDK.
    It is used to interact with the Kasumi API.
'''
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Iterator

class KasumiException(Exception):
    """
    This class is used to represent an exception raised by the Kasumi SDK.
    """
    pass

class KasumiConfigration(object):
    _token: str = ""
    _search_key: str = ""
    _kasumi_url: str = ""

    def __init__(self, token: str, search_key: str, kasumi_url: str = "http://kasumi.miduoduo.org:8196"):
        self._token = token
        self._search_key = search_key
        self._kasumi_url = kasumi_url

    def get_token(self) -> str:
        return self._token
    
    def get_search_key(self) -> str:
        return self._search_key
    
    def get_kasumi_url(self) -> str:
        return self._kasumi_url

class KasumiSearchResultField(object):
    """
    KasumiSearchResultField is used to represent a field in the search result.
    _key: The key of the field.
    _content: The content of the field.
    _llm_disabled: this field will not be sent to the LLM if this is set to True.
    _show_disabled: this field will not be shown to the client if this is set to True.
    """

    _key: str = ""
    _content: str = ""
    _llm_disabled: bool = False
    _show_disabled: bool = False

    def __init__(self,key: str, content: str, llm_disabled: bool = False, show_disabled: bool = False):
        self._key = key
        self._content = content
        self._llm_disabled = llm_disabled
        self._show_disabled = show_disabled

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self._key,
            "content": self._content,
            "llm_disabled": self._llm_disabled
        }

class KasumiSearchResult(object):
    _fields: List[KasumiSearchResultField] = []

    def __init__(self, fields: List[KasumiSearchResultField]):
        self.fields = fields

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fields": [field.to_dict() for field in self._fields]
        }
    
    @staticmethod
    def load_from_dict(data: Dict[str, Any], disabled_llm_columns: List[str] = None, disabled_show_columns: List[str] = None) -> KasumiSearchResult:
        disabled_llm_columns = disabled_llm_columns or []
        disabled_show_columns = disabled_show_columns or []

        fields = []
        for key, value in data:
            fields.append(KasumiSearchResultField(
                key=key, content=value, llm_disabled=key in disabled_llm_columns, show_disabled=key in disabled_show_columns
            ))

        return KasumiSearchResult(fields)

class KasumiSpider(ABC):
    @abstractmethod
    @property
    def name(self) -> str:
        pass

    @abstractmethod
    @property
    def priority(self) -> int:
        pass

    @abstractmethod
    def search(self, column: str, value: str) -> Iterator[KasumiSearchResult]:
        pass

class KasumiSearchStrategy(ABC):
    @abstractmethod
    @property
    def name(self) -> str:
        pass

    @abstractmethod
    @property
    def description(self) -> str:
        pass

    @abstractmethod
    @property
    def possible_columns(self) -> List[str]:
        pass

    def search(self, app: 'Kasumi', column: str, value: str) -> Iterator[KasumiSearchResult]:
        spiders = sorted(app.get_spiders(), key=lambda spider: spider.priority, reverse=True)
        for spider in spiders:
            yield from spider.search(column, value)

class KasumiResponse(object):
    _code: int = 0
    _message: str = ""
    _data: List[KasumiSearchResult]

    def __init__(self, code: int, message: str, data: List[KasumiSearchResult]):
        self._code = code
        self._message = message
        self._data = data

    def get_code(self) -> int:
        return self._code

    def get_message(self) -> str:
        return self._message

    def get_data(self) -> List[KasumiSearchResult]:
        return self._data

class KasumiEmbeddingItem(object):
    """
    This class is used to represent an embedding item.
    You can use it to store the embedding and the id of the item.
    Remember that the id is the id of the item in the `Your` database.
    """
    embedding: List[float] = []
    similarity: float = 0.0
    id: str = ""

    def __init__(self, embedding: List[float], id: str):
        self.embedding = embedding
        self.id = id

    def set_similarity(self, similarity: float) -> None:
        self.similarity = similarity

    def get_similarity(self) -> float:
        return self.similarity

class Kasumi(object):
    """
    This class is used to interact with the Kasumi API.

    :param config: The configuration of the Kasumi SDK.
    
    :raises all methods in Kasumi may raise KasumiException if the Kasumi API returns an error.
    """
    _config: KasumiConfigration = None
    _search_strategy: List[KasumiSearchStrategy] = []
    _spiders: List[KasumiSpider] = []

    def __init__(self, config: KasumiConfigration):
        self._config = config

    def embeding_text(self, text: str) -> List[float]:
        pass

    def search_embedding_similarity(self, embedding: List[float]) -> List[KasumiEmbeddingItem]:
        pass

    def get_embedding_by_id(self, id: str) -> KasumiEmbeddingItem:
        pass

    def insert_embedding(self, embedding: List[float]) -> bool:
        pass

    def add_search_strategy(self, strategy: KasumiSearchStrategy) -> None:
        pass

    def add_spider(self, spider: KasumiSpider) -> None:
        pass

    def get_search_strategies(self) -> List[KasumiSearchStrategy]:
        pass

    def get_spiders(self) -> List[KasumiSpider]:
        pass

    def run_forever(self) -> None:
        pass