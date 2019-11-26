import requests
import json
import time

TINDER_URL = "https://api.gotinder.com"

class person():
	def __init__(self, data):
		self._id = data['user']['_id']
		self.s_number = data['s_number']

class tinderAPI():
	def __init__(self, token):
		self._token = token

	def like(self, user_id, s_number):
		while True:
			try:
				data = requests.get(TINDER_URL + "/like/" + str(user_id), params = {'s_number': s_number, 'locale': 'en'}, headers={"X-Auth-Token": self._token}).json()
				break
			except:
				print ('Like error, trying again after 3 seconds')
				time.sleep(3)
				pass
		return data['match']

	def dislike(self, user_id):
		while True:
			try:
				data = requests.get(TINDER_URL + "/pass/" + str(user_id), params = {'s_number': s_number, 'locale': 'en'}, headers={"X-Auth-Token": self._token}).json()
				break
			except:
				print ('Dislike error, trying again after 3 seconds')
				time.sleep(3)
				pass
		return data

	def nearby_persons(self):
		while True:
			try:
				datas = requests.get(TINDER_URL + "/v2/recs/core", headers={"X-Auth-Token": self._token}).json()
				break
			except:
				print ('Get nearby persons error, trying again after 3 seconds')
				time.sleep(3)
				pass
		list_user_info = []
		try:
			list_user = datas['data']['results']
			for i in list_user:
				_user = person(i)
				list_user_info.append(_user)
		except Exception as e:
			print e
			pass
		return list_user_info

if __name__ == "__main__":
	token = "x-auth-token"
	api = tinderAPI(token)
	count = 1
	while True:
		list_user = api.nearby_persons()
		if not list_user:
			print ('Not found any persons around, finished')
			break
		for user in list_user:
			match = api.like(user._id, user.s_number)
			print ('Is matched for user id {}: {}'.format(user._id, match))
			print ('Liked {} users'.format(count))
			count = count + 1