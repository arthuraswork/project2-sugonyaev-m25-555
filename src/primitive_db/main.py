from .engine import RuntimeDB

def main():
    runtime = RuntimeDB()
    runtime.update_db()
    while True:
        runtime.unsafe()


if __name__ == "__main__":
    main()