import numpy as np
from enum import Enum
from uuid import uuid4



class Unit:
    def __init__(self, parent,
                 uid=0,
                 unit_shape=np.array([]),
                 location=(0,0),
                 level=0,
                 one_hit_kill=False,
                 unique_unit=False):

        self.parent = parent
        self.uid = uid
        self.alive = True
        self.location = location
        self.components = list()
        self.create_unit_components()
        self.unit_shape = unit_shape
        self.level = level
        self.one_hit_kill = one_hit_kill
        self.unique_unit = unique_unit

    def unit_hit(self):
        # If a unit is hit, we check if it's a one hit kill unit or not. If it is, we kill it. Otherwise we check
        # if there is any component left alive, and if so, we just send a HIT signal. If no components are left, the
        # unit is dead.

        if not self.one_hit_kill:
            print("Signal.HIT")
            for c in self.components:
                if c.value != 0:
                    return None
        self.kill()

    def kill(self):
        # In case a kill signal is sent to the unit, all components vanish and the unit is not longer alive.

        print("Signal.KILL")
        for c in self.components:
            c.value = 0
        self.alive = False

    def create_unit_components(self):
        # This method adds components to a Battle Unit

        for r in range(self.unit_shape.shape[0]):
            for c in range(self.unit_shape.shape[1]):
                loc = (self.location[0] + r, self.location[1] + c)
                value = self.unit_shape[r, c]
                self.components.append(Component(self, loc, value))

class Submarine(Unit):
    # Lives on level 0 (underwater), is dead after getting hit once.
    unique_unit = False
    unit_shape = np.array([[1, 1, 1]])
    one_hit_kill = True
    level = 0

class Destroyer(Unit):
    # Lives on level 1 (sea level), dies when all hit points are hit.
    unique_unit = False
    unit_shape = np.array([[1, 1, 1, 1]])
    one_hit_kill = False
    level = 1

class Jet(Unit):
    # Lives on level 2 (air), is dead after getting hit once.
    unique_unit = False
    unit_shape = np.array([
        [0,1,0],
        [1,1,1],
        [0,1,0],
        [0,1,0]])
    one_hit_kill = True
    level = 2

class General(Unit):
    # A unique unit which triggers game over when dead, may live in any of the GameBox levels.
    unique_unit = True
    level = np.random.randint(0, 3)
    unit_shape = np.array([[1]])
    one_hit_kill = True
    def __init__(self, parent, uid, unit_shape, location, level, one_hit_kill, unique_unit):
        super().__init__(parent, uid, unit_shape, location, level, one_hit_kill, unique_unit)

    def kill(self):
        for unit in self.parent.units:
            unit.alive = False


class Component:
    # Every battle unit consists of components which have a value and a location (coordinate on board).
    # parent_unit is this Component's parent battle unit.
    # location is a tuple of (row, column, level) with respect to GameBox coordinates.
    # value gets 0 if Component was hit
    # do_damage() is executed upon opponent's successful hit

    def __init__(self, parent_unit: Unit, location: tuple, value):
        self.parent = parent_unit
        self.location = location
        self.value = value

    def __repr__(self):
        if self.value == 0:
            return "0"
        return f"{type(self.parent).__name__[0]}{self.parent.uid}"

    def do_damage(self):
        if self.value == 1:
            self.value = 0
            self.parent.unit_hit()


class GameBox:
    def __init__(self, player_name, area_size, battle_units):
        assert isinstance(player_name, str), "Player name is not a string."
        assert ((area_size[0] > 0) and (area_size[1] > 0)), "Minimum playable board area is 1x1."
        assert (len(battle_units) > 0), "At least one battle unit per board is expected."
        for unit, num in battle_units.items():
            if unit.unique_unit:
                assert (num <= 1), "No more than 1 unique unit allowed!"
            assert (num > 0), "Invalid unit number (cannot be zero)"

        self.uid = [player_name, uuid4()]
        self.area_size = area_size # rows, cols
        # initialize the game box, np.object will let us populate the box with Battle Unit Components
        self.box = np.zeros((area_size[0], area_size[1], 3), dtype=np.object)
        self.units = []
        self.num_of_units = len(self.units)
        self.place_battle_units(battle_units)

    def __str__(self):
        return f"Board uid: {self.uid} \nIn air: \n{self.box[:,:,2]} \nSea surface: \n{self.box[:,:,1]} " \
            f"\nIn depth: \n{self.box[:,:,0]}"

    def place_battle_units(self, battle_unit_list):
        # This method is responsible for populating the Game Box with Battle Unit components in a random fashion.
        for unit, num in battle_unit_list.items():

            for num in range(battle_unit_list[unit]):
                row, col, flip = self.get_free_row_col(unit)
                if flip:
                    unit.unit_shape = unit.unit_shape.T
                self.units.append(unit(self,
                                       uid=num,
                                       unit_shape=unit.unit_shape,
                                       location=(row, col),
                                       level=unit.level,
                                       one_hit_kill=unit.one_hit_kill,
                                       unique_unit=unit.unique_unit))

                for c in self.units[-1].components:
                    coord = c.location
                    self.box[coord[0], coord[1], self.units[-1].level] = c


    def get_free_row_col(self, unit):
        # This method is responsible for getting a vacant cell
        # in the Game Box which will be occupied by a Battle Unit

        vacant_cells = np.array(np.where(self.box[:,:,unit.level] == 0)).T
        np.random.shuffle(vacant_cells)
        flips = [False, True]
        np.random.shuffle(flips)
        for cell in vacant_cells:
            # In case a unit in one configuration is too large, we flip it and try again.
            for f in flips:
                place = self.check_vacancy(cell, unit, self.box, f)
                if not place:
                    continue
                else:
                    return cell[0], cell[1], f

        raise AssertionError(f"Cannot find a vacant space for {unit}.")

    @staticmethod
    def check_vacancy(cell, unit, box, flip):
        # Here we look at the unit shape and check whether it has enough
        # space to be placed in the Game Box

        unit_cols = unit.unit_shape.shape[1]
        unit_rows = unit.unit_shape.shape[0]
        if flip:
            unit_cols, unit_rows = unit_rows, unit_cols

        end_cell = (cell[0] + unit_rows - 1, cell[1] + unit_cols - 1)
        box_cols = box.shape[1]
        box_rows = box.shape[0]

        if ((end_cell[0] <= box_rows) and (end_cell[1] <= box_cols)):
            for c in range(unit_cols):
                for r in range(unit_rows):
                    try:
                        if box[cell[0] + r, cell[1] + c, unit.level] != 0:
                            return False
                    except IndexError:
                        return False
            return True
        else:
            return False

    def execute_strike(self, coords: tuple):
        if self.box[coords] == 0 or self.box[coords].value==0:
            print("Signal.MISS")
        else:
            self.box[coords].do_damage()
        return self.is_gameover()

    def is_gameover(self):
        for unit in self.units:
            if not unit.alive:
                print("Signal.END")
                return True
            else:
                return False


class GamePieces(Enum):
    # This class is an enumeration class for the different battle units.
    General = General
    Jet = Jet
    Destroyer = Destroyer
    Submarine = Submarine


