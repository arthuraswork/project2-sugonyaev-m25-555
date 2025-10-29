from engine import RuntimeDB

def main():
    runtime = RuntimeDB()
    while True:
        runtime.unsafe()


if __name__ == "__main__":
    main()