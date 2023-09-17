# Kasumi Project SDK
[README](README.md) | [中文文档](README_zh.md)
## Introduction
Kasumi Project SDK is a set of tools for developing Kasumi Project applications. You can use it to build a Kasumi Application, Please refer to [Miduoduo](http://developer.miduoduo.org) for more information about Kasumi Project.

With this SDK, you can develop a Kasumi Application to achieve the following functions:
* Power your LLM Application with specific data source to provide data for LLM
* Control the flow of LLM Application to achieve specific logic

To mostly reduce the development cost, we provides a very simple and easy-to-use SDK for you to develop your Kasumi Application. Wish you have a good time with Kasumi Project.

In This SDK, we can find the following language SDK:
* Python SDK
* Go SDK

But utill now, we only provide Python SDK. We will provide Go SDK in the future.

## Open Source Agreement
Kasumi Project SDK is open source under the GPL v3.0 license. You can use it for free, but you must follow the GPL v3.0 license. For more information, please refer to [GPL v3.0](./LICENSE)

## Contents
- [Kasumi Project SDK](#kasumi-project-sdk)
  - [Introduction](#introduction)
  - [Open Source Agreement](#open-source-agreement)
  - [Contents](#contents)
  - [Python SDK](#python-sdk)
    - [Installation](#installation)
    - [Usage Example](#usage-example)
      - [Hello World Styled Mini APP](#hello-world-styled-mini-app)
      - [How to use our managed embedding database service](#how-to-use-our-managed-embedding-database-service)
    - [API Reference](#api-reference)
  
## Python SDK
### Installation
You can install Kasumi Project SDK with pip:
```bash
pip install kasumi-python
```
### Usage Example
#### Hello World Styled Mini APP
In this section, you will learn how to develop a Hello World Styled Mini APP with Kasumi Project SDK. 

The Hello World APP is a very simple Mini APP, it will use a dict as a mini databse.

If you are just developing an app without private data and this app don't need to be an  AI agent to control your computer.
Then you even don't need this sdk to develop your app. You can just the app's system prompt and leave Search Service Address and Search service key blank.

So this sdk is only for those who want to develop a Kasumi Application with private data or AI agent app.

For this example, we will use popipa's member information as our private data.So we need to define a Spider:
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
You can see that we have defined a PopipaSpider,you need to define the name,priority and search function.You should not change the parameter list. priority property will affect the default search order.For more information please check the AbstractSearchStrategy class and DefaultSearchSrategy class. Search function will return a KasumiSearchResult list. KasumiSearchResult is a class that will be used to return search result to Kasumi Project. You can see that we have defined a mini database in this function. This database is a dict, and we will use the name parameter to search the database. If the name is in the database, we will return the result, else we will return a not found message.

For real world application, you can use this function to search your database or search engine. You can also use this function to search your local file system.

We also defined a search desc:
```python
popipa_search_desc = "search popipa members information by name,accept one of [Arisa,Rimi,Saya,Kasumi,Tae] as parameter."\
                     "example:{'name':'Arisa'}"
```

This search desc will be used to describe your search function. We will use it to tell LLM how to use your search function.So you must try your best to describe your search function and it's parameter.This search desc is global for your app's all spider's search function.

Then we need to define a Kasumi Application:
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

Here, we have defined a Kasumi Application, and we have added our PopipaSpider to this application. Then we run this application forever.

Kasumi Application need a KasumiConfigration to init. KasumiConfigration need a app_id, token, search_key, search_desc and search_strategy. app_id is used to identify your app, this is related to your embedding database,varios app id have diffrent embedding database table.

token is used when you need to insert embedding vector into our managed embedding database.You just need pay for the LLM embedding token.Please fill in your own app token here.If you don't want to use our managed vector dabase service(insert,search,delete),just leave it zero. search_key is used to identify your search function,please use the same key in miduoduo platform. search_desc is used to describe your search function. search_strategy is used to define the search strategy. You can use DefaultSearchStrategy to use the default search order and data processing. You can also define your own search strategy.

After the app.run_forever() function, your app will start flask forever. You can use this app to power your LLM Application.You can also change the listen port. The default port is 3433.

#### How to use our managed embedding database service
In this section, you will learn how to use our managed embedding database service.

For example, you have some documents, and you want to insert them into our managed embedding database service. Then you can use our managed embedding database service to search similar documents.

First, I write a ```update.py``` file to insert embedding vector into our managed embedding database service:

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

Here, We defined search_desc as “NO SEARCH NEEDED” because this script is only for insert embedding vector into our managed embedding database service. We don't need LLM to search anything.

Then we defined a token variable, this variable is used to identify your app. You can get your token from miduoduo platform.

Then we defined a Kasumi Application.And use app to get embedding and insert embedding.NOTE:You should manage the embedding vector and corresponding text by yourself to deal with LLM's search quest.Here we use local file system as example,you can use document database like mongodb to manage your embedding vector and corresponding text.

So your spider may seem like this:
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
May update in the future.