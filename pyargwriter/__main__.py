from pyargwriter.main import main


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as e:
        print(f"Process could not be finished due to a NotImplementedError: {e}")
