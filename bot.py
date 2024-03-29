import time
import praw
import re
import os
from pprint import pprint

re_ban = re.compile(r'ban', re.IGNORECASE)

r = praw.Reddit(user_agent="BadBallBanBot/0.1 by /u/JJJollyjim")

if not os.path.exists('.password'): open('.password', 'w').close()
if not os.path.exists('.place_holder'): open('.place_holder', 'w').close()

f = open(".password", "r")
password = f.read(100)
f.close()

r.login("bad_ball_ban_bot", password)

subreddit = r.get_subreddit("BadBallBanBot")

def set_place_holder(new_ph):
	f = open(".place_holder", "w")
	f.write(new_ph)
	f.close()

def get_place_holder():
	f = open(".place_holder", "r")
	ph = f.read(16)
	f.close()
	return ph

print("    - Current placeholder: {0}".format(get_place_holder()))

def handle_ratelimit(func, *args, **kwargs):
	while True:
		try: return func(*args, **kwargs)
		except praw.errors.RateLimitExceeded as error:
			print '    - Sleeping for %d seconds due for rate limiting' % error.sleep_time
			time.sleep(error.sleep_time)

while True:
	if get_place_holder() != "":
		posts = list(subreddit.get_new(place_holder=get_place_holder()))
	else:
		posts = list(subreddit.get_new())

	posts.pop()

	for post in reversed(posts):
		# Decide if the post is a ban appeal
		is_ban_appeal = re.search(re_ban, post.title) and post.is_self

		if is_ban_appeal:
			# Make sure we haven't already posted on it
			
			found_bbbb = False

			for c in post.comments:
				if str(c.author) == "bad_ball_ban_bot":
					found_bbbb = True
					break

			if found_bbbb:
				print("BBBB| {0}".format(post.title.encode('unicode-escape')))
				set_place_holder(post.id)
				break

			print("BAN | {0}".format(post.title.encode('unicode-escape')))

			# Comment on the post
			comment = handle_ratelimit(post.add_comment, ("Hi there!\n\n"
				"This bot has detected that you have posted a ban appeal. \n\n"
				"If this is correct, here are a few things you should know: \n\n"
				"* You have to be reported by 8 separate people within 24 hours to get banned, meaning you definitely did *something* wrong \n"
				"* Trolls succeeding in getting someone banned is __*very* rare__ \n"
				"* Bans are only temporary. The first one lasts 1 hour, with 4 hours added for each subsequent ban (1, 5, 9, etc...) \n"
				"* Here are the reasons people may have reported you, along with some helpful suggestions:\n"
				"    - Offensive or spammy chat: don't be mean to the other team or your teammates \n"
				"    - Offensive username: visit your profile page and change your name away from \"NiggerFagBall\" \n"
				"    - AFK too much: close the game if you need to do something IRL \n"
				"    - Working against own team: if you make a mistake which hurts your team, say 'sorry' or 'mb' (stands for 'my bad') in team chat. \n"
				"* Bans are based on IP addresses, meaning that if somebody at your school, house, or workplace gets banned then everyone else there will too \n\n"
				"--- \n\n"
				"Don't like words? [Here's a friendly infographic!](http://i.imgur.com/EgZ24UK.png) \n\n"
				"--- \n\n"
				"__Note:__ this bot is in beta. It may have decided that this post is a ban appeal by mistake. If so, please downvote this comment.\n\n"
				"Click [here](http://www.reddit.com/message/compose/?to=JJJollyjim) to message the developer \n\n"
			))
			
			print("    - Comment succeeded!")
		else:
			print("    | {0}".format(post.title.encode('unicode-escape')))

		set_place_holder(post.id)
	
	time.sleep(5)
