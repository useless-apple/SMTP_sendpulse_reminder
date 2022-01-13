import json
from datetime import datetime, timedelta

from pytz import timezone

import requests

from sqlite import get_token, get_params, write_token, check_and_update_sql, get_tg_info
import telebot

import logging
from settings import BASE_DIR


def get_date_time(time_format="%Y-%m-%d"):
	date_and_time = datetime.now(timezone('Asia/Yekaterinburg')).strftime(time_format)
	return date_and_time


logging.basicConfig(
	filename="{0}/logs/log-{1}.log".format(BASE_DIR, get_date_time()),
	level=logging.INFO,
	format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
)
log = logging.getLogger("ex")

auth_url = 'https://api.sendpulse.com/oauth/access_token'
user_info_url = 'https://api.sendpulse.com/user/balance/detail'


def get_user_info(user_info_url, headers):
	return requests.get(user_info_url, headers=headers)


def get_info_global():
	headers = {
		'authorization': get_token()
	}

	user_info = get_user_info(user_info_url, headers)

	if user_info.status_code == 200:
		return json.loads(user_info.text)

	elif user_info.status_code == 500 or user_info.status_code == 401:
		log.info('New token')
		auth = requests.post(auth_url, data=get_params())
		token = json.loads(auth.text)
		access_token = token['token_type'] + ' ' + token['access_token']
		write_token(access_token)
		headers = {
			'authorization': access_token,
		}
		user_info = get_user_info(user_info_url, headers)
		return json.loads(user_info.text)

	else:
		log.warning('New status code' + str(user_info.status_code))
		print(user_info.status_code)
		return None


if __name__ == '__main__':
	try:
		log.info('-----------------------------------------------------------------------------------------------')
		log.info('Starting parsing ' + str(get_date_time()))
		timenow = datetime.strptime(get_date_time(), "%Y-%m-%d").date()
		TG_TOKEN, CHAT_ID, EXCEPTION_CHAT_ID = get_tg_info()
		bot = telebot.TeleBot(TG_TOKEN)


		@bot.message_handler(content_types=['text'])
		def text_handler(text, chat_id):
			if text is not None:
				bot.send_message(chat_id, text)

		info = get_info_global()
		if info is not None:
			if info['smtp']:
				if info['smtp']['end_date']:
					text = ''
					time_end_date = datetime.strptime(info['smtp']['end_date'], "%Y-%m-%d  %H:%M:%S").date()
					if timenow + timedelta(days=1) == time_end_date:
						text = 'Один день до конца тарифа, дата окончания'.format(time_end_date)
					elif timenow + timedelta(days=2) == time_end_date:
						text = 'Два дня до конца тарифа, дата окончания'.format(time_end_date)
					elif timenow + timedelta(days=3) == time_end_date:
						text = 'Три дня до конца тарифа, дата окончания'.format(time_end_date)
					if check_and_update_sql('last_info_day', text):
						text_handler(text, CHAT_ID)
						log.info(text)
					check_and_update_sql('current_day', str(time_end_date))
				else:
					log.warning('No Date')
					text_handler('No Date', EXCEPTION_CHAT_ID)
				if info['smtp']['email_qty_left']:
					text = ''
					log.info(str(info['smtp']['email_qty_left']))
					if info['smtp']['email_qty_left'] < 100:
						text = 'Осталось менее 100 заявок'.format(info['smtp']['email_qty_left'])
					elif info['smtp']['email_qty_left'] < 300:
						text = 'Осталось менее 300 заявок'.format(info['smtp']['email_qty_left'])
					elif info['smtp']['email_qty_left'] < 500:
						text = 'Осталось менее 500 заявок'.format(info['smtp']['email_qty_left'])
					elif info['smtp']['email_qty_left'] < 1000:
						text = 'Осталось менее 1000 заявок'.format(info['smtp']['email_qty_left'])
					if check_and_update_sql('last_info_count', text):
						text_handler(text, CHAT_ID)
					log.info('Заявок насчитано: ' + str(info['smtp']['email_qty_left']))
					check_and_update_sql('count_tickets', str(info['smtp']['email_qty_left']))
				else:
					log.warning('No limit')
					text_handler('No limit', EXCEPTION_CHAT_ID)
			else:
				log.warning('No smtp')
				text_handler('No smtp', EXCEPTION_CHAT_ID)
		log.info('Parsing Success ' + str(get_date_time()))
		log.info('-----------------------------------------------------------------------------------------------')
	except Exception as e:
		log.exception(str(e))
