import re, sys, requests, time

session = requests.session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
	})


def get_csrf_token(content):
	pattern = re.compile(r"input type='hidden' name='csrf_token' value='(.*?)'")
	return pattern.findall(content)[0]

def get_friend_id_list():
	content = session.get("https://codeforces.com/friends").text
	regex = re.compile(r'friendUserId="(.*?)"')
	return regex.findall(content)
	
def add_friend(id):
	print(id)
	content = session.get("https://codeforces.com/profile/MikeMirzayanov").text
	data = {
		'csrf_token': get_csrf_token(content),
		'friendUserId': id,
		'isAdd': 'true',
	}
	res = session.post("https://codeforces.com/data/friend", data=data)

def login(username, password):
	url = "https://codeforces.com/enter"
	text = session.get(url).text
	data = {
		'csrf_token': get_csrf_token(text),
		'ftaa': 'jshedqz38upltgyz7u',
		'bfaa': '262e4b1217220f326d1bb72da0b5daa4',
		'handleOrEmail': username,
		'password': password,
		'_tta': '115',
		'action': 'enter',
	}
	session.post(url, data=data)

def show_help_page():
	print('\nUsage: python script.py | script.exe <option> <username> <password>')
	print('\nOptions:')
	print('get      : Get friends of current user and save as file "friends.txt".')
	print('clone    : Add users in "friends.txt" as your friends of current user.')
	print('\nUsername : Handle/Email to login in.')
	print('\nPassword : Password for current user.')
	print("\nExamples:")
	print("script.exe get   zzq233 123456789    // get friends list of <zzq233>")
	print("script.exe clone bakapiano 123456789 // add them as <bakapiano>'s friends")

if __name__ == "__main__":
	if len(sys.argv) != 4 or sys.argv[1] in ["help","h","-h","--help","--h"]:
		show_help_page()
		sys.exit(0)
	
	login(sys.argv[2], sys.argv[3])

	if sys.argv[1] in ["get", "-get", "--get"]:
		friends = get_friend_id_list()
		with open("friends.txt", "w") as file:
			for id in friends:
				file.writelines(id)
				file.write("\n")
		print(friends)
		print("Done.")
		
	elif sys.argv[1] in ["clone", "-clone", "--clone"]:
		friends = []
		with open("friends.txt", "r") as file:
			friends = file.readlines()
		for id in friends:
			time.sleep(1)
			add_friend(id.strip())
		print("Done.")
		
	else:
		show_help_page()
