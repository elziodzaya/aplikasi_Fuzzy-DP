import numpy as np
import pandas as pd
from scipy.stats import norm

# =========================
# ERROR METRICS (FUZZY)
# =========================

def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def mape(y_true, y_pred):
    y_true = np.where(y_true == 0, 1e-8, y_true)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def smape(y_true, y_pred):
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2
    denom = np.where(denom == 0, 1e-8, denom)
    return np.mean(np.abs(y_true - y_pred) / denom) * 100


# =========================
# DIEBOLD–MARIANO TEST
# =========================

def diebold_mariano(actual, pred_fuzzy, pred_baseline):
    e1 = actual - pred_fuzzy
    e2 = actual - pred_baseline

    d = (e1 ** 2) - (e2 ** 2)
    dm_stat = np.mean(d) / np.sqrt(np.var(d, ddof=1) / len(d))
    p_value = 2 * (1 - norm.cdf(abs(dm_stat)))

    return dm_stat, p_value


# =========================
# VALIDATION SUMMARY
# =========================

def validation_summary(actual, fuzzy, baseline=None):
    summary = {
        "MAE": mae(actual, fuzzy),
        "RMSE": rmse(actual, fuzzy),
        "MAPE (%)": mape(actual, fuzzy),
        "sMAPE (%)": smape(actual, fuzzy)
    }

    if baseline is not None:
        dm_stat, p_val = diebold_mariano(
            np.array(actual),
            np.array(fuzzy),
            np.array(baseline)
        )
        summary.update({
            "DM Statistic": dm_stat,
            "p-value": p_val,
            "Significant (α=0.05)": p_val < 0.05
        })

    return pd.DataFrame([summary])


# =========================
# KPI DYNAMIC PROGRAMMING
# =========================

def calculate_kpis(
    df_policy,
    demand,
    import_cost,
    holding_cost,
    max_stock
):
    total_import = df_policy["Impor_Optimal"].sum()
    total_holding_cost = df_policy["Holding_Cost"].sum()
    total_cost = total_import * import_cost + total_holding_cost

    avg_inventory = df_policy["Stok_Akhir"].mean()

    stockout_rate = (df_policy["Stok_Akhir"] <= 0).mean()
    overstock_rate = (df_policy["Stok_Akhir"] >= 0.9 * max_stock).mean()

    total_demand = np.sum(demand)
    service_level = 1 - stockout_rate

    cost_per_unit = total_cost / total_demand if total_demand > 0 else 0
    inventory_turnover = total_demand / avg_inventory if avg_inventory > 0 else 0

    return {
        "Total Import": total_import,
        "Total Cost": total_cost,
        "Average Inventory": avg_inventory,
        "Stockout Rate": stockout_rate,
        "Overstock Rate": overstock_rate,
        "Service Level": service_level,
        "Cost per Unit Demand": cost_per_unit,
        "Inventory Turnover": inventory_turnover
    }
