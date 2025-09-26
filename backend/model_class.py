# model_class.py
class LogClassifier:
    def __init__(self):
        self.keywords = ["error", "failed", "exception", "timeout"]

    def predict(self, log_message):
        log_message = log_message.lower()
        for keyword in self.keywords:
            if keyword in log_message:
                return "anomaly"
        return "normal"
