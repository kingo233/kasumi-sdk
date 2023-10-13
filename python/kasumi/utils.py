from .abstract import *
import threading
from requests import post

class KasumiUtils:
    _app: AbstractKasumi = None

    def __init__(self, app: AbstractKasumi) -> None:
        self._app = app

    def llm_summary(self, content: str, prompt: str) -> str:
        '''
            summary content by llm, raise KasumiException if failed
            @param content: content to summary
            @param count: how long the summary should be
        '''

        url = self._app._config.get_kasumi_url()
        ident = threading.get_ident()
        try:
            if ident in self._app._sessions:
                session = self._app._sessions[threading.get_ident()]
                response = post(f"{url}/v1/sdk/llm_summary", data={
                    "app_id": self._app._config.get_app_id(),
                    "key": self._app._config.get_search_key(),
                    "token": session._user_token,
                    "token_type": TokenType.ENCRYPTION.value,
                    "content": content,
                    "prompt": prompt
                })
            else:
                raise KasumiException("User not logged in.")
            if response.status_code == 200:
                return response.json()["data"]["summary"]
            else:
                raise KasumiException(f"Failed to summary content by llm due to {response.text}")
        except Exception as e:
            raise KasumiException(f"Failed to summary content by llm due to {e}")