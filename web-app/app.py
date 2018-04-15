from flask import Flask, render_template, request
import pandas as pd
from flask import abort
from pymongo import MongoClient
from collections import defaultdict
from datetime import datetime
from related_words import get_top_related_words
from nGram import nGram
from os import listdir, makedirs
from os.path import isfile, join, exists
import time
import json
import math
import operator
import random
import numpy as np

app = Flask(__name__)

client = MongoClient('127.0.0.1', 27017)
db = client.influencers_db

from plots import *


def human_format(num):
	try:
		magnitude = 0
		while abs(float(num)) >= 1000:
			magnitude += 1
			num /= 1000.0
		# add more suffixes if you need them
	except:
		return ''

	return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

@app.route('/influencers/about/')
def about_page():
	return render_template('about.html')


@app.route('/influencers/start/')
def start_page():
	return render_template('start_page.html')


@app.route('/influencers/categories/')
def categories_page():
	category_data = dict()
	cursor = db.influencers_list_collection.find()
	df = pd.DataFrame(list(cursor))
	categories = df['category'].unique()
	for category in categories:
		df_handles = df[['tw_handle', 'category']]
		df_cat = df_handles.loc[df_handles['category'] == category]
		result_list = list()
		for index, row in df_cat.iterrows():
			tw_handle = row['tw_handle']
			doc = db.combined_collection.find_one({'tw_handle': tw_handle})
			# print(tw_handle, type(doc))
			infl_dict = dict()
			infl_dict['tw_handle'] = tw_handle
			infl_dict['category'] = category
			infl_dict['tw_description'] = doc['tw_description']
			infl_dict['ig_thumbnail_url'] = doc['ig_thumbnail_url']
			result_list.append(infl_dict)
		category_data[category] = result_list
	return render_template('categories_page.html', category_data=category_data)
	# categories = categories)


@app.route('/influencers/all/')
def all_influencers_page():
	all_influencers = db.combined_collection.find()
	infls = db.combined_collection.find()
	category = dict()

	for influencer in infls:
		tw_handle = influencer['tw_handle']
		all_inf_data = db.influencers_list_collection.find_one(
			{'tw_handle': tw_handle})
		category[tw_handle] = all_inf_data['category']
	# print(category)
	# print(all_influencers)

	return render_template('all_influencers_page.html',
						   all_influencers=all_influencers, category=category)


def get_by_hod(df, col, timestamp):
	given_time = df[timestamp]
	reqd_hour = list()
	for gtime in given_time:
		gtime = int(gtime)
		hr = datetime.fromtimestamp(gtime).hour
		reqd_hour.append(hr)

	df['formatted_time'] = reqd_hour
	grouped = df.groupby('formatted_time').count()
	return grouped.index, grouped[col]


def tw_get_by_hod(df, col, timestamp):
	given_time = df[timestamp]
	reqd_hour = list()
	for gtime in given_time:
		gtime = int(gtime.to_pydatetime().strftime('%s'))
		hr = datetime.fromtimestamp(gtime).hour
		reqd_hour.append(hr)

	df['formatted_time'] = reqd_hour
	grouped = df.groupby('formatted_time').count()
	return grouped.index, grouped[col]


def yt_get_by_hod(df, col, timestamp):
	given_time = df[timestamp]
	reqd_hour = list()
	for gtime in given_time:
		gtime = int(datetime.strptime(
			gtime, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%s'))
		hr = datetime.fromtimestamp(gtime).hour
		reqd_hour.append(hr)

	df['formatted_time'] = reqd_hour
	grouped = df.groupby('formatted_time').count()
	return grouped.index, grouped[col]


def fb_get_by_hod(df, col, timestamp):
	given_time = df[timestamp]
	reqd_hour = list()
	for gtime in given_time:
		gtime = int(datetime.strptime(
			gtime, '%Y-%m-%dT%H:%M:%S+%f').strftime('%s'))
		hr = datetime.fromtimestamp(gtime).hour
		reqd_hour.append(hr)

	df['formatted_time'] = reqd_hour
	grouped = df.groupby('formatted_time').count()
	return grouped.index, grouped[col]


def with_day_of_month(df, timestamp):
	given_time = df[timestamp]
	reqd_day = list()
	for gtime in given_time:
		gtime = int(gtime)
		d = datetime.fromtimestamp(gtime).day
		reqd_day.append(d)

	df['day_of_month'] = reqd_day
	return df


def with_month(df, timestamp):
	given_time = df[timestamp]
	reqd_month = list()
	for gtime in given_time:
		gtime = int(gtime)
		d = datetime.fromtimestamp(gtime).strftime('%b')
		reqd_month.append(d)

	df['month'] = reqd_month
	return df

@app.route('/review/', methods=['GET', 'POST'])
def review_page():
	if request.method == 'POST':
		tw_handle = request.form['tw_handle']
		rating = request.form['rating']
		review = request.form['review']
		result = rating + ' ' + review + ' ' + tw_handle
		collection = db.review_collection
		record = {'tw_handle': tw_handle, 'rating': rating, 'review': review}
		collection.insert_one(record)
		return render_template('review_result_page.html', disp=1)
	else:
		return render_template('review_result_page.html', disp=None)



@app.route('/influencers/search/', methods=['GET', 'POST'])
def search_page():
	if request.method == 'POST':

		search_results = list()

		product = request.form['product']
		category = request.form['category']
		num_top = 5

		related = get_top_related_words(product, num_top)
		related.append(product)
		all_inf_data = db.influencers_list_collection.find(
			{'category': category})

		ng_probabilities = dict()

		for inf_data in all_inf_data:
			tw_handle = inf_data['tw_handle']
			path = 'static/combined-data-4-sources/{}/part-00000'.format(
				tw_handle)
			if not exists(path):
				continue
			ng = nGram(n=2, corpus_file=path, cache=False)
			sum_proba = 0
			for rel in related:
				ng_proba = ng.sentence_probability(
					sentence=rel, n=1, form='antilog')
				sum_proba += ng_proba
				print('{}: {}'.format(tw_handle, sum_proba))
			ng_probabilities[tw_handle] = sum_proba

		sorted_ng_probabilities = sorted(
			ng_probabilities.items(), key=operator.itemgetter(1), reverse=True)

		rifl_document = db.rightfluencer_collection.find()
		rank_dict = dict()
		for rifl_doc in rifl_document:
			h = rifl_doc['tw_handle']
			r = rifl_doc['rf_rank']
			rank_dict[h] = r

		dict_sorted_ng_probabilities = dict(sorted_ng_probabilities)

		for key, value in dict_sorted_ng_probabilities.items():
			search_result = {}
			tw_handle = key
			influencer_document = db.combined_collection.find_one(
				{'tw_handle': tw_handle})
			search_result['tw_name'] = influencer_document['tw_name']
			search_result['tw_handle'] = tw_handle
			search_result['ig_thumbnail_url'] = influencer_document[
				'ig_thumbnail_url']
			search_result['probabilities'] = value
			search_result['score'] = 0
			search_results.append(search_result)
			if len(search_results) == 5:
				break

		return render_template('search_page.html', product=product, category=category,
							   sorted_ng_probabilities=sorted_ng_probabilities[
								   :5], related=related[::-1],
							   search_results=search_results, rank_dict=rank_dict, disp=1)
	else:
		return render_template('search_page.html', disp=None)


@app.route('/influencers/')
def influencer_page():
	data_sources = ['Twitter', 'Instagram', 'YouTube', 'Facebook']
	data_sources_colors = ['#1da1f280', '#8a3ab980', '#cc181e80', '#3b599880']
	tw_handle = request.args.get('tw_handle')
	influencer_document = db.combined_collection.find_one(
		{'tw_handle': tw_handle})
	insta_fol_document = db.instagram_followers_collection.find_one(
		{'twitter': tw_handle})
	all_inf_data = db.influencers_list_collection.find_one(
		{'tw_handle': tw_handle})
	rank_document = db.rightfluencer_collection.find_one(
		{'tw_handle': tw_handle})
	ig_posts_document = db.instagram_posts_collection.find_one(
		{'tw_handle': tw_handle})

	twitter_url = all_inf_data['twitter_url']
	instagram_url = all_inf_data['instagram_url']
	youtube_url = all_inf_data['youtube_url']
	facebook_url = all_inf_data['facebook_url']

	tw_description = influencer_document['tw_description']
	yt_subscriber_count = human_format(
		influencer_document['yt_subscriber_count'])
	tw_followers_count = human_format(
		influencer_document['tw_followers_count'])
	try:
		ig_followers = human_format(int(insta_fol_document['follower']))
		ig_followers_count = int(insta_fol_document['follower'])
	except Exception as e:
		ig_followers_count = 0
		ig_followers = 'NA'

	fb_page_likes = human_format(influencer_document['fb_page_likes'])
	tw_location = influencer_document['tw_location']
	kl_score = influencer_document['kl_score']
	# if tw_location == '':
	# 	tw_location = influencer_document['fb_location']
	fb_category = all_inf_data['category']
	tw_name = influencer_document['tw_name']
	ig_thumbnail_url = influencer_document['ig_thumbnail_url']
	print(ig_thumbnail_url)

	# Plot 1
	plot_1_y = [influencer_document['tw_followers_count'], ig_followers_count,
				influencer_document['yt_subscriber_count'], influencer_document['fb_page_likes']]
	plot_1_x = data_sources
	plot_1_div = bar_plot(x_list=plot_1_x, y_list=plot_1_y, barcolors=data_sources_colors,
						  vertical=True, title='Followers count in various social media platforms', showYAxis=True, showYticklabels=True)
	# Plot 2
	tw_posts = influencer_document['tw_statuses_count']
	ig_posts = ig_posts_document['ig_posts']
	yt_posts = influencer_document['yt_video_count']
	plot_2_x = data_sources[0:3]
	plot_2_y = [tw_posts, ig_posts, yt_posts]
	plot_2_div = bar_plot(x_list=plot_2_y, y_list=plot_2_x, barcolors=data_sources_colors,
						  title='Number of posts across platforms', showYAxis=True, showYticklabels=True,
						  vertical=False)

	# Plot 3
	# PARSE TO INT : db.youtube_collection.find().forEach( function (x)
	# {x.likes = parseInt(x.likes); db.youtube_collection.save(x);})
	try:
		ig_avg_likes = db.instagram_collection.aggregate([{'$match': {'twitter_handle': {'$eq': tw_handle}}}, {
			'$group': {'_id': '$twitter_handle', 'average': {'$avg': '$likes'}}}])
		ig_avg_likes = list(ig_avg_likes)[0]['average']
	except:
		ig_avg_likes = 0

	screen_name = influencer_document['tw_screen_name']
	tw_avg_likes = db.twitter_collection.aggregate([{'$match': {'screen_name': {'$eq': screen_name}}}, {
		'$group': {'_id': '$screen_name', 'average': {'$avg': '$favorites'}}}])
	tw_avg_likes = list(tw_avg_likes)[0]['average']

	try:
		yt_avg_likes = db.youtube_collection.aggregate([{'$match': {'twitter_handle': {'$eq': tw_handle}}}, {
			'$group': {'_id': '$twitter_handle', 'average': {'$avg': '$likes'}}}])
		yt_avg_likes = list(yt_avg_likes)[0]['average']
		plot_3_x = data_sources[0:3]
		plot_3_y = [tw_avg_likes, ig_avg_likes, yt_avg_likes]
		colors = data_sources_colors[0:3]
	except IndexError:
		plot_3_x = data_sources[0:2]
		plot_3_y = [tw_avg_likes, ig_avg_likes]
		colors = data_sources_colors[0:3]
	plot_3_radius = [item**(1. / 2.5) for item in plot_3_y]
	hver_label = plot_3_x

	plot_3_div = bubble_plot(x_list=plot_3_x, radius=plot_3_radius, bubblecolors=colors, title='Avg popularity across platforms',
							 hover_labels=plot_3_y	)

	# Plot 4
	plot_4_x = list()
	plot_4_y = list()
	plot_4_colors = list()
	try:
		ig_avg_comments = db.instagram_collection.aggregate([{'$match': {'twitter_handle': {'$eq': tw_handle}}}, {
			'$group': {'_id': '$twitter_handle', 'average': {'$avg': '$comments'}}}])
		ig_avg_comments = list(ig_avg_comments)[0]['average']
		plot_4_x.append(data_sources[1])
		plot_4_y.append(ig_avg_comments)
		plot_4_colors.append(data_sources_colors[1])
	except IndexError:
		ig_avg_comments = 0

	try:
		yt_avg_comments = db.youtube_collection.aggregate([{'$match': {'twitter_handle': {'$eq': tw_handle}}}, {
			'$group': {'_id': '$twitter_handle', 'average': {'$avg': '$comments'}}}])
		yt_avg_comments = list(yt_avg_comments)[0]['average']
		plot_4_x.append(data_sources[2])
		plot_4_y.append(yt_avg_comments)
		plot_4_colors.append(data_sources_colors[2])
	except IndexError:
		pass

	try:
		fb_avg_comments = db.facebook_new_collection.aggregate([{'$match': {'twitter_handle': {'$eq': tw_handle}}}, {
			'$group': {'_id': '$twitter_handle', 'average': {'$avg': '$fb_no_of_comments'}}}])
		fb_avg_comments = list(fb_avg_comments)[0]['average']
		plot_4_x.append(data_sources[3])
		plot_4_y.append(fb_avg_comments)
		plot_4_colors.append(data_sources_colors[3])
	except IndexError:
		pass

	plot_4_radius = [item**(1. / 2) for item in plot_4_y]

	plot_4_div = bubble_plot(x_list=plot_4_x, radius=plot_4_radius, bubblecolors=plot_4_colors, title='Avg audience interaction across platforms',
							 hover_labels=plot_4_y)

	try:
		tw_tm_div = open(
			'static/html_plots/tw_{}.html'.format(tw_handle)).read()
	except:
		tw_tm_div = 'HTTP 404: Account unavailable.'

	try:
		ig_tm_div = open(
			'static/html_plots/ig_{}.html'.format(tw_handle)).read()
	except:
		ig_tm_div = 'HTTP 404: Account unavailable.'

	try:
		yt_tm_div = open(
			'static/html_plots/yt_{}.html'.format(tw_handle)).read()
	except:
		yt_tm_div = 'HTTP 404: Account unavailable.'

	try:
		fb_tm_div = open(
			'static/html_plots/fb_{}.html'.format(tw_handle)).read()
	except:
		fb_tm_div = 'HTTP 404: Account unavailable.'

	tw_df = pd.DataFrame(
		list(db.twitter_new_collection.find({'handle': tw_handle})))
	ig_df = pd.DataFrame(
		list(db.instagram_collection.find({'twitter_handle': tw_handle})))
	yt_df = pd.DataFrame(
		list(db.youtube_collection.find({'twitter_handle': tw_handle})))
	fb_df = pd.DataFrame(
		list(db.facebook_new_collection.find({'twitter_handle': tw_handle})))

	# Start
	try:
		trace0_x, trace0_y = get_by_hod(ig_df, 'likes', 'timestamp')
		# print(trace0_x, trace0_y)

		trace0_x = list(trace0_x)
		trace0_y = list(trace0_y)

		for i in range(0, 24):
			if i not in trace0_x:
				trace0_x.append(i)
				trace0_y.append(0)

		trace0_df = pd.DataFrame([trace0_x, trace0_y]).T
		trace0_df.columns = ['x', 'y']
		trace0_df = trace0_df.sort_values(by='x')

		trace0_x = trace0_df.x.astype(int).tolist()
		trace0_y = trace0_df.y.astype(int).tolist()
	except:
		trace0_x = []
		trace0_y = []

	# End

	trace1_x, trace1_y = tw_get_by_hod(tw_df, 'favorites', 'created_at')
	# print(trace0_x, trace0_y)

	trace1_x = list(trace1_x)
	trace1_y = list(trace1_y)

	for i in range(0, 24):
		if i not in trace0_x:
			trace1_x.append(i)
			trace1_y.append(0)

	trace1_df = pd.DataFrame([trace1_x, trace1_y]).T
	trace1_df.columns = ['x', 'y']
	trace1_df = trace1_df.sort_values(by='x')

	trace1_x = trace1_df.x.astype(int).tolist()
	trace1_y = trace1_df.y.astype(int).tolist()

	# End
	try:
		trace2_x, trace2_y = yt_get_by_hod(yt_df, 'likes', 'publishat')
		trace2_x = list(trace2_x)
		trace2_y = list(trace2_y)

		for i in range(0, 24):
			if i not in trace2_x:
				trace2_x.append(i)
				trace2_y.append(0)

		trace2_df = pd.DataFrame([trace2_x, trace2_y]).T
		trace2_df.columns = ['x', 'y']
		trace2_df = trace2_df.sort_values(by='x')

		trace2_x = trace2_df.x.astype(int).tolist()
		trace2_y = trace2_df.y.astype(int).tolist()
	except:
		trace2_x = []
		trace2_y = []

	try:
		# print(trace0_x, trace0_y)
		trace3_x, trace3_y = fb_get_by_hod(
			fb_df, 'fb_shares', 'fb_time_created')
		# print(trace0_x, trace0_y)

		trace3_x = list(trace3_x)
		trace3_y = list(trace3_y)

		for i in range(0, 24):
			if i not in trace2_x:
				trace3_x.append(i)
				trace3_y.append(0)

		trace3_df = pd.DataFrame([trace3_x, trace3_y]).T
		trace3_df.columns = ['x', 'y']
		trace3_df = trace3_df.sort_values(by='x')

		trace3_x = trace3_df.x.astype(int).tolist()
		trace3_y = trace3_df.y.astype(int).tolist()
	except:
		trace3_x = []
		trace3_y = []

	trace_list_x = [trace0_x, trace1_x, trace2_x, trace3_x, ]
	trace_list_y = [trace0_y, trace1_y, trace2_y, trace3_y, ]

	print(trace_list_x)
	print(trace_list_y)

	plot_5_div = multi_line(x_data=trace_list_x, y_data=trace_list_y, labels=data_sources[0:4], colors=data_sources_colors[0:4],
							title="Influencer activity by hour", x_axis_label='Hours', fill=True)

	# Topic pills
	pills_list = list(db.pills_collection.find({'tw_handle': tw_handle}))
	topics = pills_list[0]['topics']

	# CV Results
	cv_results = db.cv_collection.find({'tw_handle': tw_handle})

	# Plot 6 - Heatmap
	try:
		ig_df_dom = with_day_of_month(ig_df, 'timestamp')
		ig_df_new = with_month(ig_df_dom, 'timestamp')

		ig_df_new['interactions_count'] = ig_df_new[
			'likes'] + ig_df_new['comments']
		gpd = ig_df_new.groupby(['month', 'day_of_month'])[
			'interactions_count'].sum()

		months = ['January', 'February', 'March', 'April', 'May', 'June',
				  'July', 'August', 'September', 'October', 'November', 'December']
		months_form = [m[:3] for m in months[::-1]]

		pv = ig_df_new.pivot_table(index='month', columns=[
			'day_of_month'], aggfunc='sum', fill_value=0, values='interactions_count')
		pv = pv.reindex(months_form)
		# print(gpd.head())

		y = list(pv.index)

		x = list(range(1, 31))

		z = pv.values.tolist()
		# print(z[0])

		plot_6_div = heat_map(x, y, z, title='Monthly user interaction quotient',
							  colorscale=[[0.0, 'rgb(49,54,149)'], [0.5, 'rgb(224,243,248)'], [1.0, 'rgb(165,0,38)']])
		insta_path = 'static/instagram-images/{}/'.format(tw_handle)
		insta_files = [f for f in listdir(insta_path) if isfile(
			join(insta_path, f)) and (not f.startswith('.'))]

		random_images = random.sample(insta_files, 5)

	except:
		plot_6_div = ''
		random_images = []

	try:
	# Plot 7 div
		def get_date(epoch):
			return datetime.fromtimestamp(epoch).strftime('%b %d')

		ig_audience_document = db.instagram_audience_collection.find({'tw_handle': tw_handle})
		ig_aud_df = pd.DataFrame(list(ig_audience_document))
		ig_aud_df['followers_diff'] = ig_aud_df['followers'].shift(-1) - ig_aud_df['followers']

		ig_aud_df['m_d'] = ig_aud_df['epoch'].apply(get_date)

		x_data = list(ig_aud_df['m_d'])

		fols = ig_aud_df['followers'].tolist()
		vals = ig_aud_df['followers_diff'].tolist()
		height = [math.fabs(i) for i in vals]
		positives = []
		negatives = []

		counter = 0
		for v in vals:
			if v >=0:
				positives.append(height[counter])
			else:
				positives.append(0)
			if v < 0:
				negatives.append(-height[counter])
			else:
				negatives.append(0)
			counter += 1

		data = vals[0:7]


		data = np.array(data)
		changes = {'amount' : data}

		index = list(range(1,8))
		trans = pd.DataFrame(data=changes,index=index)
		bases = list(trans.amount.cumsum().shift(1).fillna(0))

		bases = bases[0:7]
		positives = positives[0:7]
		negatives = negatives[0:7]
		x_data = x_data[0:7]

		wfall_div = plotWaterfall(x_data, positives, negatives, bases)
	except:
		wfall_div = ''

	return render_template('per_influencer_page.html', yt_subscriber_count=yt_subscriber_count,
						   tw_followers_count=tw_followers_count, ig_followers=ig_followers, fb_page_likes=fb_page_likes,
						   tw_description=tw_description, tw_location=tw_location, fb_category=fb_category,
						   tw_name=tw_name, ig_thumbnail_url=ig_thumbnail_url, plot_1_div=plot_1_div, plot_2_div=plot_2_div,
						   plot_3_div=plot_3_div, plot_4_div=plot_4_div, tw_tm_div=tw_tm_div, ig_tm_div=ig_tm_div,
						   yt_tm_div=yt_tm_div, fb_tm_div=fb_tm_div, tw_handle=tw_handle, plot_5_div=plot_5_div, topics=topics,
						   cv_results=cv_results, twitter_url=twitter_url, facebook_url=facebook_url, instagram_url=instagram_url,
						   youtube_url=youtube_url, plot_6_div=plot_6_div, random_images=random_images, kl_score=kl_score,
						   rank=rank_document['rf_rank'], wfall_div=wfall_div)

if __name__ == '__main__':
	app.run(port=5000, debug=True)
