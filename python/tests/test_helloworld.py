from typing import List, Dict
from kasumi import Kasumi,KasumiConfigration,DefaultSearchStrategy
from examples.helloworld.helloworld import PopipaSpider,popipa_search_desc

def test_helloworld():
    # token = input("Please input your token: ")
    app = Kasumi(
        KasumiConfigration(app_id=0, token='HCZl5Rnq4UJO60z4WM4EDqKMMs2Fk5Br1yXdHe93ghs6A9ZDQfVbt4vhSECUvXg8', search_key="",search_desc=popipa_search_desc, search_strategy=DefaultSearchStrategy)
    )
    app.add_spider(PopipaSpider())
    app.run_forever()