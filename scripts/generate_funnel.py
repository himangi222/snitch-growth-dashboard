import pandas as pd
import numpy as np

# Read catalog
catalog = pd.read_csv("data/snitch_catalog.csv")

events = []

NUM_USERS = 100000

for i in range(NUM_USERS):

    user_id = i + 1

    viewed = np.random.choice([1,0], p=[0.45,0.55])

    if viewed:

        product = catalog.sample(1).iloc[0]

        add_to_cart = np.random.choice([1,0], p=[0.10,0.90])

        purchase = 0

        if add_to_cart:

            purchase = np.random.choice([1,0], p=[0.35,0.65])

        events.append({
            "user_id": user_id,
            "product_id": product['product_id'],
            "category": product['category'],
            "price": product['price'],
            "viewed_pdp": viewed,
            "added_to_cart": add_to_cart,
            "purchased": purchase
        })

df = pd.DataFrame(events)

df.to_csv("data/funnel_data.csv", index=False)

print(df.head())

print("Funnel Simulation Complete!")