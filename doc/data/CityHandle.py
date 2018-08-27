

"""
    使用脚本实现数据导入
        将JSON的内容存储到数据库

        把JSON的内容读取出来
        把读出来的数据写入到数据库中


"""
import json

import pymysql


def json_to_db():
    # 连接数据库
    client = pymysql.Connect(user='root', password='rock1204', host='127.0.0.1', port=3306, db='Python1803Tpp', charset="utf8")

    cursor = client.cursor()

    with open("Cities.json", "r") as cities:
        cities_info = cities.read()
        load_json = json.loads(cities_info)
        returnValue = load_json.get('returnValue')
        # print(returnValue)

        city_letters = returnValue.keys()

        # print(city_letters)

        for key in city_letters:
            print(key)
            # 存储字母

            print(cursor.execute("INSERT INTO letter(letter) VALUE ('%s');" % key))

            client.commit()

            cursor.execute("SELECT * FROM letter WHERE letter='%s';" % key)

            client.commit()

            letter_id = cursor.fetchone()[0]

            letter_cities = returnValue.get(key)
            # print(letter_cities)

            for letter_city in letter_cities:
                # print(letter_city)
                city_id = letter_city.get("id")
                city_regionName = letter_city.get("regionName")
                city_cityCode = letter_city.get("cityCode")
                city_pinYin = letter_city.get("pinYin")

                print(city_id, city_regionName, city_cityCode, city_pinYin)

                cursor.execute("INSERT INTO city(id, regionName, cityCode, pinYin, c_letter) VALUE (%d, '%s', %d, '%s', %d);" % (city_id, city_regionName, city_cityCode, city_pinYin, letter_id))

                client.commit()

    cursor.close()

    client.close()


if __name__ == '__main__':
    json_to_db()


