from __future__ import annotations

# This file contains the functions used to insert and retrieve embeddings from the Kasumi database.
from typing import List, Union

from requests import post, get

from kasumi.abstract import AbstractKasumi, AbstractKasumiEmbeddingItem
from kasumi.base_cls import TokenType
from .base_cls import TokenType
from .abstract import *

class KasumiEmbeddingItem(AbstractKasumiEmbeddingItem):
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

class KasumiEmbedding(AbstractKasumiEmbedding):
    def __init__(self) -> None:
        pass

    def embedding_text(self, app: AbstractKasumi, text: str, token_type: TokenType, token: str):
        url = app._config.get_kasumi_url()
        response = post(f"{url}/v1/embedding", data={
            "text": text,
            "token_type": token_type.value,
            "token": token
        })
        if response.status_code != 200:
            raise KasumiException("Failed to embed text.")
        
        return response.json()['data']['embedding']

    def get_embedding_by_id(self, app: AbstractKasumi, id: str, token_type: TokenType, token: str) -> KasumiEmbeddingItem:
        pass

    def insert_embedding(self, app: AbstractKasumi, embedding: List[float], id: str) -> bool:
        pass

    def search_similarity(self, app: AbstractKasumi, embedding: List[float], token_type: TokenType, token: str, limit: int = 10) -> List[KasumiEmbeddingItem]:
        pass
