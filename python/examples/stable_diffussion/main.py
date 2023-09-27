from typing import Dict, List
from .config import SEARCH_KEY
from .draw import draw_image_api
from kasumi import *

class KawaiiDrawAction(AbstractKasumiAction):
    @property
    def name(self) -> str:
        return 'draw'
    
    @property
    def priority(self) -> int:
        return 10
    
    @property
    def description(self) -> str:
        # 你需要尽可能描述清楚用户没有表达的特征，如几个人、是否为全身、光线分布、发色、瞳色、性别、体型、身高等多个特征。
        return 'draw image by text, prompt should be english and split by , or space. you should translate other language to english first. prompt must be more than 10 words.'
    
    @property
    def param_template(self) -> Dict[str, str]:
        return {"prompt": "girl, full-body, white stocking, inside, window, high light in hair, white hair, long hair, blue eyes, blush, smile, white background"}
    
    def action(self, search_param: Dict) -> List[KasumiActionResult]:
        prompt = search_param['prompt']
        result = []
        try:
            image_bytes = draw_image_api(prompt)
            url = self.app.upload_file(image_bytes, 'image.png', 'image/png')
            file = KasumiActionResult.get_file_dict(
                content_type='image/png',
                filename='kawaii.png',
                url=url,
                filesize=len(image_bytes),
                key='image',
            )
            result.append(KasumiActionResult.load_from_dict({
                'result': 'image has been drawed',
            }, disabled_show_columns=['result'], files=[file]))
        except Exception as e:
            print('failed to draw image: ' + str(e))
            result.append(KasumiActionResult.load_from_dict({
                'result': 'failed to draw image',
            }, disabled_show_columns=['result']))

        return result

if __name__ == "__main__":
    kasumi = Kasumi(
        KasumiConfigration(
            app_id=53,
            token='',
            search_key=SEARCH_KEY,
        )
    )
    kasumi.add_action(KawaiiDrawAction(app=kasumi))
    kasumi.run_forever(3433)