import numpy as np
import pandas as pd

def dp_deterministic_horizon(
    demand,
    fuzzy_import,
    holding_cost,
    import_cost,
    max_stock,
    initial_stock
):
    """
    Deterministic finite-horizon DP (12 bulan)
    """

    T = len(demand)

    # Action space dibatasi oleh fuzzy
    def action_space(fuzzy_value):
        base = int(round(fuzzy_value))
        return sorted(set([
            max(0, base - 50),
            base,
            base + 50
        ]))

    V = np.zeros((T+1, max_stock+1))
    policy = np.zeros((T, max_stock+1))

    for t in reversed(range(T)):
        for s in range(max_stock+1):
            best_cost = 1e15
            best_action = 0

            for a in action_space(fuzzy_import[t]):
                new_stock = s + a - demand[t]

                if new_stock < 0:
                    continue

                new_stock = min(max_stock, new_stock)

                cost = (
                    import_cost * a +
                    holding_cost * new_stock
                )

                total_cost = cost + V[t+1, new_stock]

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_action = a

            V[t, s] = best_cost
            policy[t, s] = best_action

    # Simulasi kebijakan optimal
    stock = initial_stock
    results = []

    for t in range(T):
        action = int(policy[t, stock])
        new_stock = min(max_stock, stock + action - demand[t])

        results.append({
            "Month": t+1,
            "Demand": demand[t],
            "Impor_Fuzzy": round(fuzzy_import[t],2),
            "Impor_Optimal": action,
            "Stok_Awal": stock,
            "Stok_Akhir": new_stock,
            "Holding_Cost": holding_cost * new_stock,
            "Import_Cost": import_cost * action
        })

        stock = new_stock

    return pd.DataFrame(results), V[0, initial_stock]
