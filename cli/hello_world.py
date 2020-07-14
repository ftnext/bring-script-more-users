from argparse import ArgumentParser


if __name__ == "__main__":
    # enable to take arguments from the command line
    parser = ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()

    print(f"Hello, {args.name}")
