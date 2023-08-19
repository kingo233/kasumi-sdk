from __future__ import annotations

# This file contains the functions used to insert and retrieve embeddings from the Kasumi database.
from typing import List, Union
from .base_cls import TokenType


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

def insert_embedding(app_id: int, remote_search_key: str, embedding: List[float], id: str) -> bool:
    """
    This function is used to insert an embedding into the Kasumi database.

    will not cost any KaToken but has a limit of 1000 times per day.

    :param app_id: The id of the app.
    :param remote_search_key: The remote search key of the app, can be set in miduoduo developer platform.
    :param embedding: The embedding to insert.
    :return: True if the embedding was inserted successfully, False otherwise.
    """
    pass

def embedding_text(text: str, token_type: TokenType, token: str):
    """
    This function is used to get the embedding of a text.

    cause it's necessary to cost tokens to embedding text in Kasumi, so you should pass the token_type and token to this function.
    token_type declare the type of the token, to security reason, if the caller is user not developer, Kasumi will send an encrypted token to the caller, finally pass it here.
    but if developer call this function, you can pass TokenType.PLAINTEXT and token to this function.

    :param text: The text to get the embedding of.
    :param token_type: The type of the token. Can be TokenType.PLAINTEXT or TokenType.ENCRYPTION.
    :return: The embedding of the text.
    """

def search_similarity(app_id: int, remote_search_key: str, embedding: List[float], token_type: TokenType, token: str, limit: int = 10) -> List[KasumiEmbeddingItem]:
    """
    This function is used to search for embeddings that are similar to a given embedding.

    search similarity will cause at least 1 KaToken, so you should pass the token_type and token to this function.

    :param app_id: The id of the app.
    :param remote_search_key: The remote search key of the app, can be set in miduoduo developer platform.
    :param embedding: The embedding to search for.
    :param limit: The maximum number of embeddings to return.
    :return: A list of EmbeddingSimilarity objects.
    """
    pass

def get_embedding_by_id(app_id: int, remote_search_key: str, id: str, token_type: TokenType, token: str) -> KasumiEmbeddingItem:
    """
    This function is used to get the embedding of an item by its id.

    get embedding by id will cause at least 1 KaToken, so you should pass the token_type and token to this function.

    :param app_id: The id of the app.
    :param remote_search_key: The remote search key of the app, can be set in miduoduo developer platform.
    :param id: The id of the item.
    :return: The embedding of the item.
    """
    pass