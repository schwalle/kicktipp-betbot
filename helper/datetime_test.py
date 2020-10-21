import pytest
from helper import deadline
from datetime import datetime
from datetime import timedelta

@pytest.mark.parametrize("text_delta,expected_td",[("1m", timedelta(minutes=1)),("20d", timedelta(days=20)),("12h", timedelta(hours=12))])
def test_working_deltas(text_delta,expected_td):
    assert deadline.to_timedelta(text_delta) == expected_td
    
def test_failing_deltas():
    with pytest.raises(ValueError, match=r'Wrong delta string: 1 h'):
        deadline.to_timedelta("1 h")
    with pytest.raises(ValueError, match=r'Wrong delta string: 1g'):
        deadline.to_timedelta("1g")
    with pytest.raises(ValueError, match=r'Wrong delta string: dfg'):
        deadline.to_timedelta("dfg")


def test_is_before_dealine():
    now = datetime.now()
    dl = now + timedelta(days=2)
    assert not deadline.is_before_dealine("1d", dl, now)
    assert deadline.is_before_dealine("3d", dl, now)
    assert deadline.is_before_dealine("3d", dl)
