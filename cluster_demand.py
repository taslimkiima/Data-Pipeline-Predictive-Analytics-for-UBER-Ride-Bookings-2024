# ============================================================
# cluster_demand.py
# - Forecast HOURLY DEMAND per trip_segment (cluster 0/1/2)
# - Model: Baseline Naive + Prophet
# - Output per cluster di folder output_cluster_demand/
# ============================================================

import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error, mean_squared_error

# Try import Prophet
try:
    from prophet import Prophet
    HAS_PROPHET = True
except:
    print("⚠ Prophet tidak tersedia, hanya baseline yang dijalankan.")
    HAS_PROPHET = False

# ------------------------------------------------------------
# PATH CONFIG
# ------------------------------------------------------------

OUT_SEG   = "outputs_segmentation"
SEG_CSV   = os.path.join(OUT_SEG, "segmented_trips.csv")

OUT_CLUSTER = "output_cluster_demand"
os.makedirs(OUT_CLUSTER, exist_ok=True)


# ------------------------------------------------------------
# UTIL FUNCTIONS
# ------------------------------------------------------------

def load_segmented_data() -> pd.DataFrame:
    if not os.path.exists(SEG_CSV):
        raise FileNotFoundError(
            f"{SEG_CSV} tidak ditemukan. Jalankan segmentasi.py terlebih dahulu."
        )
    df = pd.read_csv(SEG_CSV, parse_dates=["datetime"])
    return df


def build_cluster_hourly(df: pd.DataFrame, cluster_id: int) -> pd.DataFrame:
    sub = df[df["trip_segment"] == cluster_id].copy()
    if sub.empty:
        return None

    df_ts = (
        sub
        .groupby(pd.Grouper(key="datetime", freq="H"))
        .size()
        .reset_index(name="y")
        .rename(columns={"datetime": "ds"})
    )

    df_ts["cluster"] = cluster_id
    df_ts = df_ts.sort_values("ds").reset_index(drop=True)
    return df_ts


def train_test_split_time(df_ts: pd.DataFrame, ratio: float = 0.2):
    n = len(df_ts)
    n_test = int(n * ratio)
    df_train = df_ts.iloc[:-n_test].copy()
    df_test  = df_ts.iloc[-n_test:].copy()
    return df_train, df_test


def baseline_naive_last(train, test):
    last_value = train["y"].iloc[-1]
    return np.full(len(test), last_value)


def model_prophet(train, test):
    m = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
        seasonality_mode="additive",
    )
    m.fit(train[["ds", "y"]])

    future = pd.DataFrame({"ds": test["ds"].values})
    forecast = m.predict(future)
    y_pred = forecast["yhat"].values

    return y_pred, forecast, m


def eval_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mape = (np.abs((y_true - y_pred) / np.maximum(y_true, 1e-6))).mean() * 100
    return mae, rmse, mape


def plot_forecast(df_train, df_test, y_pred, model_name, cluster_id):
    plt.figure(figsize=(12, 5))

    plt.plot(df_train["ds"], df_train["y"], label="Train")
    plt.plot(df_test["ds"], df_test["y"], label="Actual Test")
    plt.plot(df_test["ds"], y_pred, label=f"Predicted ({model_name})")

    plt.title(f"Cluster {cluster_id} Demand Forecast - {model_name}")
    plt.xlabel("Time")
    plt.ylabel("Demand")
    plt.legend()
    plt.tight_layout()

    fname = f"cluster_{cluster_id}_forecast_plot_{model_name}.png"
    plt.savefig(os.path.join(OUT_CLUSTER, fname), dpi=300)
    plt.close()
    print(f"  💾 Plot saved → {fname}")


# ------------------------------------------------------------
# MAIN PIPELINE
# ------------------------------------------------------------

def run_cluster_demand():
    print("📥 Loading segmented trips...")
    df = load_segmented_data()
    print("Shape:", df.shape)

    clusters = sorted(df["trip_segment"].unique())
    print("\n🔎 Clusters ditemukan:", clusters)

    metrics_all = []

    for cluster_id in clusters:
        print("\n========================================")
        print(f"  🔥 CLUSTER {cluster_id}")
        print("========================================")

        df_ts = build_cluster_hourly(df, cluster_id)

        if df_ts is None or df_ts["y"].sum() == 0:
            print(f"  ⚠ Cluster {cluster_id} tidak punya data cukup. Skip.")
            continue

        # Simpan hourly demand
        hourly_path = os.path.join(OUT_CLUSTER, f"cluster_{cluster_id}_hourly.csv")
        df_ts.to_csv(hourly_path, index=False)
        print(f"  💾 Hourly demand saved → {hourly_path}")

        # Train-test split
        df_train, df_test = train_test_split_time(df_ts, ratio=0.2)
        print(f"  Train={len(df_train)}, Test={len(df_test)}")

        # ------------------- Baseline -------------------
        print("  🚀 Baseline model...")
        y_pred_base = baseline_naive_last(df_train, df_test)
        mae, rmse, mape = eval_metrics(df_test["y"], y_pred_base)

        # Save baseline forecast
        base_csv = os.path.join(OUT_CLUSTER, f"cluster_{cluster_id}_forecast_baseline.csv")
        df_out = df_test[["ds", "y"]].copy()
        df_out["y_pred"] = y_pred_base
        df_out.to_csv(base_csv, index=False)
        print(f"  💾 Baseline forecast → {base_csv}")

        plot_forecast(df_train, df_test, y_pred_base, "baseline", cluster_id)

        metrics_all.append({
            "cluster": cluster_id,
            "model": "baseline",
            "mae": mae,
            "rmse": rmse,
            "mape": mape
        })

        # ------------------- Prophet -------------------
        if HAS_PROPHET:
            print("  🚀 Prophet model...")
            try:
                y_pred_prophet, forecast_obj, m = model_prophet(df_train, df_test)
                mae_p, rmse_p, mape_p = eval_metrics(df_test["y"], y_pred_prophet)

                # Save prophet test forecast
                prop_csv = os.path.join(OUT_CLUSTER, f"cluster_{cluster_id}_forecast_prophet_test.csv")
                df_out2 = df_test[["ds", "y"]].copy()
                df_out2["y_pred"] = y_pred_prophet
                df_out2.to_csv(prop_csv, index=False)
                print(f"  💾 Prophet forecast → {prop_csv}")

                plot_forecast(df_train, df_test, y_pred_prophet, "prophet", cluster_id)

                # Future 7 days
                future = m.make_future_dataframe(periods=168, freq="H")
                future_pred = m.predict(future)
                future_csv = os.path.join(OUT_CLUSTER, f"cluster_{cluster_id}_forecast_prophet_future.csv")
                future_pred[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(future_csv, index=False)
                print(f"  💾 Future 7-day forecast → {future_csv}")

                metrics_all.append({
                    "cluster": cluster_id,
                    "model": "prophet",
                    "mae": mae_p,
                    "rmse": rmse_p,
                    "mape": mape_p
                })

            except Exception as e:
                print(f"  ⚠ Prophet gagal untuk cluster {cluster_id}: {e}")

        else:
            print("  ⚠ Prophet tidak tersedia, skip Prophet.")

    # SIMPAN METRIKS SEMUA CLUSTER
    metrics_df = pd.DataFrame(metrics_all)
    metric_csv = os.path.join(OUT_CLUSTER, "cluster_demand_metrics.csv")
    metrics_df.to_csv(metric_csv, index=False)

    print("\n💾 Metrics all clusters →", metric_csv)
    print(metrics_df)


if __name__ == "__main__":
    run_cluster_demand()
