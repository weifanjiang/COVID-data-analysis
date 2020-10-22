"""
Sample usage: python3 get_geotag.py -i sample_tweets.txt -o sample_output.csv
"""

import pandas as pd
import requests
import argparse
import os

def get_bearer_token():
    with open("twitter_authentication", "r") as fin:
        lines = fin.readlines()
    return lines[2].split(": ")[1]

def parse_tweet(tweet_str):
    tokens = tweet_str.split(" ")
    ret = dict()
    ret["id"] = tokens[0]
    ret["date"] = tokens[1].rstrip(" ")
    ret["time"] = tokens[2].rstrip(" ")
    ret["timezone"] = tokens[3].rstrip(" ")
    ret["usr_id"] = tokens[4].rstrip(" ")
    ret["text"] = " ".join(tokens[5:]).replace("\n", "")
    return ret

def twitter_status_lookup(unparsed, bearer_token):
    url = "https://api.twitter.com/1.1/statuses/lookup.json"
    parsed = [parse_tweet(x) for x in unparsed]
    id_str = ",".join([x["id"] for x in parsed])

    request_url = url + "?" + "id=" + id_str
    headers = {'Authorization': 'Bearer {}'.format(bearer_token)}
    response = requests.get(request_url, headers=headers)
    res_json = response.json()

    id_to_meta = dict()
    for meta in res_json:
        geo = meta["geo"]
        if geo is not None:
            geo = geo.rstrip(" ")
        id_to_meta[meta["id"]] = {"geo": geo, "usr_location": meta.get("user", dict()).get("location", None)}

    parsed_with_meta = list()
    for i in range(len(parsed)):
        twt = parsed[i]
        twt["id"] = int(twt["id"])
        if twt["id"] in id_to_meta.keys():
            twt["geo"] = id_to_meta[twt["id"]]["geo"]
            twt["usr_location"] = id_to_meta[twt["id"]]["usr_location"]
        parsed_with_meta.append(twt)
    return parsed_with_meta

def main(input_file, output_file, bearer_token):

    LIMIT = 900  # twitter developer API has maximum of 900 queries per 15 min

    if not os.path.isfile(input_file):
        print("invalid file supplied")
        exit(0)

    with open(input_file, "r") as fin:
        unparsed_tweets = fin.readlines()
    if len(unparsed_tweets) > LIMIT:
        print("Twitter API supports {} queries every 15 min".format(LIMIT))
        print("processing first {} tweets only".format(LIMIT))
        unparsed_tweets = unparsed_tweets[:LIMIT]

    if bearer_token == "No token":
        bearer_token = get_bearer_token()

    batch_size = 100  # size of 100 tweets can be retrieved in each request
    parsed_tweets_meta = list()
    idx = 0
    while idx < len(unparsed_tweets):
        start = idx
        end = min(idx + batch_size, len(unparsed_tweets))
        idx = end
        parsed_tweets_meta += twitter_status_lookup(unparsed_tweets[start:end], bearer_token)

    df = pd.DataFrame(parsed_tweets_meta)
    df = df[['id', 'date', 'time', 'timezone', 'geo', 'usr_location', 'text']]
    df.to_csv(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', help='input file of tweets')
    parser.add_argument('-o', '--output_file', help='CSV file of tweets with geolocation metadata')
    parser.add_argument('-b', '--bearer_token', help='bearer_token', default="No token")
    args = parser.parse_args()
    main(args.input_file, args.output_file, args.bearer_token)
