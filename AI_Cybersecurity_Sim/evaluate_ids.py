# evaluate_ids.py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
import tensorflow as tf

# Create test set (balanced)
np.random.seed(0)
normal = np.random.normal(loc=0.3, scale=0.08, size=(500,1))
attack = np.random.normal(loc=0.8, scale=0.08, size=(500,1))
X_test = np.vstack((normal, attack)).astype('float32')
y_test = np.hstack((np.zeros(500), np.ones(500)))

# Load TFLite model for inference
interpreter = tf.lite.Interpreter(model_path="ids_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Predict function
def predict_batch(X):
    preds = []
    for x in X:
        arr = x.reshape(1,1).astype('float32')
        interpreter.set_tensor(input_details[0]['index'], arr)
        interpreter.invoke()
        out = interpreter.get_tensor(output_details[0]['index'])[0][0]
        preds.append(out)
    return np.array(preds)

y_scores = predict_batch(X_test)
y_pred = (y_scores >= 0.5).astype(int)

# Metrics
print("Classification report:\n", classification_report(y_test, y_pred, digits=4))
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:\n", cm)

# Plot confusion matrix
plt.figure()
plt.imshow(cm, cmap='Blues')
plt.title("Confusion Matrix")
plt.xticks([0,1], ["Normal","Attack"])
plt.yticks([0,1], ["Normal","Attack"])
for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i,j], ha='center', va='center', color='red')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("confusion_matrix.png")
plt.show()

# ROC curve
fpr, tpr, _ = roc_curve(y_test, y_scores)
roc_auc = auc(fpr,tpr)
plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.4f}")
plt.plot([0,1],[0,1],'--', color='gray')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig("roc_curve.png")
plt.show()
