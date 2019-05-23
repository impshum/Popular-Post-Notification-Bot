import configparser
import praw
import datetime
import schedule
from time import sleep


config = configparser.ConfigParser()
config.read('config.ini')
client_id = config.get('REDDIT', 'client_id')
client_secret = config.get('REDDIT', 'client_secret')
reddit_user = config.get('REDDIT', 'reddit_user')
reddit_pass = config.get('REDDIT', 'reddit_pass')
target_sub = config.get('SETTINGS', 'target_sub')
target_user = config.get('SETTINGS', 'target_user')
min_score = config.get('SETTINGS', 'min_score')
run_time = int(config.get('SETTINGS', 'run_time'))
test_mode = int(config.get('TEST_MODE', 'test_mode'))

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='Popular Post Notification Bot (by /u/impshum)',
                     username=reddit_user,
                     password=reddit_pass)


def main():
    posts = []
    today = datetime.datetime.now().strftime('%d/%m/%Y')

    for submission in reddit.subreddit(target_sub).hot(limit=None):
        if not submission.saved:
            score = submission.score
            if score >= int(min_score):
                title = submission.title
                url = submission.url
                permalink = f'https://reddit.com{submission.permalink}'
                ups = submission.ups
                downs = submission.downs
                msg_body = f'[**{title}**]({url})\n\n^Score: ^{score} ^Ups: ^{ups} ^Downs: ^{downs} ^[permalink]({permalink})'
                posts.append(msg_body)

                if not test_mode:
                    submission.save()

    if not test_mode:
        msg_title = f'Popular Posts {today}'
        msg_body = '\n\n'.join(posts)
        reddit.redditor(target_user).message(msg_title, msg_body)

    print(f'{today} - Sent PM with {len(posts)} posts with score over {min_score}')


schedule.every().day.at(f'{run_time}:00').do(main)
print(f'\nWaiting until {run_time}:00 to run\n')

while True:
    schedule.run_pending()
    sleep(1)
