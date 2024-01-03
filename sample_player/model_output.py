import pickle
from itertools import combinations
from statistics import mode

import pandas as pd

from sample_player.logger import logger  # noqa
from sample_player.utils_teamACN.preprocess import pre_process_data

root = "content"
data_path = f"{root}/data"


def get_model_input(cards) -> list:
    suit = {"H": 1, "S": 2, "D": 3, "C": 4}
    rank = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
    }
    # Combine dictionaries using the update method
    char_mapping = {}
    char_mapping.update(suit)
    char_mapping.update(rank)
    model_input = []
    logger.info(cards)
    for i in cards:
        for char in list(i):
            model_input.append(char_mapping[char])

    return model_input


def get_best_hand(model_input, model_file_path=f"{root}/model/saved_model_teamACN.pkl"):
    # Specify the path to your pickled model file

    # Load the model from the pickled file
    with open(model_file_path, "rb") as file:
        loaded_model = pickle.load(file)

    # Now 'loaded_model' contains the model loaded from the pickled file
    column_names = ["S1", "C1", "S2", "C2", "S3", "C3", "S4", "C4", "S5", "C5"]

    df_model_input = pd.DataFrame([model_input], columns=column_names)

    x = pre_process_data(df_model_input)
    y_pred = loaded_model.predict(x)
    return y_pred


def evaluate_poker_hand(hand, best_hand) -> int:
    # Sort the hand by rank
    sorted_hand = sorted(hand[1::2], reverse=True)

    is_nothing = best_hand == 0
    is_1_pair = best_hand == 1
    is_2_pairs = best_hand == 2
    is_3_of_kind = best_hand == 3
    is_straight = best_hand == 4
    is_flush = best_hand == 5
    is_full_house = best_hand == 6
    is_4_of_kind = best_hand == 7
    is_straight_flush = best_hand == 8
    is_royal_flush = best_hand == 9

    if is_nothing or is_straight or is_flush or is_straight_flush or is_royal_flush:
        return max(sorted_hand)

    if is_1_pair or is_2_pairs or is_3_of_kind or is_4_of_kind or is_full_house:
        return mode(sorted_hand)


def get_model_output(
    hands, team_name, model_file_path=f"{root}/model/saved_model_teamACN.pkl"
):
    best_hands = {}
    best_hand = 0
    highest_rank = 0
    combination_length = 5
    logger.info(hands)
    # Generate all combinations of length 'combination_length'
    all_combinations = list(combinations(hands, combination_length))
    for combination in all_combinations:
        input_list = list(combination)

        model_input = get_model_input(input_list)
        logger.info(model_input)

        best_input_hand = get_best_hand(model_input, model_file_path)
        logger.info(best_input_hand)
        highest_rank = evaluate_poker_hand(model_input, best_input_hand)

        # Check if the key exists in best_hands and if the current highest_rank is greater
        if (
            best_input_hand[0] in best_hands
            and best_hands[best_input_hand[0]] < highest_rank
        ):
            best_hands[best_input_hand[0]] = highest_rank
        elif best_input_hand[0] not in best_hands:
            # If the key doesn't exist, add it to the dictionary
            best_hands[best_input_hand[0]] = highest_rank

    logger.info(f"Best hands: {best_hands}")
    best_hand = max(best_hands)
    highest_rank = best_hands[best_hand]
    logger.info(f"{team_name} Best hand: {best_hand}")
    logger.info(f"{team_name} Highest Rank in Hand: {highest_rank}")

    return best_hand, highest_rank


if __name__ == "__main__":
    hole_card = ["CK", "C6"]
    community_card = ["C7", "C8", "C9"]
    get_model_output(
        hole_card + community_card, f"{root}/model/saved_model_teamACN.pkl", "teamACN"
    )
