# Kasumi Project SDK
[README](README.md) | [中文文档](README_zh.md)
## 介绍
Kasumi Project SDK 是一个用于开发 Kasumi Project 应用的工具集。你可以使用它来构建 Kasumi 应用，如果你还不了解Kasumi是什么，更多关于 Kasumi Project 的信息请参考 [Miduoduo](http://developer.miduoduo.org)。

使用这个 SDK，你可以开发一个 Kasumi 应用来实现以下功能：
* 为你的 LLM 应用提供特定的数据源，以提供数据给 LLM
* 控制 LLM 应用的流程，以实现特定的业务逻辑

为了尽可能的降低开发成本，我们提供了一个非常简单易用的 SDK 来帮助你开发 Kasumi 应用。希望您能快速上手 Kasumi并开发出优秀的 Kasumi 应用。

在这个 SDK 中，我们提供了以下语言的 SDK：
* Python SDK
* Go SDK

但截止目前，我们只提供Python语言的SDK，Go语言的SDK将在后续版本中提供。

## 开源协议
Kasumi Project SDK 是一个开源项目，使用 GPL v3.0 协议。你可以免费使用它，但是你必须遵循 GPL v3.0 协议。更多信息请参考 [GPL v3.0](./LICENSE)

## 目录
- [Kasumi Project SDK](#kasumi-project-sdk)
  - [介绍](#介绍)
  - [开源协议](#开源协议)
  - [目录](#目录)
  - [Python SDK](#python-sdk)
    - [安装](#安装)
    - [示例](#示例)
      - [Hello World 迷你APP](#hello-world-迷你app)
      - [How to use our managed embedding database service](#how-to-use-our-managed-embedding-database-service)
    - [API Reference](#api-reference)

## Python SDK

### 安装
你可以使用 pip 来安装 Kasumi Project SDK，使用以下命令即可：
```bash
pip install kasumi-python
```
### 示例
#### Hello World 迷你APP
在这个例子中，你将学习如何使用 Kasumi Project SDK 来开发一个 Hello World 迷你APP。

这个 Hello World APP 是一个非常简单的迷你APP，它将使用一个字典作为它的迷你数据库。

如果你只是开发一个不需要私有数据的迷你APP，而且这个迷你APP也不需要作为一个AI agent来控制你的电脑。
那么你甚至不需要这个SDK来开发你的迷你APP。你只需要使用迷你APP的system prompt，然后将Search Service Address和Search service key留空即可。

所以这个SDK只是为了那些想要开发一个带有私有数据或者AI agent的迷你APP的人。

在这个例子中，我们将使用popipa的成员信息作为我们的私有数据。所以我们需要定义一个Spider：

```python
from kasumi import AbstractKasumiSpider, KasumiSearchResult
from typing import List, Dict
class PopipaSpider(AbstractKasumiSpider):
    @property
    def name(self) -> str:
        return "popipa"
    
    @property
    def priority(self) -> int:
        return 1

    def search(self, search_param : Dict) -> List[KasumiSearchResult]:
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
        text = mini_database.get(name,'not found,please check your parameter')
        result = KasumiSearchResult.load_from_dict({
            'result':text,
        })
        return [result]
```

你可以看到我们定义了一个PopipaSpider，你需要定义name，priority和search function。你不应该改变参数列表。priority属性将影响默认的搜索顺序。更多信息请参考AbstractSearchStrategy类和DefaultSearchSrategy类。Search function将返回一个KasumiSearchResult列表。KasumiSearchResult是一个类，它将用于将搜索结果返回给Kasumi Project。你可以看到我们在这个函数中定义了一个迷你数据库。这个数据库是一个字典，我们将使用name参数来搜索这个数据库。如果name在数据库中，我们将返回结果，否则我们将返回一个not found消息。

对于真实的应用，你可以使用这个函数来搜索你的数据库或者搜索引擎。你也可以使用这个函数来搜索你的本地文件系统。

我们还定义了一个search desc：
```python
popipa_search_desc = "search popipa members information by name,accept one of [Arisa,Rimi,Saya,Kasumi,Tae] as parameter."\
                     "example:{'name':'Arisa'}"
```

这个search desc将用于描述你的search function。我们将使用它来告诉LLM如何使用你的search function如何使用。所以你必须尽你最大的努力来描述你的search function和它的参数。这个search desc是你的app的所有spider的search function的全局描述。

接下来我们需要定义一个Kasumi Application：
```python
from typing import List, Dict
from kasumi import Kasumi,KasumiConfigration,DefaultSearchStrategy
from examples.helloworld.helloworld import PopipaSpider,popipa_search_desc

def test_helloworld():
    app = Kasumi(
        KasumiConfigration(app_id=0, token=0, search_key="123",search_desc=popipa_search_desc, search_strategy=DefaultSearchStrategy)
    )
    app.add_spider(PopipaSpider(app))
    app.run_forever()
```

这里，我们定义了一个Kasumi Application，并且我们将我们的PopipaSpider添加到这个application中。然后我们永远运行这个application。

Kasumi Application 需要一个KasumiConfigration来初始化。KasumiConfigration需要一个app_id, token, search_key, search_desc和search_strategy。app_id用于标识你的app，这与你的embedding database有关，不同的app id有不同的embedding 数据库表。

token用于当你需要插入embedding 向量到我们管理的embedding数据库时。你只需要为LLM embedding消耗的token付费。请在这里填写你自己的app token。如果你不想使用我们管理的embedding数据库服务(插入,搜索,删除),请将它设置为0或任意值。search_key用于标识你的search function，请在miduoduo平台上使用相同的key。search_desc用于描述你的search function。search_strategy用于定义搜索策略。你可以使用DefaultSearchStrategy来使用默认的搜索顺序和数据处理。你也可以定义你自己的搜索策略。

在app.run_forever()函数之后，你的app将永远运行flask。你可以使用这个app来为你的LLM Application提供服务。你也可以更改监听端口。默认端口是3433。

#### How to use our managed embedding database service
在这个例子中，你将学习如何使用我们管理的embedding数据库服务。

例如，你有一些文档，你想将它们插入到我们管理的embedding数据库服务中。然后你可以使用我们管理的embedding数据库服务来搜索相似的文档。

首先，我写了一个```update.py```文件来将embedding向量插入到我们管理的embedding数据库服务中：

```python
from typing import List, Dict
from kasumi import Kasumi,KasumiConfigration,DefaultSearchStrategy
from utils.chunk import len_safe_get_embedding
import json

search_desc = "NO SEARCH NEEDED"

idx = 0

if __name__ == '__main__':
    token = input("Please input your(develper's) token: ")
    app = Kasumi(
        KasumiConfigration(app_id=3, token=token, search_key="123",search_desc=search_desc, search_strategy=DefaultSearchStrategy)
    )
    
    data_path = '${MY_DATA_PATH}}'
    with open(data_path, 'r') as f:
        text = f.read()
    
    # chunk embedding
    def get_embedding_callback(text):
        global idx
        print(f'embedding id = {idx}')
        idx += 1
        return app.embeding_text(text)
    
    embeddings, chunked_texts = len_safe_get_embedding(text, get_embedding_callback)

    i = 0
    chunked_text_path = '${MY_CHUNKED_TEXT_PATH}'
    
    chunked_text_dict = {}
    for chunked_text in chunked_texts:
        chunked_text_dict[str(i)] = chunked_text
        i += 1
    chunked_text_json = json.dumps(chunked_text_dict)
    with open(chunked_text_path,'w') as f:
        f.write(chunked_text_json)
    
    
    for i in range(len(embeddings)):
        embedding_id = str(i)
        embedding = embeddings[i]
        app.insert_embedding(embedding,embedding_id)
        print('insert embedding id: ', embedding_id)
```

and ```utils.chunk``` as follows:
```python
from itertools import islice
from typing import Iterable,Iterator,List,Callable, Tuple
import tiktoken
import numpy as np

def batched(iterable :Iterable, n :int) -> Iterator:
    """Batch data into tuples of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it : Iterator = iter(iterable)
    while (batch := tuple(islice(it, n))):
        yield batch

def chunked_tokens(text :str, chunk_length :int, encoding_name :str = 'cl100k_base'):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    chunks_iterator = batched(tokens, chunk_length)
    yield from chunks_iterator


def len_safe_get_embedding(text,get_embedding_callback: Callable, max_tokens=1024) -> Tuple[List[List[float]],List[str]]:
    chunk_embeddings = []
    chunk_texts = []
    for chunk in chunked_tokens(text, chunk_length=max_tokens):
        # using tiktoken to decode tokens to text
        chunk = tiktoken.get_encoding('cl100k_base').decode(chunk)
        chunk_embeddings.append(get_embedding_callback(chunk))
        chunk_texts.append(chunk)

    return chunk_embeddings,chunk_texts
```

这里，我们将search_desc定义为“NO SEARCH NEEDED”，因为这个脚本只是用来将embedding向量插入到我们管理的embedding数据库服务中。我们不需要LLM来搜索任何东西。

然后我们定义了一个token变量，这个变量用于标识你的app。你可以从miduoduo平台上获取你的token。


接着我们定义了一个Kasumi Application。并且使用app来获取embedding和插入embedding。注意：你应该自己管理embedding向量和对应的文本来处理LLM的搜索请求。这里我们使用本地文件系统作为例子，你可以使用文档数据库如mongodb来管理你的embedding向量和对应的文本。

所以你的spider可能看起来像这样：
```python
    def __init__(self, app : Kasumi) -> None:
        super().__init__(app)
        chunked_text_path = '${MY_CHUNKED_TEXT_PATH}'
        with open(chunked_text_path,'r') as f:
            chunked_text_json = f.read()
        self.chunked_text_dict = json.loads(chunked_text_json)


    def search(self, search_param : Dict) -> List[KasumiSearchResult]:
        keyword = search_param.get("keyword",'')
        if len(keyword) == 0:
            return []
        
        embedding = self.app.embeding_text(keyword)
        embedding_results = self.app.search_embedding_similarity(embedding, 1)
        embedding_result = embedding_results[0]
        embedding_id = embedding_result.id
        chunked_text = self.chunked_text_dict[embedding_id]
        text = chunked_text

        result = KasumiSearchResult.load_from_dict({
            'result':text,
        })
        return [result]
```

### API Reference
可能会在未来更新。