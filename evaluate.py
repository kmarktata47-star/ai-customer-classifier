import time
import pandas as pd
from classifier import classify

df = pd.read_csv("test_data.csv")


def classify_with_retry(message, tries=3):
    for attempt in range(tries):
        try:
            return classify(message)
        except Exception as e:
            print("   error:", e)
            time.sleep(20)
    return None


pred_categories = []
pred_urgencies = []
pred_reasons = []

for i, row in df.iterrows():
    result = classify_with_retry(row["message"])
    if result is None:
        pred_categories.append("ERROR")
        pred_urgencies.append("ERROR")
        pred_reasons.append("")
    else:
        pred_categories.append(result.category)
        pred_urgencies.append(result.urgency)
        pred_reasons.append(result.reason)
    print(f"Done {i + 1}/{len(df)}")
    time.sleep(7)

df["predicted_category"] = pred_categories
df["predicted_urgency"] = pred_urgencies
df["reason"] = pred_reasons

df["category_correct"] = df["expected_category"] == df["predicted_category"]
df["urgency_correct"] = df["expected_urgency"] == df["predicted_urgency"]

print()
print("Category accuracy:", round(df["category_correct"].mean() * 100, 1), "%")
print("Urgency accuracy: ", round(df["urgency_correct"].mean() * 100, 1), "%")

mistakes = df[~(df["category_correct"] & df["urgency_correct"])]
print()
print("Mistakes:", len(mistakes), "of", len(df))
for _, row in mistakes.iterrows():
    print("-" * 60)
    print("Message: ", row["message"])
    print("Expected:", row["expected_category"], "/", row["expected_urgency"])
    print("AI said: ", row["predicted_category"], "/", row["predicted_urgency"])
    print("Reason:  ", row["reason"])

df.to_csv("results.csv", index=False)
print()
print("Saved full results to results.csv")