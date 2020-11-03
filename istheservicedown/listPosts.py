import argparse
import requests
import os


def main(start_time, file_name):
    url = "https://disqus.com/api/3.0/forums/listPosts.json"
    forum_name = "istheservicedown"
    api_key = "X7B84G87DeFZOGfhWOc9TgkUt7wkkbLPuzXdDTj7CaNqkr3pb1u2RnK8xvL0SPfR"
    limit = 100
    order = "asc"
    since = start_time

    response = requests.get("{}?forum={}&api_key={}&limit={}&order={}&since={}".format(
        url,
        forum_name,
        api_key,
        limit,
        order,
        since
    ))
    response_json = response.json()

    if os.path.isfile(file_name):
        fout = open(file_name, "a+")
    else:
        fout = open(file_name, "w")
        fout.write('id\tcreatedAt\tusername\tforum\traw_message\n')

    for resp in response_json["response"]:
        fout.write("{}\t{}\t{}\t{}\t{}\n".format(
            resp["id"], resp["createdAt"], resp["author"].get("username", None), resp["forum"] ,resp["raw_message"].replace("\n", "")
        ))
    fout.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_time', type=int, default=1577836800)
    parser.add_argument('-f', '--file_name', type=str, default="istheservicedown.tsv")
    args = parser.parse_args()
    main(start_time=args.start_time, file_name=args.file_name)
