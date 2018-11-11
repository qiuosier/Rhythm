from collections import OrderedDict


def credit_cards(data):
    cards = data.get("cards", [])
    # Get all the available categories
    categories = {}
    for card in cards:
        reward = card.get("reward", {})
        reward_cat = reward.get("categories", {})
        for cat, value in reward_cat.items():
            categories[cat] = categories.get(cat, 0) + 1
    
    categories = OrderedDict(sorted(categories.items(), key=lambda (k, v): v, reverse=True))
    print(categories)
    context = {
        "categories": categories,
        "cards": cards
    }
    return context
