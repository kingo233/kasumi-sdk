from typing import List, Dict

from kasumi import Kasumi,KasumiConfigration,DefaultActionStrategy, AbstractKasumiAction, KasumiActionResult, KasumiActionResultField

class PopipaSpider(AbstractKasumiAction):
    @property
    def name(self) -> str:
        return "popipa"
    
    @property
    def priority(self) -> int:
        return 1

    def action(self, search_param : Dict) -> List[KasumiActionResult]:
        name = search_param.get("name",'')
        if len(name) == 0:
            return []
        mini_database = {
            "Arisa": "Poppin'Party乐队的键盘手，就读花咲川女子学园。喜欢的食物有豆沙水果凉粉、玄米、白煮蛋，讨厌葱类的食物。以盆景和上网为兴趣的室内派"\
                        "虽然基本一直不出门，但很有方法所以在学校成绩优秀。非常毒舌，特别是总对Kasumi很强硬，但其实只是坦率不起来而已。在年幼时就学习过钢琴、不过半途而废了"\
                        "因为缺乏锻炼所以体力很差，拥有各式各样的坐姿以及狂放的睡姿",
            "Rimi": "Poppin'Party乐队的贝斯手，就读于花咲川女子学园。兴趣是游戏和读书，还有摄影的专长，平常会纪录乐团的日常。"\
                                "关西人，性格比较胆小怯懦，一紧张就容易说出方言，比较认生所以起初一直自己一人在屋顶吃午餐。"\
                                "是隔壁Hello, Happy World!的濑田薰的铁粉。弹奏贝斯方面，在台上演出时使用拨片弹奏，台下作曲时偶尔会指弹。",
            "Saya": "Poppin'Party乐队的鼓手。兴趣是卡拉OK、观看棒球赛、收集发饰。开学典礼就和香澄交好，经常和香澄一起吃饭。性格温柔，为朋友着想，是香澄的咨询对象。",

            "Kasumi": "Poppin 'Party乐队的主唱兼吉他手。喜欢冒险和唱卡拉OK。喜欢的食物是炸薯条、白米饭,讨厌纳豆。有着积极乐观的性格。做事冲动莽撞"\
                        "常有令人诧异的举动,例如当DD。发型本意是星星形状,但一眼看去总会被认为是猫耳",
            "Tae": "Poppin'Party乐队的主音吉他手，RAISE A SUILEN最佳第六人，就读花咲川女子学园。兴趣是跑步（不会勉强去跑）、黏土、泡澡。小学就开始学习吉他的实力派。"\
                    "非常喜欢音乐，升入高中后就一直在Live House打工.对从小攒钱买来的蓝色ESP SNAPPER吉他非常中意。性格我行我素而又天然。时不时会做出意料之外的行动让周围的人吃惊"\
                    "想法很直率，但是是一个十分冷静，很清楚知道为了别人该怎么做的孩子。家人是父亲母亲和20只兔子。",
        }
        text = mini_database.get(name,'not found')
        result = KasumiActionResult.load_from_dict({
            'result':text,
        })
        return [result]

popipa_search_desc = "search popipa members information by name,accept one of [Arisa,Rimi,Saya,Kasumi,Tae] as parameter."\
                     "example:{'name':'Arisa'}"
