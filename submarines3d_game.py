from submarines3d_engine import *
from collections import OrderedDict
from itertools import cycle
import re


def at_least_one_alive(battle_boxes):
    alive = True
    for key, box in battle_boxes.items():
        for unit in box.units:
            if not unit.unique_unit:
                alive = alive and unit.alive
    return alive


def start(battle_area, battle_units, players):
    battle_boxes = OrderedDict()
    for player in players:
        battle_boxes[player] = GameBox(player, battle_area, battle_units)

    np.random.shuffle(players)
    pool = cycle(players)
    current_player = next(pool)
    game_on = True

    print(f"Welcome to Submarines3D."
          f"\n Battle arena size: {battle_area}."
          "\n Battle units (name, amount): ")
    for name, val in battle_units.items():
        print(f"   {name.__name__}: {val}")

    print(f"Players: {players}."
          "\n Enter \"quit\" to exit game."
          "\n Enter \"show\" to see your board."
          "\n Enter \"attack player_name row,col,depth\" "
          "to execute an attack on player_name at coordinates row, col, depth")


    while game_on:
            user_input = input(
                f"Player {battle_boxes[current_player].uid[0]}:  "
            )
            if user_input == "quit":
                print("\nQuitting game.")
                break

            if user_input == "show":
                print(battle_boxes[current_player])
                continue

            if re.split(" ", user_input)[0] == "attack":
                player_to_attack = re.split(" ", user_input)[1]
                if not player_to_attack in players:
                    print("\nInvalid target player name.")
                    continue

                try:
                    coords_to_attack = tuple(map(int,re.split(",", re.split(" ", user_input)[2])))
                except ValueError:
                    print("\nCoordinates must be in row, col, depth format.")
                    continue

                if len(coords_to_attack) != 3:
                    print("\nCoordinates must be in row, col, depth format.")
                    continue

                if not (coords_to_attack[2] < 3
                        and coords_to_attack[2] >= 0):
                    print("\nInvalid depth. Depth levels are: 0, 1 or 2.")
                    continue

                if not (coords_to_attack[1] >= 0
                        and coords_to_attack[0] >= 0):
                    print("\nAttack coordinates must be positive.")
                    continue

                if not (coords_to_attack[1] < battle_area[1] and
                        coords_to_attack[0] < battle_area[0]):
                    print(f"\nAttack coordinates must be within the battle area {battle_area}.")
                    continue

                game_on = not battle_boxes[player_to_attack].execute_strike(coords_to_attack)
                if game_on:
                    if at_least_one_alive(battle_boxes):
                        current_player = next(pool)
                    else:
                        game_on = False

    if game_on == False:
        print(f"Game over. Player {battle_boxes[current_player].uid[0]} is the winner.")

if __name__ == "__main__":
    battle_area = (8,8)
    battle_units = {General: 1, Jet: 2, Submarine: 3, Destroyer: 2}

    players = ["Player1", "Player2"]

    start(battle_area=battle_area,
          battle_units=battle_units,
          players=players)


