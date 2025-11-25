import pandas as pd

df = pd.read_csv("ncr_ride_bookings.csv")

order_count = df.groupby("Customer ID")["Booking ID"].count()
multi_order_customers = order_count[order_count >= 2]

total_customers = len(order_count)
multi_pct = len(multi_order_customers) / total_customers * 100

print(f"Persentase customer yg order >= 2: {multi_pct:.2f}%")
