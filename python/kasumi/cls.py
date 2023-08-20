from __future__ import annotations

'''
    This file contains the class for the Kasumi SDK.
    It is used to interact with the Kasumi API.
'''
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Iterator
from .base_cls import TokenType
from .abstract import *
from .embedding import KasumiEmbedding

import threading

class KasumiConfigration(AbstractKasumiConfigration):
    _token: str = ""
    _search_key: str = ""
    _kasumi_url: str = ""
    _app_id: int = 0

    def __init__(self, app_id: int, token: str, search_key: str, kasumi_url: str = "http://kasumi.miduoduo.org:8192"):
        self._app_id = app_id
        self._token = token
        self._search_key = search_key
        self._kasumi_url = kasumi_url

    def get_app_id(self) -> int:
        return self._app_id

    def get_token(self) -> str:
        return self._token
    
    def get_search_key(self) -> str:
        return self._search_key
    
    def get_kasumi_url(self) -> str:
        return self._kasumi_url

class KasumiSearchResultField(AbstractKasumiSearchResultField):
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

class KasumiSearchResult(AbstractKasumiSearchResult):
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

class KasumiSpider(AbstractKasumiSpider):
    pass

class KasumiSearchStrategy(AbstractKasumiSearchStrategy):
    def search(self, app: 'Kasumi', column: str, value: str) -> Iterator[KasumiSearchResult]:
        spiders = sorted(app.get_spiders(), key=lambda spider: spider.priority, reverse=True)
        for spider in spiders:
            results = spider.search(column, value)
            if len(results) > 0:
                return results
        return []

class KasumiSearchResponse(AbstractKasumiSearchResponse):
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

class KasumiInfoResponse(AbstractKasumiInfoResponse):
    _code: int = 0
    _message: str = ""
    _data: Dict[str, Any]

    def __init__(self, code: int, message: str, data: Dict[str, Any]):
        self._code = code
        self._message = message
        self._data = data

    def get_code(self) -> int:
        return self._code

    def get_message(self) -> str:
        return self._message

    def get_data(self) -> Dict[str, Any]:
        return self._data

class KasumiSession(AbstractKasumiSession):
    _user_token: str = ""

class Kasumi(AbstractKasumi):
    """
    This class is used to interact with the Kasumi API.

    :param config: The configuration of the Kasumi SDK.
    
    :raises all methods in Kasumi may raise KasumiException if the Kasumi API returns an error.
    """
    _config: KasumiConfigration = None
    _search_strategy: List[KasumiSearchStrategy] = []
    _spiders: List[KasumiSpider] = []
    _sessions: Dict[int, KasumiSession] = {}
    _embedding: AbstractKasumiEmbedding = KasumiEmbedding()

    def __init__(self, config: KasumiConfigration):
        self._config = config

    def embeding_text(self, text: str) -> List[float]:
        ident = threading.get_ident()
        try:
            if ident in self._sessions:
                session = self._sessions[threading.get_ident()]
                embedding = self._embedding.embedding_text(self, text, TokenType.ENCRYPTION, session._user_token)
            else:
                embedding = self._embedding.embedding_text(self, text, TokenType.PLAINTEXT, self._config.get_token())
            return embedding
        except Exception as e:
            raise KasumiException("Failed to get embedding of text. for more information, please see the traceback. %s" % e)
        
    def search_embedding_similarity(self, embedding: List[float], limit: int = 10) -> List[AbstractKasumiEmbeddingItem]:
        ident = threading.get_ident()
        try:
            if ident in self._sessions:
                session = self._sessions[threading.get_ident()]
                similarities = self._embedding.search_similarity(self, embedding, TokenType.ENCRYPTION, session._user_token, limit=limit)
            else:
                similarities = self._embedding.search_similarity(self, embedding, TokenType.PLAINTEXT, self._config.get_token(), limit=limit)
            return similarities
        except Exception as e:
            raise KasumiException("Failed to search embedding similarity. for more information, please see the traceback. %s" % e)

    def get_embedding_by_id(self, id: str) -> AbstractKasumiEmbeddingItem:
        ident = threading.get_ident()
        try:
            if ident in self._sessions:
                session = self._sessions[threading.get_ident()]
                embedding = self._embedding.get_embedding_by_id(self, id, TokenType.ENCRYPTION, session._user_token)
            else:
                embedding = self._embedding.get_embedding_by_id(self, id, TokenType.PLAINTEXT, self._config.get_token())
            return embedding
        except Exception as e:
            raise KasumiException("Failed to get embedding by id. for more information, please see the traceback. %s" % e)

    def insert_embedding(self, embedding: List[float], id: str) -> bool:
        try:
            return self._embedding.insert_embedding(self, embedding, id)
        except Exception as e:
            raise KasumiException("Failed to insert embedding. for more information, please see the traceback. %s" % e)

    def add_search_strategy(self, strategy: KasumiSearchStrategy) -> None:
        self._search_strategy.append(strategy)

    def add_spider(self, spider: KasumiSpider) -> None:
        self._spiders.append(spider)

    def get_search_strategies(self) -> List[KasumiSearchStrategy]:
        return self._search_strategy

    def get_spiders(self) -> List[KasumiSpider]:
        return self._spiders

    def _handle_request_info(self, request: Dict[str, Any]) -> KasumiInfoResponse:
        if request.get('remote_search_key') != self._config.get_search_key():
            return KasumiInfoResponse(
                code=401, message="Unauthorized", data={}
            )

        return KasumiInfoResponse(
            code=200, message="OK", data={
                "search_strategies": [{
                    'name': strategy.name,
                    'description': strategy.description,
                } for strategy in self._search_strategy],
            }
        )

    def _handle_request_search(self, request: Dict[str, Any]) -> KasumiSearchResponse:
        if request.get('remote_search_key') != self._config.get_search_key():
            return KasumiSearchResponse(
                code=401, message="Unauthorized", data=[]
            )

        ident = threading.get_ident()
        self._sessions[ident] = KasumiSession()

        strategy = request.get("strategy")
        column = request.get("column")
        value = request.get("value")

        if strategy is None or column is None or value is None:
            return KasumiSearchResponse(
                code=400, message="Bad Request", data=[]
            )
        
        if not isinstance(strategy, str) or not isinstance(column, str) or not isinstance(value, str):
            return KasumiSearchResponse(
                code=400, message="Bad Request", data=[]
            )

        for search_strategy in self._search_strategy:
            if search_strategy.name == strategy:
                results = search_strategy.search(self, column, value)

        if ident in self._sessions:
            del self._sessions[ident]

        return KasumiSearchResponse(
            code=200, message="OK", data=results
        )

    def run_forever(self) -> None:
        pass