import pickle
from itertools import combinations
from statistics import mode

import numpy as np
import pandas as pd

from sample_player.logger import logger  # noqa
from sample_player.utils_teamACN.preprocess import pre_process_data

root = "content"
data_path = f"{root}/data"


def get_model_input(cards) -> list:
    """
    Converts card representations from strings to numerical values suitable for model input.

    Args:
        cards (list): A list of strings, where each string represents a single card in the format "RankSuit" (e.g., "AS", "KD").

    Returns:
        list: A list of numerical values representing the cards, where suits are mapped to integers 1-4 and ranks to integers 1-13.
    """
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
    # print(cards)
    # logger.info(cards)
    for i in cards:
        for char in list(i):
            model_input.append(char_mapping[char])

    return model_input


def get_best_hand(
    model_input,
    model_file_path=f"{root}/model/saved_model_teamACN.pkl",
    model_name="model",
):
    """
    Predicts the best poker hand category for a given set of model inputs using a pre-trained model.

    Args:
        model_input (list): A list of numerical values representing the poker hand features.
            The values should be in the order of [S1, C1, S2, C2, S3, C3, S4, C4, S5, C5],
            where Sx represents suit and Cx represents rank.
        model_file_path (str, optional): The file path to the pickled model file. Default is the path
            to the pre-trained model file.
        model_name (str, optional): The name of the model. Defaults to 'model'.

    Returns:
        int: The predicted poker hand category.
    """

    # Load the model from the pickled file
    with open(model_file_path, "rb") as file:
        loaded_model = pickle.load(file)

    # Now 'loaded_model' contains the model loaded from the pickled file
    column_names = ["S1", "C1", "S2", "C2", "S3", "C3", "S4", "C4", "S5", "C5"]

    df_model_input = pd.DataFrame([model_input], columns=column_names)

    x = pre_process_data(df_model_input)
    if "lstm" in model_name.lower():
        # Assuming model_input has shape (batch_size, num_features)
        x_reshaped = np.expand_dims(x, axis=1)
        y_pred = loaded_model.predict(x_reshaped)
        # Get the index of the maximum probability
        predicted_class = np.argmax(y_pred)
        return [predicted_class]

    y_pred = loaded_model.predict(x)
    return y_pred


def evaluate_poker_hand(hand, best_hand) -> int:
    """
    Evaluates the specific value or rank of a poker hand based on its best hand category.

    Args:
        hand (list): A list of numerical values representing the poker hand, where even indices are ranks and odd indices are suits.
        best_hand (int): The numerical category of the best possible hand (0-9).

    Returns:
        int: The value or rank of the hand's key card(s), determined based on the best hand category.
    """
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
    """
    Identifies the best possible poker hand and its rank from a collection of hands using a model.

    Args:
        hands (list): A list of lists, where each inner list represents a set of cards (e.g., [["AS", "KD"], ["QH", "JC"]]).
        team_name (str): The name of the team whose hands are being evaluated.
        model_file_path (str, optional): The file path to the pickled model file. Default is the path
            to the pre-trained model file.

    Returns:
        tuple[int, int]: A tuple containing the best hand category (0-9) and the rank of the key card(s) in that hand.
    """
    best_hands = {}
    best_hand = 0
    highest_rank = 0
    combination_length = 5
    # print(hands)
    # logger.info(hands)
    # Generate all combinations of length 'combination_length'
    all_combinations = list(combinations(hands, combination_length))
    for combination in all_combinations:
        input_list = list(combination)

        model_input = get_model_input(input_list)
        # print(model_input)
        # logger.info(model_input)

        best_input_hand = get_best_hand(model_input, model_file_path)
        # logger.info(best_input_hand)
        # print(best_input_hand)

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
    msg_best_hands = f"Best hands: {best_hands}"
    # print(msg_best_hands)
    # logger.info(msg_best_hands)

    best_hand = max(best_hands)
    highest_rank = best_hands[best_hand]
    msg_best_hand = f"{team_name} Best hand: {best_hand}"
    # print(msg_best_hand)
    # logger.info(msg_best_hand)
    msg_highest_rank = f"{team_name} Highest Rank in Hand: {highest_rank}"
    # print(msg_highest_rank)
    # logger.info(msg_highest_rank)

    logger.info("flop_strategy", best_hand=best_hand, highest_rank=highest_rank)

    return best_hand, highest_rank


if __name__ == "__main__":
    hole_card = ["CK", "C6"]
    community_card = ["C7", "C8", "C9"]
    get_model_output(
        hole_card + community_card, f"{root}/model/saved_model_teamACN.pkl", "teamACN"
    )
