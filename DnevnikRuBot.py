import traceback
try:
	from selenium import webdriver
	from selenium.webdriver import Chrome
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.common.keys import Keys
	from time import sleep, ctime
	import os
	import datetime
	from pushbullet import Pushbullet
	import configparser
	from os import system
	from cryptography.fernet import Fernet

	system("title DnevnikRuBot")

	print("-------------------------------------------\nDnevnikRuBot v1.2\nРазработчик/поддержка: vk.com/oleg_kapranov\nДля вопрос-ответ читайте info.txt\n-------------------------------------------")

	opts = Options()
	opts.headless = True
	opts.add_argument('--log-level=3')

	homepath = os.getenv('USERPROFILE')
	file_name = os.path.normpath(homepath + '/Documents/DnevnikRuBot/data.ini')
	folder_path = os.path.normpath(homepath + '/Documents/DnevnikRuBot')
	salt_path = os.path.normpath(homepath + '/AppData/Roaming/DnevnikRuBot/salt.md')
	salt_folder_path = os.path.normpath(homepath + '/AppData/Roaming/DnevnikRuBot')

	try:
		check = open('./fix.txt')
		check.close()
		fexist = 1
	except FileNotFoundError:
		fexist = 0

	timesNeed = 1
	if fexist == 1:
		fix = open('./fix.txt')
		fixTimes = fix.read()
		fix.close()
		fixTimes = fixTimes.split('\n')
		
		timesLen = len(fixTimes)
		i = 0
		hour = []
		minute = []
		stopHour = []
		stopMinute = []
		while i < timesLen:
			text = fixTimes[i]
			text = text.split(" ")
			stopText = text[2]
			stopText = stopText.split(":")
			stopHour.append(int(stopText[0]))
			stopMinute.append(int(stopText[1]))
			text = text[0]
			text = text.split(":")
			hour.append(int(text[0]))
			minute.append(int(text[1]))
			i += 1

		text = fixTimes[timesLen-1]
		text = text.split(" ")
		text = text[2]
		text = text.split(":")
		hour.append(int(text[0]))
		minute.append(int(text[1])+1)
		timesNeed = 0

	try:
		check = open(file_name)
		check.close()
		fexist = 1
	except FileNotFoundError:
		fexist = 0

	if fexist == 1:
		ini = configparser.ConfigParser()
		ini.read(file_name)
		getlogin = ini.get('data', 'login')
		getpassword = ini.get('data', 'pass')
		gettoken = ini.get('data', 'token')
	else:
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)
		create = open(file_name, 'w')
		create.write('[data]\nlogin=-1\npass=-1\ntoken=-1')
		create.close()
		ini = configparser.ConfigParser()
		ini.read(file_name)
		getlogin = -1
		getpassword = -1
		getpath = -1
		
	if gettoken != '-1':
		print('Использовать сохраненный токен Pushbullet?(да/нет): ', end='')
		answer = input()
		if answer.lower() == 'да':
			token = gettoken
		elif answer.lower() == 'нет':
			print('Введите новый токен Pushbullet: ', end='')
			token = input()
			print('Сохранить введеный токен Pushbullet?(да/нет): ', end='')
			answer = input()
			if answer.lower() == 'да':
				ini.set('data', 'token', token)
			elif answer.lower() == 'нет':
				ini.set('data', 'token', '-1')
			else:
				print('Не обнаружено ответа (да/нет). Завершение...')
				os.system('pause')
				raise SystemExit
		else:
			print('Не обнаружено ответа (да/нет). Завершение...')
			os.system('pause')
			raise SystemExit
	else:
		print('Введите токен Pushbullet: ', end='')
		token = input()
		print('Сохранить введеный токен Pushbullet?(да/нет): ', end='')
		answer = input()
		if answer.lower() == 'да':
			ini.set('data', 'token', token)
		elif answer.lower() == 'нет':
			ini.set('data', 'token', '-1')
		else:
			print('Не обнаружено ответа (да/нет). Завершение...')
			os.system('pause')
			raise SystemExit
			
	try:
		check = open(salt_path)
		check.close()
		fexist = 1
	except FileNotFoundError:
		fexist = 0
		
	if fexist == 0:
		if getlogin != '-1':
			print('Не удалось получить ключ для дешифровки пароля. Просьба ввести логин/пароль заново.')
		getlogin = '-1'
		getpassword = '-1'
		ini.set('data', 'login', '-1')
		ini.set('data', 'pass', '-1')
		with open(file_name, "w") as config_file:
			ini.write(config_file)
	else:
		salt_file = open(salt_path)
		salt = salt_file.read()
		salt = salt.encode()
		salt_file.close()

	if getlogin != '-1':
		print('Использовать сохраненный логин/пароль?(да/нет): ', end='')
		answer = input()
		if answer.lower() == 'да':
			login = getlogin
			f = Fernet(salt)
			password = f.decrypt(getpassword.encode())
			password = password.decode()
		elif answer.lower() == 'нет':
			print('Введите новый логин: ', end='')
			login = input()
			print('Введите новый пароль: ', end='')
			password = input()
			if not os.path.exists(salt_folder_path):
				os.makedirs(salt_folder_path)
			salt = Fernet.generate_key()
			salt_file = open(salt_path, 'w')
			salt_file.write(salt.decode())
			salt_file.close()
			f = Fernet(salt)
			encoded = f.encrypt(password.encode())
			print('Сохранить введеные логин/пароль?(да/нет): ', end='')
			answer = input()
			if answer.lower() == 'да':
				ini.set('data', 'login', login)
				ini.set('data', 'pass', encoded.decode())
			elif answer.lower() == 'нет':
				ini.set('data', 'login', '-1')
				ini.set('data', 'pass', '-1')
			else:
				print('Не обнаружено ответа (да/нет). Завершение...')
				os.system('pause')
				raise SystemExit
		else:
			print('Не обнаружено ответа (да/нет). Завершение...')
			os.system('pause')
			raise SystemExit
	else:
		print('Введите логин: ', end='')
		login = input()
		print('Введите пароль: ', end='')
		password = input()
		if not os.path.exists(salt_folder_path):
			os.makedirs(salt_folder_path)
		salt = Fernet.generate_key()
		salt_file = open(salt_path, 'w')
		salt_file.write(salt.decode())
		salt_file.close()
		f = Fernet(salt)
		encoded = f.encrypt(password.encode())
		print('Сохранить введеные логин/пароль?(да/нет): ', end='')
		answer = input()
		if answer.lower() == 'да':
			ini.set('data', 'login', login)
			ini.set('data', 'pass', encoded.decode())
		elif answer.lower() == 'нет':
			ini.set('data', 'login', '-1')
			ini.set('data', 'pass', '-1')
		else:
			print('Не обнаружено ответа (да/нет). Завершение...')
			os.system('pause')
			raise SystemExit
			
	with open(file_name, "w") as config_file:
		ini.write(config_file)
		
	try:
		pb = Pushbullet(token)
	except:
		print("[ERROR] Не удалось подключиться к Pushbullet. Возможно вы ввели неверный токен. В ином случае обращайтесь в поддержку.")

	path = './chromedriver.exe'
	browser = Chrome(path, options=opts)
	browser.get("https://login.dnevnik.ru/login")

	print("\n[INFO] Авторизируюсь...\n")

	sleep(1)
	login_form = browser.find_element_by_class_name('login__body__input_login')
	login_form.send_keys(login)

	sleep(1)
	pass_form = browser.find_element_by_class_name('login__body__input_password')
	pass_form.send_keys(password)

	sleep(1)
	browser.find_element_by_class_name('login__submit').click()

	try:
		sleep(1)
		menu = browser.find_elements_by_class_name('header-submenu__item')
		menu[3].click()
	except:
		print('[ERROR] Не удалось зайти в расписание. Возможно вы ввели неверный логин или пароль. В ином случае обращайтесь в поддержку.\n Завершение...')
		os.system('pause')
		raise SystemExit

	try:
		if timesNeed == 1:
			sleep(1)
			tabs = browser.find_elements_by_class_name('NotSet   ')
			tabs[4].click()

			sleep(1)
			times = browser.find_elements_by_class_name('s3')
			timesLen = len(times)
			i = 0
			hour = []
			minute = []
			stopHour = []
			stopMinute = []
			while i < timesLen:
				text = times[i].text
				text = text.split(" ")
				stopText = text[2]
				stopText = stopText.split(":")
				stopHour.append(int(stopText[0]))
				stopMinute.append(int(stopText[1]))
				text = text[0]
				text = text.split(":")
				hour.append(int(text[0]))
				minute.append(int(text[1]))
				i += 1

			text = times[timesLen-1].text
			text = text.split(" ")
			text = text[2]
			text = text.split(":")
			hour.append(int(text[0]))
			minute.append(int(text[1])+1)

			sleep(1)
			menu = browser.find_elements_by_class_name('header-submenu__item')
			menu[3].click()
	except:
		print('[ERROR] Не удалось получить время звонков. Проверьте вкладку Расписание -> Звонки, если расписание звонков есть - обращайтесь в поддержку. Если нет - читайте savetext.ru/82r59tKG\n Завершение...')
		os.system('pause')
		raise SystemExit

	def getLessionNum(now):
		i = 0
		lession = -1
		while i < timesLen:
			if (now.hour == hour[i] and now.minute >= minute[i]) or (now.hour == hour[i+1] and now.minute <= minute[i+1]-1):
				lession = i+1
			i += 1
		return str(lession)
		
	def getIdBlock(now, num):
		nowdate = now.strftime('%Y%m%d')
		return 'd'+nowdate+'_'+str(num)
		
	def getTomIdBlock(now, num):
		day = str(int(now.strftime('%d')) + 1)
		if int(day) < 10:
			day = "0" + day
		nowdate = now.strftime('%Y%m') + day
		return 'd'+nowdate+'_'+str(num)
		
	def minusTen(hour, minute):
		if minute >= 10:
			minute -= 10
		else:
			ost = minute - 10
			hour -= 1
			minute = 60 + ost
		return [hour, minute]

	nextName = ''
	print("\n")
	print("[INFO] Уведомления активны. В работе.")
	while 1:
		now = datetime.datetime.now()
		week = datetime.datetime.today().isoweekday()
		
		lesNum = getLessionNum(now)
		got = minusTen(stopHour[int(lesNum)-1], stopMinute[int(lesNum)-1])
		h = got[0]
		m = got[1]
		if now.hour == h and now.minute == m and now.second == 0 and nextName != 'empty':
			push = pb.push_note("Урок скоро закончится!", "Осталось 10 минут до конца урока.")
			
		if now.hour == stopHour[int(lesNum)-1] and now.minute == stopMinute[int(lesNum)-1] and now.second == 0 and (nextName != 'empty' and nextName != 'last'):
			push = pb.push_note("Урок закончился!", "Следующий урок: "+nextName+'\nКабинет: '+nextCab)
			
		if now.hour == stopHour[int(lesNum)-1] and now.minute == stopMinute[int(lesNum)-1] and now.second == 0 and nextName == 'last':
			i = 0
			tom = ""
			while i < len(stopMinute):
				idBlock = getTomIdBlock(now, i+1)
				info = browser.find_element_by_id(idBlock).text
				info = info.split('\n')
				if minute[i] < 10:
					minutePlus = "0"
				else:
					minutePlus = ""
				if stopMinute[i] < 10:
					stopMinutePlus = "0"
				else:
					stopMinutePlus = ""
				if info[0] != '':
					NameFirst = 1
					if len(info) > 4:
						menu = browser.find_elements_by_class_name('header-submenu__item')
						menu[2].click()
						sleep(1)
						if week > 0 and week < 4:
							leftnright = "1"
							dayl = str(week)
						else:
							leftnright = "2"
							dayl = str(week - 3)
						fixLession = browser.find_element_by_xpath('/html[1]/body[1]/div[2]/div[1]/div[9]/div['+leftnright+']/div['+dayl+']/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr['+str(int(lesNum)+1)+']/td[1]').text
						fixLession = fixLession.split('\n')
						fixLession = fixLession[0]
						listI = list(info[0])
						listF = list(fixLession)
						fixLen = len(fixLession)
						
						if fixLen < 6:
							fixCheck = fixLen
						else:
							fixCheck = 6
						
						f = 0
						while f < fixCheck:
							if listI[f] != listF[f]:
								NameFirst = 0
								break
							f += 1
						menu = browser.find_elements_by_class_name('header-submenu__item')
						menu[3].click()
						sleep(1)
					tom += "\n"+str(i+1)+". "+info[0]+"("+info[3]+"), "+str(hour[i])+":"+minutePlus+str(minute[i])+"-"+str(stopHour[i])+":"+stopMinutePlus+str(stopMinute[i])
				i += 1
				
			if tom == "":
				tom = "\nотсутствует"
			push = pb.push_note("Последний урок закончился!", "Расписание на завтра:"+tom)

		if now.second == 20:
			sleep(1)
			try:
				menu = browser.find_elements_by_class_name('header-submenu__item')
				menu[3].click()
			except:
				print("[WARN] Не удалось обновить расписание.")
				continue
			sleep(1)
			lesNum = getLessionNum(now)
			if lesNum == '-1':
				continue
			idBlock = getIdBlock(now, int(lesNum)+1)
			info = browser.find_element_by_id(idBlock).text
			info = info.split('\n')
			if info[0] != '':
				NameFirst = 1
				if len(info) > 4:
					menu = browser.find_elements_by_class_name('header-submenu__item')
					menu[2].click()
					sleep(1)
					if week > 0 and week < 4:
						leftnright = "1"
						dayl = str(week)
					else:
						leftnright = "2"
						dayl = str(week - 3)
					fixLession = browser.find_element_by_xpath('/html[1]/body[1]/div[2]/div[1]/div[9]/div['+leftnright+']/div['+dayl+']/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr['+str(int(lesNum)+1)+']/td[1]').text
					fixLession = fixLession.split('\n')
					fixLession = fixLession[0]
					listI = list(info[0])
					listF = list(fixLession)
					fixLen = len(fixLession)
					
					if fixLen < 6:
						fixCheck = fixLen
					else:
						fixCheck = 6
					
					f = 0
					while f < fixCheck:
						if listI[f] != listF[f]:
							NameFirst = 0
							break
						f += 1
					menu = browser.find_elements_by_class_name('header-submenu__item')
					menu[3].click()
					sleep(1)
				if NameFirst == 1:
					nextName = info[0]
					nextCab = info[3]
				else:
					nextName = info[4]
					nextCab = info[7]
				idBlock = getIdBlock(now, int(lesNum))
				info = browser.find_element_by_id(idBlock).text
				info = info.split('\n')
				if info[0] == '':
					nextName = 'empty'
			else:
				idBlock = getIdBlock(now, int(lesNum))
				info = browser.find_element_by_id(idBlock).text
				info = info.split('\n')
				if info[0] != '':
					nextName = 'last'
				else:
					nextName = 'empty'
		sleep(1)
except Exception as e:
	print("[ERROR] "+traceback.format_exc())
	os.system('pause')
	raise SystemExit