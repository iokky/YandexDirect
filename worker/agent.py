from apscheduler.schedulers.background import BackgroundScheduler

from connectors.yandex_direct.client import YandexDirectConn

from logger.telegram import send_message


yandex_direct_agent = YandexDirectConn()


def yandex_direct_run():
    yandex_direct_agent.run()
    send_message('yandex_direct_agent done ')


scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Moscow'})
scheduler.start()
scheduler.add_job(yandex_direct_run, 'cron', hour='01', minute='40')


