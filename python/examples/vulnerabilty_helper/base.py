from mongoengine import Document
from abc import ABC, abstractmethod
from typing import Dict, List, Callable,Tuple, Any

class BaseDocumentModel(Document):
    meta = {
        'abstract': True,
        'strict': False
    }

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return data
    
    @classmethod
    def load_motor(cls, document: dict):
        return cls(**document)
    
    def embedding_text(self) -> str:
        '''
            return embedding text
        '''
        pass
