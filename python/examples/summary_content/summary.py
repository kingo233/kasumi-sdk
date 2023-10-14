from kasumi import *

prompt = '''
你是一个PPT制作助手，你精通如何总结通过长文本制作PPT，现在总结下面的Markdown文档为PPT，以1000字左右的篇幅。
写出你的总结内容，列出关键内容，并且该总结将被用来做成PPT，因此你需要提取所有的表格、公式相关的信息，并将每一页PPT的内容展示出来。
最终需要的内容为：标题、导航、每个章节的内容、每个小节的内容、原文包含的公式和表格，并将表格和公式保存在每个对应小节中。

下面是需要制作为PPT的内容。
'''

class KasumiServer(Kasumi):
    def before_chat(self, event: AbstractKasumiBeforeChatEvent):
        origin = event.get_origin_content()
        if len(origin) > 114514:
            content = self._utils.llm_summary('funny mad pee', '')
        else:
            content = self._utils.llm_summary(origin, prompt)
        event.transfer_to(content)
        event.interrupt()
