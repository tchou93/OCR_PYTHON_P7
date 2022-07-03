from typing import List, Tuple
import csv
import time

# Global variables

# PRECISION indicate the precision we need for the algorithms
# 0 => float with no precision
# 1 => float with precision of 10th
# 2 => float with precision of 100th ect..
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


def matrix_init_0(x: int, y: int) -> List[List[int]]:
    """Init a matrix to 0.

    Args:
        x (int): number of columns
        y (int): number of rows

    Returns:
        List[List[int]]: Init Matrice[y,x] to 0
    """
    matrix = [[0 for i in range(x)] for j in range(y)]
    return matrix


def algo_optimized(a: List[Action], c: int) -> List[Action]:
    """Implement the Knapsack algorithm.

    Args:
        a (List[Action]): List of all the actions
        c (int): capacity (client budget)

    Returns:
        List[Action]: List of actions to buy
    """

    # init the matrix, first line and first colomn
    # should always equal to 0
    matrix = matrix_init_0(c + 1, len(a) + 1)
    for y in range(1, len(a) + 1):
        for x in range(1, c + 1):
            if a[y - 1].price <= x:
                matrix[y][x] = max(
                    matrix[y - 1][x],
                    a[y - 1].benefits_2y + matrix[y - 1][x - a[y - 1].price],
                )
            else:
                matrix[y][x] = matrix[y - 1][x]

    # When the algo is done, we find the list of
    # actions we buy with the last value of the matrix.
    c_tmp = c
    current_action = len(a)
    list_best_combination = []
    # When the capacity is equal 0 or all the actions
    # have been checked then we have the list of the actions
    # we need to buy.
    while c_tmp != 0 and current_action != 0:
        current_value_action = a[current_action - 1].benefits_2y
        last_value_optimized = matrix[current_action - 1][
            c_tmp - a[current_action - 1].price
        ]
        last_element = matrix[current_action][c_tmp]
        if last_element == current_value_action + last_value_optimized:
            list_best_combination.append(a[current_action - 1])
            c_tmp -= a[current_action - 1].price
        current_action -= 1

    return list_best_combination


def cost_profit(actions: List[Action]) -> Tuple[float, float]:
    """Calcul the cost and profit of a group of actions.

    Args:
        actions (List[Action]): List of action we need to buy

    Returns:
        Tuple[float, float]: return the tuple (total price, total benefits for 2 years)
    """
    total_price = format(
        sum([action.price / pow(10, PRECISION) for action in actions]), f".{PRECISION}f"
    )
    total_benefits_2y = format(
        sum([action.benefits_2y / pow(10, PRECISION) for action in actions]),
        f".{PRECISION}f",
    )
    return (total_price, total_benefits_2y)


def display_results_algo(path_csv: str):
    """Call the function algo_optimized with actions obtains in the file path_csv
    and display the results.

    Args:
        path_csv (str): path of the csv with contain all the action/price/benefit
    """
    actions = read_csv(path_csv)

    start = time.time()
    list_actions_max_benef = algo_optimized(actions, CLIENT_BUDGET * pow(10, PRECISION))
    end = time.time()

    (total_price, total_benefits_2y) = cost_profit(list_actions_max_benef)
    filename = path_csv.replace("./datas/", "")
    print(
        f"Le temps de l'algorithme optimisé pour le fichier {filename} ({len(actions)} actions) avec une precision de {PRECISION} est de: {end - start} secondes !"
    )
    print(f"Les actions à acheter sont: {list_actions_max_benef}")
    print(f"Le bénéfice est de: {total_benefits_2y} euros")
    print(f"Le coût d'achat est de: {total_price} euros\n")


if __name__ == "__main__":
    PRECISION = 2
    display_results_algo("./datas/dataset_20_actions.csv")
    display_results_algo("./datas/dataset1_1001_actions.csv")
    display_results_algo("./datas/dataset2_1000_actions.csv")

    PRECISION = 3
    display_results_algo("./datas/dataset_20_actions.csv")
