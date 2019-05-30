import pytest
import numpy as np
import matplotlib.pyplot as plt
from submarines_3d import *


def test_submarine_creation():
    assert Submarine((0, 0), 0, False)


def test_submarine_creation():
    assert Destroyer((0, 0), 0, False)


def test_jet_creation():
    assert Jet((0, 0), 0, False)


def test_coordinates_not_tuple():
    pass

def test_top_left_coordinate_not_in_board():
    pass

def test_game_piece_out_of_bounds():
    pass

def test_game_piece_overlap():
    pass



