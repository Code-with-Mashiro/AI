from 真白 import MashiroCore
mashiro = MashiroCore("dummy_rules.json")

def test_Calculation_skill():
    response = mashiro.respond("10+5は？")
    assert "15" in response]
def test_date_skill():
    response = mashiro.respond("今日は何曜日？")
    assert"日" in response