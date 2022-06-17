from typing import List, Tuple
import csv
import time

CLIENT_BUDGET = 500


class Action:
    def __init__(
        self, name: str, purchase_price_euros: float, rentability_2y_euros: float
    ):
        """Constructor of the class Action

        Args:
            name (str): action name
            purchase_price_euros (float): action purchase_price_euros
            rentability_2y_euros (float): rentability of the action in 2 years
        """
        self.name = name
        self.purchase_price_euros = purchase_price_euros
        self.rentability_2y_euros = rentability_2y_euros

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
            actions.append(
                Action(
                    row[0],
                    float(row[1]),
                    # rentability of the action in 2 years in euros = purchase price in euros * rentability of the action in 2 years in pourcent
                    float(row[1]) * float(row[2].replace("%", "")) / 100,
                )
            )
    return actions


def find_best_combination(actions: List[Action]) -> Tuple[List[Action], float, float]:
    """Find the best combination of actions to buy with CLIENT_BUDGET.
    The algorithm complexity is O(2^N) with N the number of actions.

    Args:
        actions (List[Action]): List of all the action.

    Returns:
        Tuple[List[Action], float, float]: Tuple with the list of actions to buy,
        the rentabilty and the purchase cost in euros.
    """
    max_rentability = 0

    # Check all the combinations (0: not buy, 1:buy) of actions
    # to keep the best in term of rentability in 2 years.
    for actions_tobuy in range(1, (pow(2, len(actions)))):
        rentability_actions_tmp = 0
        purchase_price_euros_actions_tmp = 0
        actions_choosed_tmp = []

        # Check all the position with 1 (buy) in actions_tobuy convert
        # in binary.
        positions_actions_tobuy = [
            pos
            for pos, char in enumerate(format(actions_tobuy, f"{len(actions)}b"))
            if char == "1"
        ]

        # Calcul the rentabilty of all the actions to buy.
        for position_action_tobuy in positions_actions_tobuy:
            rentability_actions_tmp += actions[
                position_action_tobuy
            ].rentability_2y_euros
            purchase_price_euros_actions_tmp += actions[
                position_action_tobuy
            ].purchase_price_euros
            actions_choosed_tmp.append(actions[position_action_tobuy])

            # If the purchase price > CLIENT_BUDGET then it is not necessary
            # to continue, the combination is not the good one.
            if purchase_price_euros_actions_tmp > CLIENT_BUDGET:
                break
        # If the purchase price is in the range and if the rentability
        # is the best then we store all the tempory variables.
        if purchase_price_euros_actions_tmp <= CLIENT_BUDGET:
            if rentability_actions_tmp > max_rentability:
                max_rentability = rentability_actions_tmp
                actions_choosed = actions_choosed_tmp
                purchase_price_euros_actions = purchase_price_euros_actions_tmp
    return (actions_choosed, max_rentability, purchase_price_euros_actions)


if __name__ == "__main__":
    """From a CSV actions file, check the best combination and display it, also with
    the time of execution.
    """

    actions = read_csv("./files/dataset_20_actions.csv")
    start = time.time()
    (
        actions_choosed,
        max_rentability,
        purchase_price_euros_actions,
    ) = find_best_combination(actions)
    end = time.time()
    print(
        f"Le temps de l'algorithme bruteforce pour {len(actions)} actions est de: {end - start} secondes !"
    )
    print(f"Les actions à acheter sont: {actions_choosed}")
    print(f"Le bénéfice est de: {max_rentability} euros")
    print(f"Le coût d'achat est de: {purchase_price_euros_actions} euros")
