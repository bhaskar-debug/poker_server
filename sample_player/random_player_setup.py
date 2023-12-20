import random

from pypokerengine.players import BasePokerPlayer


class AiPlayer(
    BasePokerPlayer
):  # Do not forget to make parent class as "BasePokerPlayer"
    #  we define the logic to make an action through this method. (so this method would be the core of your AI)

    def get_best_hands(cards):
        suit = {"H": 1, "S": 2, "D": 3, "C": 4}
        rank = {"A": 1, "J": 11, "Q": 13, "K": 13}

        model_input = []

        for i in cards:
            a = i.split(",")

    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
        print(f"valid_actions: {valid_actions}")
        print(f"hole_card: {hole_card}")
        print(f"round_state: {round_state}")

        self.get_best_hands(hole_card + round_state["community_card"])

        action = random.choice(valid_actions)["action"]

        if action == "raise":
            action_info = valid_actions[2]
            amount = random.randint(
                action_info["amount"]["min"], action_info["amount"]["max"]
            )
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
