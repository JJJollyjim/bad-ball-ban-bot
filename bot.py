import time
import praw
import re
from pprint import pprint

re_ban = re.compile(r'ban', re.IGNORECASE)

r = praw.Reddit(user_agent="BadBallBanBot/0.1 by /u/JJJollyjim")

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

print("Current placeholder: {0}".format(get_place_holder()))

def handle_ratelimit(func, *args, **kwargs):
	while True:
		try:
			func(*args, **kwargs)
			print("Comment succeeded!")
			break
		except praw.errors.RateLimitExceeded as error:
			print 'Sleeping for %d seconds due for rate limiting' % error.sleep_time
			time.sleep(error.sleep_time)

while True:
	posts_gen = subreddit.get_new(place_holder=get_place_holder())
	posts = [post for post in posts_gen]

	# print([post.title for post in posts])

	posts.pop()

	for post in reversed(posts):
		# Decide if the post is a ban appeal
		is_ban_appeal = re.search(re_ban, post.title) and post.is_self

		if is_ban_appeal:
			print("BAN | {0}".format(post.title))
			handle_ratelimit(post.add_comment, ("Hi there, {0}!\n\n"
				"This bot has detected that you have posted a ban appeal. \n\n"
				"If this is correct, here are a few things you should know: \n\n"
				"* You have to be reported by 8 seperate people within 24 hours to get banned, meaning you definitely did *something* wrong \n"
				"* Trolls succeeding in getting someone banned is __*very* rare__ \n"
				"* Bans are only temporary. The first one lasts 1 hour, with 4 hours added for each subsequent ban (1, 5, 9, etc...) \n"
				"* Here are the reasons people may have reported you, along with some helpful suggestions:\n"
				"    - Offensive or spammy chat: don't be mean to the other team or your teammates \n"
				"    - Offensive username: visit your profile page and change your name away from \"NiggerFagBall\" \n"
				"    - AFK too much: close the game if you need to do something IRL \n"
				"    - Working against own team: if you make a mistake which hurts your team, say sorry in team chat. Otherwise it's hard to tell what is intentional \n"
				"* Bans are based on IP addresses, meaning that if somebody at your school, house, or workplace gets banned then everyone else there will too \n\n"
				"--- \n\n"
				"Don't like words? [Here's a friendly infographic!](http://i.imgur.com/EgZ24UK.png) \n\n"
				"--- \n\n"
				"__Note:__ this bot is in beta. It may have decided that this post is a ban appeal by mistake. If so, please downvote this comment.\n\n"
				"Click [here](http://www.reddit.com/message/compose/?to=JJJollyjim) to message the developer \n\n"
			).format(post.author))
		else:
			print("    | {0}".format(post.title))

		set_place_holder(post.id)
	
	time.sleep(5)