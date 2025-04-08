class Diagnostics:
    @staticmethod
    def note(message):
        print(f"[NOTE] {message}")

    @staticmethod
    def warning(message):
        print(f"[WARNING] {message}")

    @staticmethod
    def error(message):
        print(f"[ERROR] {message}")

    @staticmethod
    def debug(message):
        # Optionally, enable via environment or config
        print(f"[DEBUG] {message}")

    @staticmethod
    def success(message):
        print(f"[SUCCESS] {message}")
