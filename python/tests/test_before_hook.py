from examples.summary_content.summary import *

def test_before_hook():
    app = KasumiServer(KasumiConfigration(
        app_id=0,
        search_key='',
        token=''
    ))

    app.run_forever(3433)