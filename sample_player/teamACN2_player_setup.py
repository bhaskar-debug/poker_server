import random

from model_output import get_model_output
from pypokerengine.players import BasePokerPlayer
from utils_teamACN2.card_strategy import get_card_action
from utils_teamACN2.pre_flop_strategy import get_pre_flop_action


class AiPlayer(
    BasePokerPlayer
):  # Do not forget to make parent class as "BasePokerPlayer"
    #  we define the logic to make an action through this method. (so this method would be the core of your AI)

    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
        print(f"valid_actions: {valid_actions}")
        print(f"hole_card: {hole_card}")
        print(f"round_state: {round_state}")
        action = ""
        amount = 0
        action_info = valid_actions[2]
        if round_state["street"] == "preflop":
            action, amount = get_pre_flop_action(
                hole_card, action_info["amount"]["min"], action_info["amount"]["max"]
            )
        else:
            best_hand, highest_hand = get_model_output(
                hole_card + round_state["community_card"],
                "model/saved_model_teamACN.pkl",
                "teamACN2",
            )
            action, amount = get_card_action(
                best_hand,
                highest_hand,
                action_info["amount"]["min"],
                action_info["amount"]["max"],
            )

        if action == "raise":
            if amount == -1:
                action = "call"
        if action == "call":
            action_info = valid_actions[1]
            amount = action_info["amount"]
        if action == "fold":
            action_info = valid_actions[0]
            amount = action_info["amount"]
        print(f"action played: {action}, {amount}")
        return action, amount  # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return AiPlayer()
