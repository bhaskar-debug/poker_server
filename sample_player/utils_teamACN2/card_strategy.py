def get_card_action(best_hand, highest_hand, min_amount, max_amount):
    if best_hand >= 8 and highest_hand > 8:
        raise_amount = min_amount <= max_amount * 0.3 <= max_amount
        return "raise", raise_amount
    elif best_hand >= 7 and highest_hand > 7:
        raise_amount = min_amount <= max_amount * 0.15 <= max_amount
        return "raise", raise_amount
    elif best_hand > 3 and best_hand < 7:
        return "call", 0
    else:
        return "fold", 0
