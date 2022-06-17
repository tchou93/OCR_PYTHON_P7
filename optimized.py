from typing import List
import csv
import time

PRECISION = 1
CLIENT_BUDGET = 500


class Action:
    def __init__(self, name, price, benefits_2y, precision=0):
        self.name = name
        self.price = int(price * pow(10, precision))
        self.benefits_2y = int(benefits_2y * pow(10, precision))

    def __repr__(self):
        return f"{self.name}"


def read_csv(path: str) -> List[Action]:
    """Extract actions informations and store its in a list.

    Args:
        path (str): path of the file which contains all informations about the actions.

    Returns:
        List[Action]: List of action.
    """
    actions = []
    with open(path, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        next(spamreader)
        for row in spamreader:
            if float(row[1]) > 0.0 and float(row[2].replace("%", "")) > 0.0:
                actions.append(
                    Action(
                        row[0],
                        float(row[1]),
                        # rentability of the action in 2 years in euros = purchase price in euros * rentability of the action in 2 years in pourcent
                        float(row[1]) * float(row[2].replace("%", "")) / 100,
                        PRECISION,
                    )
                )
    return actions


def matrice_init_0(x, y):
    matrice = [[0 for i in range(x)] for j in range(y)]
    return matrice


def algo_optimized(a, c):
    matrice = matrice_init_0(c + 1, len(a) + 1)
    for y in range(1, len(a) + 1):
        for x in range(1, c + 1):
            if a[y - 1].price <= x:
                matrice[y][x] = max(
                    matrice[y - 1][x],
                    a[y - 1].benefits_2y + matrice[y - 1][x - a[y - 1].price],
                )
            else:
                matrice[y][x] = matrice[y - 1][x]

    c_tmp = c
    current_action = len(a)
    list_best_combination = []
    while c_tmp != 0 and current_action != 0:
        current_value_action = a[current_action - 1].benefits_2y
        last_value_optimized = matrice[current_action - 1][
            c_tmp - a[current_action - 1].price
        ]
        last_element = matrice[current_action][c_tmp]
        if last_element == current_value_action + last_value_optimized:
            list_best_combination.append(a[current_action - 1])
            c_tmp -= a[current_action - 1].price
        current_action -= 1

    return list_best_combination


def matrice_display(matrice):
    for i in range(len(matrice)):
        print(matrice[i])


def cost_benefit(actions):
    total_price = format(
        sum([action.price / pow(10, PRECISION) for action in actions]), f".{PRECISION}f"
    )
    total_benefits_2y = format(
        sum([action.benefits_2y / pow(10, PRECISION) for action in actions]),
        f".{PRECISION}f",
    )
    return (total_price, total_benefits_2y)


def display_results_algo(path_csv):
    actions = read_csv(path_csv)

    start = time.time()
    list_actions_max_benef = algo_optimized(actions, 500 * pow(10, PRECISION))
    end = time.time()

    (total_price, total_benefits_2y) = cost_benefit(list_actions_max_benef)
    filename = path_csv.replace("./files/", "")
    print(
        f"Le temps de l'algorithme optimisé pour le fichier {filename} ({len(actions)} actions) avec une precision de {PRECISION} est de: {end - start} secondes !"
    )
    print(f"Les actions à acheter sont: {list_actions_max_benef}")
    print(f"Le bénéfice est de: {total_benefits_2y} euros")
    print(f"Le coût d'achat est de: {total_price} euros\n")


if __name__ == "__main__":
    PRECISION = 0
    display_results_algo("./files/dataset_20_actions.csv")
    display_results_algo("./files/dataset1_1001_actions.csv")
    display_results_algo("./files/dataset2_1000_actions.csv")

    PRECISION = 2
    display_results_algo("./files/dataset1_1001_actions.csv")
    display_results_algo("./files/dataset2_1000_actions.csv")
