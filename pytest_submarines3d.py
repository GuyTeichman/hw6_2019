import pytest
from submarines3d_engine import *

def test_create_gamebox():
    assert GameBox("Test", (10, 10), {General: 1, Submarine: 2, Destroyer: 2, Jet: 2})

def test_gamebox_too_small():
    with pytest.raises(AssertionError) as AE:
        box = GameBox("Test", (3,4), {Jet:2})
    assert "Cannot find a vacant space" in str(AE)

def test_odd_player_name():
    with pytest.raises(AssertionError) as AE:
        box = GameBox(1, (10, 10), {General: 1})
    assert "Player name is not a string" in str(AE)

def test_gamebox_zero_size():
    with pytest.raises(AssertionError) as AE:
        box = GameBox("Test", (10, 0), {General: 1})
    assert "Minimum playable board area" in str(AE)
    with pytest.raises(AssertionError) as AE:
        box = GameBox("Test", (0, 10), {General: 1})
    assert "Minimum playable board area" in str(AE)

def test_no_battle_units():
    with pytest.raises(AssertionError) as AE:
        box = GameBox("Test", (10, 10), {})
    assert "At least one battle unit per board is expected" in str(AE)

def test_more_than_one_unique_unit():
    with pytest.raises(AssertionError) as AE:
        box = GameBox("Test", (10, 10), {General: 2})
    assert "No more than 1 unique unit allowed" in str(AE)

def test_zero_units():
    with pytest.raises(AssertionError) as AE:
        box = GameBox("Test", (10, 10), {General: 0})
    assert "Invalid unit number" in str(AE)
