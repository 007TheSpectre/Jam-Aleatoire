# Poker-Dice Battler

> Epitech JAM — thème : **Le Hasard**

Roll 5 dice, form poker hands, and deal damage to a 100-HP boss. Defeat it in as few rolls as possible and land on the top-3 leaderboard.

## Requirements

```bash
pip install pillow
# Their game also needs pygame:
pip install pygame
```

## Run

```bash
python main.py
```

Must be run from the project root (asset paths are relative).

## How to play

Each turn you roll 5d6. The best poker hand formed deals damage to the boss:

| Combo | Damage |
|---|---|
| Yahtzee (5 of a kind) | 50 |
| Grande Suite (straight) | 35 |
| Carré (4 of a kind) | 25 |
| Full House | 20 |
| Brelan (3 of a kind) | 15 |
| Double Paire | 10 |
| Paire | 5 |
| Carte Haute | 2 |

Win in the fewest rolls to set a record.

## Dice Quest

The **DICE QUEST ↗** button in the main menu launches [Dice Quest](https://github.com/Felix-Lcr/random_hackaton), our linked group's game, in a separate window. It requires `pygame`.

To get the submodule after cloning:

```bash
git submodule update --init
```
