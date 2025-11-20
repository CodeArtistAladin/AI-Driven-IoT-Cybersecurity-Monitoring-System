import tensorflow as tf

# Check TensorFlow version
print("TensorFlow version:", tf.__version__)

# Try to access TFLite converter
try:
    converter = tf.lite.TFLiteConverter.from_concrete_functions
    print("✅ TensorFlow Lite module is available!")
except Exception as e:
    print("❌ TensorFlow Lite module not available:", e)
