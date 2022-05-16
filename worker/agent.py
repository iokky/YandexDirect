from apscheduler.schedulers.background import BackgroundScheduler

from connectors.yandex_direct.client import YandexDirectConn

from logger.telegram import send_message


yandex_direct_agent = YandexDirectConn()


def ct_run():
    yandex_direct_agent.run()
    send_message('yandex_direct_agent done ')


scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Moscow'})
scheduler.start()
scheduler.add_job(ct_run, 'cron', hour='01', minute='40')


# date -s "03 MAY 2022 02:10:00"
