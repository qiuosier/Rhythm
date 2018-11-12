from collections import OrderedDict


def credit_cards(data):
    cards = data.get("cards", [])
    # Get all the available categories
    # key = category name
    # value = a list of tuples (card, normalized reward value) for cards having this reward category.
    categories = {}
    for card in cards:
        reward = card.get("reward", {})
        reward_categories = reward.get("categories", {})
        for category, value in reward_categories.items():
            # Normalize the reward value
            reward_value = reward.get("value", 1)
            normalized_value = round(value * reward_value, 1)
            reward["value"] = round(reward_value, 2)
            reward_categories[category] = normalized_value
            # Add card to the category
            card_list = categories.get(category, [])
            card_list.append((card, normalized_value))
            categories[category] = card_list
    categories = OrderedDict(sorted(categories.items(), key=lambda (k, v): len(v), reverse=True))
    
    # Store the categories with only one card
    singles = []
    # For each category, store the max and min reward cards.
    # key = category
    # value = a list of cards with max or min rewards in this category
    max_rewards = {}
    min_rewards = {}

    for category, card_list in categories.items():
        # Store the categories with only one card
        if len(card_list) == 1:
            singles.append(category)
        # Find the cards with max and min reward in each category
        reward_list = []
        for card in cards:
            reward = card.get("reward", {})
            reward_categories = reward.get("categories", {})
            reward_value = reward_categories.get(category, reward_categories.get("Base"))
            reward_list.append((card, reward_value))
        reward_list.sort(key=lambda (k, v): v, reverse=True)
        # The max and min reward values in this category
        max_value = reward_list[0][1]
        min_value = reward_list[-1][1]
        for card, value in reward_list:
            if value == max_value:
                l = max_rewards.get(category, [])
                l.append(card["name"])
                max_rewards[category] = l
            if value == min_value:
                l = min_rewards.get(category, [])
                l.append(card["name"])
                min_rewards[category] = l

    # Remove categories that have only one card (Show the rewards in "Others")
    for category in singles:
        card = categories[category][0][0]
        reward = card.get("reward", {})
        reward_categories = reward.get("categories", {})
        others = reward_categories.get("Others", [])
        others.append("%s: %.1f" % (category, reward_categories[category]))
        reward_categories["Others"] = others
        categories.pop(category)
    data.update({
        "categories": categories,
        "cards": cards,
        "max_rewards": max_rewards,
        "min_rewards": min_rewards,
    })
    return data
