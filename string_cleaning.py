import json
import sys

def main():
    # load the data
    documents_data = None
    with open('data/' + sys.argv[1], 'r') as raw_documents_file:
        documents_data = json.load(raw_documents_file)

    # clean the strings!
    for stock in documents_data:
        for date in documents_data[stock]:
            for comment in documents_data[stock][date]['reddit_data']['comments']:
                string_data = comment['body']
                string_data = string_data.encode("ascii", "ignore").decode()
                string_data = string_data.replace("*", " ")
                string_data = string_data.replace("\n", " ")
                string_data = string_data.replace("\"", " ")
                string_data = ' '.join(string_data.split())
                comment['body'] = string_data

    # write the cleaned data to a new file
    with open('data/cleaned_' + sys.argv[1], 'w+') as cleaned_documents_file:
        json.dump(documents_data, cleaned_documents_file, indent=1)


if __name__ == '__main__':
    main()
