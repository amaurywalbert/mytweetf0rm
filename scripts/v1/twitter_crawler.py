#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	This script automate the crawling of users, and their twitter, retweets, favorites, mentions and timeline. 
	It starts with a list of seed users, and crawl 3-layers (friends of a seed user are on the first level; and friends of the friends are on the second level)
	It's input is the:
		apikeys:
		config: config of the seed users as well as the config file for tracking the progress, if it's non-exist; it will start from the beginning and save its progress to this file
		output: the output folder of each run;

	The system can also generate a snapshot of the current progress if exceptions happens, and the system can resume from the config file (json) 
'''

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

import argparse, pickle, os, json, sys, multiprocessing, time, shutil

sys.path.append("..")
from tweetf0rmer.user_farm import UserFarm

MAX_QUEUE_SIZE = 32767 # On mac... 
MAX_RETRY = 10
RETRY_SLEEP = 60

def farm_user_timelines(apikeys, user_timeline_queue, output_folder='./farm/'):

	timelines_output_folder = os.path.abspath('%s/timelines/'%(output_folder)) # by user id

	user_timelines_farmer = UserFarm(apikeys=apikeys, verbose=False, output_folder=timelines_output_folder)

	current_user_id = 0

	retry = False

	problem_queue = []

	while current_user_id != -1:
		time.sleep(10)
		if retry and retry_cnt > 0:
			time.sleep(RETRY_SLEEP)
			user_timelines_farmer.write_to_handler.delete(current_user_id)
			retury = False
			retry_cnt -= 1
		else:
			current_user_id = user_timeline_queue.get(True) # will block and wait for the next user_id
			#logger.info("timeline queue size: %d"%(user_timeline_queue.qsize())) no qsize() function on mac os x
			if current_user_id == -1:
				if len(problem_queue) > 0: #have issues with a few user_id, we try to add them back to the queue to retry
					# add this point, the queue should be empty; so no need to worry about block on the put
					for uid in problem_queue:
						user_timeline_queue.put(uid, block=True)

					# get one to continue the process
					current_user_id = user_timeline_queue.get(True)
				else:
					break#continue

			logger.info('retrieving timeline for: %d'%(current_user_id))
			retry_cnt = MAX_RETRY

		try:
			if not os.path.exists(os.path.abspath('%s/%s'%(timelines_output_folder, current_user_id))):
				user_timelines_farmer.user_timeline(current_user_id)

		except:
			logger.warn("exception; retry: %d"%(retry_cnt))
			retry = True
			# note the problem, but don't die; move onto the next; and push this to the back of the current queue
			user_timeline_queue.put(user_id, block=True)
		finally:
			user_timelines_farmer.close()
			

	# notify -1
	user_timelines_farmer.close()

	return True

##########################################################################################################################################################################
def farm_user_retweets(apikeys, user_retweets_queue, output_folder='./farm/'):

	retweets_output_folder = os.path.abspath('%s/retweets/'%(output_folder)) # by user id

	user_retweets_farmer = UserFarm(apikeys=apikeys, verbose=False, output_folder=retweets_output_folder)

	current_user_id = 0

	retry = False

	problem_queue = []

	while current_user_id != -1:
		time.sleep(10)
		if retry and retry_cnt > 0:
			time.sleep(RETRY_SLEEP)
			user_retweets_farmer.write_to_handler.delete(current_user_id)
			retury = False
			retry_cnt -= 1
		else:
			current_user_id = user_retweets_queue.get(True) # will block and wait for the next user_id
			#logger.info("retweets queue size: %d"%(user_retweets_queue.qsize())) no qsize() function on mac os x
			if current_user_id == -1:
				if len(problem_queue) > 0: #have issues with a few user_id, we try to add them back to the queue to retry
					# add this point, the queue should be empty; so no need to worry about block on the put
					for uid in problem_queue:
						user_retweets_queue.put(uid, block=True)

					# get one to continue the process
					current_user_id = user_retweets_queue.get(True)
				else:
					break#continue

			logger.info('retrieving retweets for: %d'%(current_user_id))
			retry_cnt = MAX_RETRY

		try:
			if not os.path.exists(os.path.abspath('%s/%s'%(retweets_output_folder, current_user_id))):
				user_retweets_farmer.user_retweets(current_user_id)

		except:
			logger.warn("exception; retry: %d"%(retry_cnt))
			retry = True
			# note the problem, but don't die; move onto the next; and push this to the back of the current queue
			user_retweets_queue.put(user_id, block=True)
		finally:
			user_retweets_farmer.close()
			

	# notify -1
	user_retweets_farmer.close()

	return True
	
##########################################################################################################################################################################
##########################################################################################################################################################################
def farm_user_favorites(apikeys, user_favorites_queue, output_folder='./farm/'):

	favorites_output_folder = os.path.abspath('%s/favorites/'%(output_folder)) # by user id

	user_favorites_farmer = UserFarm(apikeys=apikeys, verbose=False, output_folder=favorites_output_folder)

	current_user_id = 0

	retry = False

	problem_queue = []

	while current_user_id != -1:
		time.sleep(10)
		if retry and retry_cnt > 0:
			time.sleep(RETRY_SLEEP)
			user_favorites_farmer.write_to_handler.delete(current_user_id)
			retury = False
			retry_cnt -= 1
		else:
			current_user_id = user_favorites_queue.get(True) # will block and wait for the next user_id
			#logger.info("favorites queue size: %d"%(user_favorites_queue.qsize())) no qsize() function on mac os x
			if current_user_id == -1:
				if len(problem_queue) > 0: #have issues with a few user_id, we try to add them back to the queue to retry
					# add this point, the queue should be empty; so no need to worry about block on the put
					for uid in problem_queue:
						user_favorites_queue.put(uid, block=True)

					# get one to continue the process
					current_user_id = user_favorites_queue.get(True)
				else:
					break#continue

			logger.info('retrieving favorites for: %d'%(current_user_id))
			retry_cnt = MAX_RETRY

		try:
			if not os.path.exists(os.path.abspath('%s/%s'%(favorites_output_folder, current_user_id))):
				user_favorites_farmer.user_favorites(current_user_id)

		except:
			logger.warn("exception; retry: %d"%(retry_cnt))
			retry = True
			# note the problem, but don't die; move onto the next; and push this to the back of the current queue
			user_favorites_queue.put(user_id, block=True)
		finally:
			user_favorites_farmer.close()
			

	# notify -1
	user_favorites_farmer.close()

	return True
##########################################################################################################################################################################
##########################################################################################################################################################################
def farm_user_mentions(apikeys, user_mentions_queue, output_folder='./farm/'):

	mentions_output_folder = os.path.abspath('%s/mentions/'%(output_folder)) # by user id

	user_mentions_farmer = UserFarm(apikeys=apikeys, verbose=False, output_folder=mentions_output_folder)

	current_user_id = 0

	retry = False

	problem_queue = []

	while current_user_id != -1:
		time.sleep(10)
		if retry and retry_cnt > 0:
			time.sleep(RETRY_SLEEP)
			user_mentions_farmer.write_to_handler.delete(current_user_id)
			retury = False
			retry_cnt -= 1
		else:
			current_user_id = user_mentions_queue.get(True) # will block and wait for the next user_id
			#logger.info("mentions queue size: %d"%(user_mentions_queue.qsize())) no qsize() function on mac os x
			if current_user_id == -1:
				if len(problem_queue) > 0: #have issues with a few user_id, we try to add them back to the queue to retry
					# add this point, the queue should be empty; so no need to worry about block on the put
					for uid in problem_queue:
						user_mentions_queue.put(uid, block=True)

					# get one to continue the process
					current_user_id = user_mentions_queue.get(True)
				else:
					break#continue

			logger.info('retrieving mentions for: %d'%(current_user_id))
			retry_cnt = MAX_RETRY

		try:
			if not os.path.exists(os.path.abspath('%s/%s'%(mentions_output_folder, current_user_id))):
				user_mentions_farmer.user_mentions(current_user_id)

		except:
			logger.warn("exception; retry: %d"%(retry_cnt))
			retry = True
			# note the problem, but don't die; move onto the next; and push this to the back of the current queue
			user_mentions_queue.put(user_id, block=True)
		finally:
			user_mentions_farmer.close()
			

	# notify -1
	user_mentions_farmer.close()

	return True
##########################################################################################################################################################################

def farm_user_network(apikeys, config = {}, output_folder='./farm/', network_type="followers"):

	network_output_folder = os.path.abspath('%s/%s/'%(output_folder, network_type)) # by user id

	shutil.rmtree(network_output_folder, True)

	user_network_farmer = UserFarm(apikeys=apikeys, verbose=False, output_folder=network_output_folder)
	
	seeds = config['seeds'] if 'seeds' in config else []
	depth = int(config.get('depth', 3)) # by default only fetch 3 layers

	#progress = config.get('progress', {})

	#current_depth = progress.get('current_depth', 0) # start from the first layer
	#queue = progess.get('queue', {})
	#queue = queue if type(queue) is dict else raise Exception("the queue must be a dict, see twitter_crawler_config.json as an example")

	user_timeline_queue = multiprocessing.Queue(maxsize=MAX_QUEUE_SIZE)
	p = multiprocessing.Process(target=farm_user_timelines, args=(apikeys, user_timeline_queue, output_folder))
	p.start()
	
	user_favorites_queue = multiprocessing.Queue(maxsize=MAX_QUEUE_SIZE)
	q = multiprocessing.Process(target=farm_user_favorites, args=(apikeys, user_favorites_queue, output_folder))
	q.start()
	
	user_retweets_queue = multiprocessing.Queue(maxsize=MAX_QUEUE_SIZE)
	r = multiprocessing.Process(target=farm_user_retweets, args=(apikeys, user_retweets_queue, output_folder))
	r.start()	
	
	user_mentions_queue = multiprocessing.Queue(maxsize=MAX_QUEUE_SIZE)
	s = multiprocessing.Process(target=farm_user_mentions, args=(apikeys, user_mentions_queue, output_folder))
	s.start()
		
	# get user_ids for the seeds
	user_network_queue = user_network_farmer.get_user_ids(seeds)

	try:
		#get user id first 
		while depth > 0 and len(user_network_queue) > 0:
			temp_user_network_queue = set()

			for user_id in user_network_queue:
				time.sleep(5)
				if network_type == 'friends':
					f_ids = user_network_farmer.find_all_friends(user_id)
				else:
					f_ids = user_network_farmer.find_all_followers(user_id)

				logger.info('user_id: %d has %d friends'%(user_id, len(f_ids)))

				for f_id in f_ids:
#					user_timeline_queue.put(f_id, block=True)							# AVALIAR - Me parece que se eu habilitar ele pega os amigos e a timeline dos amigos... Não é o nosso caso.
#					user_favorites_queue.put(f_id, block=True)						# AVALIAR - Me parece que se eu habilitar ele pega os amigos e os favoritos dos amigos.... Não é o nosso caso.
#					user_retweets_queue.put(f_id, block=True)						# AVALIAR - Me parece que se eu habilitar ele pega os amigos e os retweets dos amigos.... Não é o nosso caso.
#					user_mentions_queue.put(f_id, block=True)						# AVALIAR - Me parece que se eu habilitar ele pega os amigos e os menções dos amigos.... Não é o nosso caso.
					temp_user_network_queue.add(f_id)
					user_network_farmer.close() # force flush once 

			logger.info('finish depth: %d'%(depth))

			depth -= 1
	 		user_network_queue = temp_user_network_queue

	except KeyboardInterrupt:
		print()
		logger.error('You pressed Ctrl+C!')
		raise
	except:		
		raise
	finally:
		user_network_farmer.close()

	user_timeline_queue.put_nowait(-1)
	user_favorites_queue.put_nowait(-1)
	user_retweets_queue.put_nowait(-1)
	user_mentions_queue.put_nowait(-1)

	p.join()
	q.join()
	r.join()
	s.join()

	logger.info('all done')

if __name__=="__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-a', '--apikeys', help="config file for twitter api keys (json format); twitter requires you to have an account to crawl;", required = True)
	parser.add_argument('-c', '--crawler', help="the crawler identifier; you can have multiple crawler accounts set in the apikeys.json; pick one", required = True)
	parser.add_argument('-s', '--seeds', help="the config file for defining seed users and depth; see twitter_crawler.json as an example", required = True)
	parser.add_argument('-o', '--output', help="define the location of the output", required = True)
	parser.add_argument('-nt', '--network_type', help="crawling [friends] or [followers]", default = 'followers')

	args = parser.parse_args()
	
	with open(os.path.abspath(args.apikeys), 'rb') as apikeys_f, open(os.path.abspath(args.seeds), 'rb') as config_f:
		import json, os
		apikeys_config = json.load(apikeys_f)
		apikeys = apikeys_config.get(args.crawler, None)
		
		config = json.load(config_f)
		
		farm_user_network(apikeys, config, args.output, args.network_type)
			


