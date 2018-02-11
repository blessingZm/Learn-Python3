import requests
import json


def hf_get_forecast(loccode):
    with open('hf_descrip.json', 'r') as jf:
        hf_descripDict = json.load(jf)

    url = 'https://free-api.heweather.com/v5/weather'
    data = {
        'city': '{}'.format(loccode),
        'key': '2053a52f388d44a2871d061597023802'
    }
    res = requests.post(url, data).json()
    forecastDatas = res['HeWeather5'][0]

    aqiInfo = forecastDatas['aqi']['city']
    update = '信息更新时间：' + forecastDatas['basic']['update']['loc'] + '\n'
    forecastInfo = forecastDatas['daily_forecast']
    suggestion = forecastDatas['suggestion']

    aqiList = ['——————————————————\n今日空气质量相关指数：']
    for key, value in aqiInfo.items():
        aqiList.append(hf_descripDict[key].ljust(10) + ':' + value)

    forecastList = ['——————————————————\n三天天气预报结果：']
    for i in forecastInfo:
        buffList = [i['date'], '白天:' + i['cond']['txt_d'], '夜间:' + i['cond']['txt_n'],
                    i['tmp']['min'] + '--' + i['tmp']['max'] + '℃',
                    i['wind']['dir'] + i['wind']['sc'] + '级']
        forecastList.append(' '.join(buffList))

    liveSuggesList = ['——————————————————\n今日相关生活指数:']
    for key, value in suggestion.items():
        liveSuggesList.append(hf_descripDict[key] + ':' + '\n' +
                              value['brf'] + '-----' + value['txt'])
    msg = update + '\n'.join(forecastList) + '\n' + \
          '\n'.join(aqiList) + '\n' + \
          '\n'.join(liveSuggesList) + '\n'
    print(msg)


class weatherForecast:
    def __init__(self, city):
        self.city = city

    # 获取城市对应的id
    def hf_get_code(self):
        code = {}
        url = 'https://api.heweather.com/v5/search'
        data = {
            'city': '{}'.format(self.city),
            'key': '2053a52f388d44a2871d061597023802'
        }
        res = requests.post(url, data).json()
        cityDatas = res['HeWeather5']
        for i in range(len(cityDatas)):
            cityInfo = cityDatas[i]['basic']
            key = cityInfo['prov'] + '--' + cityInfo['city']
            code[key] = cityInfo['id']
        return code

    # 利用城市id（唯一）获取相应的预报结果

if __name__ == '__main__':
    while True:
        loc = input('请输入查询点：\n')
        locCode = weatherForecast(loc).hf_get_code()
        # 根据输入的地区的id查询结果判断是否查询到和是否唯一，
        # 若查询到多个则提示将地区精细到县进行查询
        if len(locCode.keys()) < 1:
            print('未查询到{},请重新输入！'.format(loc))
            continue
        elif len(locCode.keys()) > 1:
            print('查询到多个{0}, 请重新输入，最好精确到县等,\n'
                  '查询到的{0}为：\n{1}'.format(loc, locCode))
            continue
        else:
            locCode = list(locCode.values())[0]
            hf_get_forecast(locCode)
            break
