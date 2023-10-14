from typing import Dict, List
from kasumi import *
from kasumi.abstract import AbstractKasumiActionResult
from .generate import create_ppt
from .config import KEY

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

class Action(AbstractKasumiAction):
    @property
    def name(self) -> str:
        return 'generate_ppt'
    
    @property
    def priority(self) -> int:
        return 10
    
    @property
    def description(self) -> str:
        return 'create a ppt from a reveal.js markdown format content, '
    
    @property
    def param_template(self) -> Dict[str, str]:
        return {'markdown_text': 'reveal.js format markdown text'}
    
    def action(self, search_param: Dict) -> List[AbstractKasumiActionResult]:
        markdown = search_param['markdown_text']
        result = []
        try:
            ppt_content = create_ppt(markdown)
            url = self.app.upload_file(ppt_content, 'ppt.pptx', 'application/pptx')
            file = KasumiActionResult.get_file_dict(
                content_type='application/pptx',
                filename='ppt.pptx',
                url=url,
                filesize=len(ppt_content),
                key='ppt',
            )
            result.append(KasumiActionResult.load_from_dict({
                'result': 'ppt has been created and sent to user',
            }, disabled_show_columns=['result'], files=[file]))
        except Exception as e:
            print('failed to create ppt: ' + str(e))
            result.append(KasumiActionResult.load_from_dict({
                'result': 'failed to create ppt',
            }, disabled_show_columns=['result']))

        return result

def ppt():
    app = KasumiServer(KasumiConfigration(
        kasumi_url="http://127.0.0.1:8192",
        app_id=66,
        search_key=KEY,
        token=''
    ))
    app.add_action(Action())

    app.run_forever(3433)