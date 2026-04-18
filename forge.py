import pandas as pd
import random

def run_forge():
    data = []

    attack_types = ["ATTACK", "SAFE"]

    for _ in range(50):
        row = {
            "feature1": random.randint(1, 100),
            "feature2": random.randint(1, 100),
            "feature3": random.randint(1, 100),
            "attack_type": random.choice(attack_types)
        }
        data.append(row)

    df = pd.DataFrame(data)

    return df
