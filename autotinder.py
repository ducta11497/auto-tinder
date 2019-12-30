from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
import requests
import time
import grequests

TINDER_URL = "https://api.gotinder.com"

class person():
	def __init__(self, data):
		self._id = data['user']['_id']
		self.s_number = data['s_number']

class tinderAPI():
	def __init__(self, token):
		self._token = token

	def exception(self, request, exception):
		print ('Problem: {}: {}'.format(request.url, exception))

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

	def like_async(self, list_user):
		urls = []
		for user in list_user:
			url = '{}/like/{}?locale=en&s_number={}'.format(TINDER_URL, user._id, user.s_number)
			urls.append(url)
		results = grequests.map((grequests.get(u, headers={"X-Auth-Token": self._token}) for u in urls), exception_handler=self.exception, size=5)
		count_success = 0
		for data in results:
			try:
				if 'match' in data.json():
					count_success = count_success + 1
			except:
				pass
		return results, count_success

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
			pass
		return list_user_info

def login_by_phone():
	s = requests.Session()

	phone_number = input('Enter your phone number: ')

	print ('Sending SMS...')
	s.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=en', json={"phone_number":phone_number})

	otp_code = input('Enter your verify code: ')

	print ('Verifying...')
	res = s.post('https://api.gotinder.com/v2/auth/sms/validate?auth_type=sms&locale=en', json={"otp_code":otp_code,"phone_number":phone_number,"is_update":False})

	json_res = res.json()
	if json_res['data']['validated']:
		json_data = {}
		json_data['refresh_token'] = json_res['data']['refresh_token']
		json_data['phone_number'] = phone_number

		res = s.post('https://api.gotinder.com/v2/auth/login/sms?locale=en', json=json_data)
		json_res = res.json()
		api_token = json_res['data']['api_token']
		print ('Verified')
		return api_token
	else:
		print ('Failed to verify, try again later')
		return False

def like_person(api_token):
	print ('Started to like')
	count = 0
	while True:
		list_user = api_token.nearby_persons()
		if not list_user:
			print ('Not found any persons around, finished')
			break
		like_list, success = api_token.like_async(list_user)
		count = count + success
		print ('Liked {} users'.format(count))
		
def main():
	while True:
		select = input ('''Select a way to login to tinder:
1. Input your token get on tinder.com
2. Login by phone number
Your choice: ''')
		if select == '1':
			token = input('Your token: ')
			break
		elif select == '2':
			token = login_by_phone()
			break
		else:
			pass
			
	if token and token != False:
		api_token = tinderAPI(token)
		like_person(api_token)
	else:
		return

if __name__ == "__main__":
	main()