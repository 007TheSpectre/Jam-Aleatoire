from collections import Counter


def calculer_degats(des):
    compte = Counter(des)
    valeurs = sorted(compte.values(), reverse=True)
    des_uniques = sorted(set(des))
    est_suite = len(des_uniques) == 5 and (des_uniques[-1] - des_uniques[0] == 4)

    if valeurs == [5]:
        return "YAHTZEE", 50
    if est_suite:
        return "GRANDE SUITE", 35
    if valeurs == [4, 1]:
        return "CARRÉ", 25
    if valeurs == [3, 2]:
        return "FULL HOUSE", 20
    if valeurs == [3, 1, 1]:
        return "BRELAN", 15
    if valeurs == [2, 2, 1]:
        return "DOUBLE PAIRE", 10
    if valeurs == [2, 1, 1, 1]:
        return "PAIRE", 5
    return "CARTE HAUTE", 2
