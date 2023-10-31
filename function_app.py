import datetime
import json
import logging
import os
import azure.functions as func

# from logging import getLogger, Formatter, StreamHandler, DEBUG
from typing import Any, Dict
from urllib import request

# logger = getLogger(__name__)
# handler = StreamHandler()
# handler.setLevel(DEBUG)
# handler.setFormatter(Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s', datefmt='%Y/%m/%d %H:%M:%S'))
# logger.setLevel(DEBUG)
# logger.addHandler(handler)
# logger.propagate = False

DAY_OF_WEEKS = '日月火水木金土日'

WEBHOOK_URL = os.getenv("SlackWebhookUrl")

OPEN_METEO_URL = 'https://api.open-meteo.com/v1/forecast'

OPEN_METEO_QUERIES = {
    'latitude': 34.6937,
    'longitude': 135.5022,
    'daily': [
        'weathercode',
        'temperature_2m_max',
        'temperature_2m_min',
        'sunrise',
        'sunset',
        'precipitation_probability_max',
    ],
    'timezone': r'Asia%2FTokyo',
    'forecast_days': 1,
}


app = func.FunctionApp()


def create_query_parameter(params: Dict[str, Any]) -> str:
    """
    Create query string from object.

    Parameters
    ----------
    params : Dict[str, Any]
        Query object.

    Returns
    -------
    str
        Query string
    """
    ret = '?'
    for key, value in params.items():
        if type(value) is list:
            ret += f"{key}={','.join(value)}&"
        else:
            ret += f"{key}={value}&"
    return ret[:-1]


def get_weather_string_from_wmo_code(wmo_code: int) -> str:
    """
    Get weather string (ja) from WMO Code 4677 (ww).

    Parameters
    ----------
    wmo_code : int
        WMO Code 4677 (ww).

    Returns
    -------
    str
        String representation.

    Raises
    ------
    ValueError
        _description_
    """
    ret = ''
    if wmo_code == 0:
        ret = '晴れ'
    elif 1 <= wmo_code <= 3:
        ret = '曇り'
    elif 40 <= wmo_code <= 49:
        ret = '霧'
    elif 50 <= wmo_code <= 59:
        ret = '小雨'
    elif 60 <= wmo_code <= 69:
        ret = '雨'
    elif 70 <= wmo_code <= 79:
        ret = '雪'
    elif 80 <= wmo_code <= 84:
        ret = '時々雨'
    elif 85 <= wmo_code <= 89:
        ret = '時々雪'
    elif 99 <= wmo_code <= 99:
        ret = '雷'
    else:
        raise ValueError(f"Code ww {wmo_code} is not defined by WMO Code 4677.")
    return ret


def post_slack(message: str) -> None:
    """
    Post message to Slack.

    Parameters
    ----------
    message : str
        Post content.

    Raises
    ------
    e
        _description_
    """
    webhook_req_header = {
        'Content-Type': 'application/json',
    }
    webhook_req_data = json.dumps({
        'text': message
    })
    webhook_req = request.Request(WEBHOOK_URL, data=webhook_req_data.encode(), method='POST', headers=webhook_req_header)
    try:
        with request.urlopen(webhook_req) as response:
            headers = response.getheaders()
            status = response.getcode()
            logging.debug(headers)
            logging.debug(status)
    except Exception as e:
        raise e


@app.schedule(schedule="0 0 0 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def TimerFunc(myTimer: func.TimerRequest) -> None:
    """
    _summary_

    Parameters
    ----------
    myTimer : func.TimerRequest
        _description_
    """
    logging.info('start uchi-notify-weather-slack-bot, TimerFunc')
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    try:
        get_url = OPEN_METEO_URL + create_query_parameter(OPEN_METEO_QUERIES)
        get_response = {}
        with request.urlopen(get_url) as response:
            get_response = json.loads(response.read())

        daily_units = get_response['daily_units']
        daily = get_response['daily']
        wmo_str = get_weather_string_from_wmo_code(daily['weathercode'][0])
        target_date = datetime.date.fromisoformat(daily['time'][0])
        sunrise_time = datetime.datetime.fromisoformat(daily['sunrise'][0]).time()
        sunset_time = datetime.datetime.fromisoformat(daily['sunset'][0]).time()
        dow_idx = target_date.strftime('%u')
        dow_str = DAY_OF_WEEKS[int(dow_idx)]

        message = f"{target_date.year}年{target_date.month}月{target_date.day}日 ({dow_str}) の天気は{wmo_str}。\n" + \
            f"最低気温は{daily['temperature_2m_min'][0]}{daily_units['temperature_2m_min']}、" + \
            f"最高気温は{daily['temperature_2m_max'][0]}{daily_units['temperature_2m_max']}、" + \
            f"降水確率は{daily['precipitation_probability_max'][0]}{daily_units['precipitation_probability_max']}です。\n" + \
            f"日の出時刻は{sunrise_time.hour}時{sunrise_time.minute}分、" + \
            f"日の入時刻は{sunset_time.hour}時{sunset_time.minute}分です。"

        post_slack(message)
    except Exception as e:
        logging.error(e.with_traceback())
    logging.info('end uchi-notify-weather-slack-bot, TimerFunc')
