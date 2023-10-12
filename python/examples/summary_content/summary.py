from kasumi import *

class KasumiServer(Kasumi):
    def before_chat(self, event: AbstractKasumiBeforeChatEvent):
        origin = event.get_origin_content()
        if len(origin) > 114514:
            content = self._utils.llm_summary('funny mad pee', 114)
        else:
            content = origin
        event.transfer_to(content)
        event.interrupt()
