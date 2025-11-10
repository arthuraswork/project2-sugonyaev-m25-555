class Logger:
    @staticmethod
    def info(message):
        print(f"[ INFO ] {message} [ INFO ]")
    @staticmethod
    def alarm(message):
        print(f"[ !!! ] {message} [ !!! ]")


log = Logger()