
import pytest
import kicktippbb

def test_tippabgabeurl_wo_matchday():
    actualUrl = kicktippbb.get_tippabgabe_url('mycomm')
    assert actualUrl == 'http://www.kicktipp.de/mycomm/tippabgabe'

def test_tippabgabeurl_with_matchday():
    actualUrl = kicktippbb.get_tippabgabe_url('mycomm', 5)
    assert actualUrl == 'http://www.kicktipp.de/mycomm/tippabgabe?&spieltagIndex=5'

def test_tippabgabeurl_matchday_oob():
    with pytest.raises(IndexError):
        kicktippbb.get_tippabgabe_url('mycomm', 42)
    with pytest.raises(IndexError):
        kicktippbb.get_tippabgabe_url('mycomm', 0)
    