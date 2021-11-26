import praw
import pandas as pd

#praw documentation: https://praw.readthedocs.io/en/latest/index.html
#create Reddit instance to access Reddit API

def main(args):
    limit_subreddit=args.limit_subreddit
    limit_submissions=args.limit_submissions
    print("limit_subreddit: "+str(limit_subreddit),"\nlimit_submissions: "+str(limit_submissions))
    reddit = praw.Reddit(
    client_id='3bBUkQkkkTRq1fLuWXGb3g',
    client_secret='Dr48sSaUGS5SA7ksaLrBNR6MN5I2wQ',
    user_agent='Scraper',
    username='reddit_User_410',
    password='CS410rocks')

    subreddits = []
    submissions = []
    all_submissions = []

    for subreddit in reddit.subreddits.popular(limit=limit_subreddit):
        #print(subreddit.display_name)
        for submission in subreddit.hot(limit=limit_submissions):
            submissions.append(submission.title + submission.selftext)
            subreddits.append(subreddit.display_name)

    output_subreddits=pd.DataFrame({'Subreddit': list(set(subreddits))})
    output_subreddits.to_csv('output-subreddits.csv',index=False)

    output_submissions=pd.DataFrame({'Subreddit': subreddits,'Submissions':submissions})
    output_submissions.to_csv('output-submissions.csv',index=False)

    print(output_submissions)

    def to_xml(df):
        def row_xml(row):
            xml = ['<item>']
            for i, col_name in enumerate(row.index):
                xml.append('  <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
            xml.append('</item>')
            return '\n'.join(xml)
        res = '\n'.join(df.apply(row_xml, axis=1))
        return(res)

    with open('output-submissions.xml', 'w',encoding="utf-8") as f:
        f.write(to_xml(output_submissions))

    print("\nFiles generated: \n output-submissions.csv \n output-submissions.xml \n output-subreddits.csv")

if __name__ =='__main__':
    import argparse
    # Create the parser
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-l1','--limit_subreddit',type=int,default=10)
    my_parser.add_argument('-l2','--limit_submissions',type=int,default=10)
    args = my_parser.parse_args()
    main(args)





