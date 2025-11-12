from .engine import RuntimeDB

def main():
    runtime = RuntimeDB()
    runtime.update_db()
    while True:
        runtime.user_prompt()


if __name__ == "__main__":
    main()