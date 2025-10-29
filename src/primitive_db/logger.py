class Logger:
    @staticmethod
    def info(message):
        print(f"[ INFO ] {message}")
    def alarm(message):
        print(f"[ !!! ] {message}")


log = Logger()