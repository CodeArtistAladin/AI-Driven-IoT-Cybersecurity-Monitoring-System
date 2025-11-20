# realtime_ids.py
import time, random, csv, os
import numpy as np
import tensorflow as tf
from datetime import datetime

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="ids_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Where to save alerts
logfile = "ids_alerts.csv"
if not os.path.exists(logfile):
    with open(logfile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "feature", "prediction", "label", "note"])

print("✅ IDS realtime detector ready. Streaming simulated traffic...")

def simulate_feature(attack_prob=0.1):
    # realistic: return a single feature value; attacks are higher values
    if random.random() < attack_prob:
        return round(random.normalvariate(0.8, 0.08), 3), 1  # attack
    else:
        return round(random.normalvariate(0.3, 0.08), 3), 0  # normal

def predict_single(value):
    arr = np.array([[value]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], arr)
    interpreter.invoke()
    out = float(interpreter.get_tensor(output_details[0]['index'])[0][0])
    return out

# Stream loop
try:
    for i in range(200):            # run 200 readings; change as needed
        feature, true_label = simulate_feature(attack_prob=0.15)
        score = predict_single(feature)           # score in [0,1]
        pred = 1 if score >= 0.5 else 0
        t = datetime.now().isoformat(sep=' ', timespec='seconds')

        # Print to console
        status = "ATTACK" if pred==1 else "normal"
        print(f"[{t}] feature={feature:.3f} → score={score:.3f} → {status}")

        # Log alerts (only attacks) and also save all records
        with open(logfile, "a", newline="") as f:
            writer = csv.writer(f)
            note = "ALERT" if pred==1 else ""
            writer.writerow([t, feature, round(score,3), true_label, note])

        # If attack, you can also trigger an action — here we just print extra line
        if pred == 1:
            print(">>> ALERT: Possible intrusion detected! (logged)")

        time.sleep(0.5)     # 0.5 second between readings; change to 1.0 for slower
except KeyboardInterrupt:
    print("\nStopped by user.")
