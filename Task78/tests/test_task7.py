from task7 import chain_sum


def test_chain_sum():
    assert chain_sum(5)() == 5
    assert chain_sum(5)(2)() == 7
    assert chain_sum(5)(100)(-10)() == 95
    assert chain_sum() == 0
