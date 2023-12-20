import pickle

import numpy as np


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
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
    }
    # Combine dictionaries using the update method
    char_mapping = {}
    char_mapping.update(suit)
    char_mapping.update(rank)
    model_input = []
    print(cards)
    for i in cards:
        for char in list(i):
            model_input.append(char_mapping[char])

    return model_input


hole_card = ["CK", "C6"]
community_card = ["C7", "C8", "C9"]


def get_best_hand(model_input):
    # Specify the path to your pickled model file
    model_file_path = "model/saved_model.pkl"

    # Load the model from the pickled file
    with open(model_file_path, "rb") as file:
        loaded_model = pickle.load(file)

    # Now 'loaded_model' contains the model loaded from the pickled file
    column_names = ["S1", "C1", "S2", "C2", "S3", "C3", "S4", "C4", "S5", "C5"]

    df_model_input = pd.DataFrame([model_input], columns=column_names)

    x = process_data(df_model_input)
    y_pred = loaded_model.predict(x)
    return y_pred


model_input = get_model_input(hole_card + community_card)
print(model_input)

best_hand = get_best_hand(model_input)
print(best_hand)
