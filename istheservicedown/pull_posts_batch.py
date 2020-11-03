import pandas as pd
import argparse
import datetime
import tqdm
from listPosts import main as listPostsMain

def get_max_time(filename):
    df = pd.read_csv(filename, delimiter="\t")
    return df["createdAt"].max()

def get_max_timestamp(filename):
    max_time = get_max_time(filename)
    tokens = max_time.split("T")
    year, month, day = tuple(map(int, tokens[0].split("-")))
    hr, minute, sec = tuple(map(int, tokens[1].split(":")))
    return datetime.datetime(year, month, day, hr, minute, sec).timestamp()

def main(start_time, filename):
    if start_time == -1:
        start_time = get_max_timestamp(filename)
    since = start_time
    for i in tqdm.tqdm(range(70)):
        listPostsMain(start_time=since, file_name=filename)
        since = get_max_timestamp(filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', type=int, default=-1)
    parser.add_argument('-f', '--file_name', type=str, default="istheservicedown.tsv")
    args = parser.parse_args()
    main(start_time=args.start, filename=args.file_name)
