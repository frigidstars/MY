import requests
from bs4 import BeautifulSoup
import pprint
import json
import csv


my_104T = ["職稱", "公司名稱", "工作內容", "職務類別", "工作待遇", "工作地點", "學歷要求", "工作經歷", "科系要求",
             "語文條件", "擅長工具", "工作技能", "其他條件", "福利制度", "聯絡人"]
with open("my104.csv", mode="w", newline="", encoding="Big5") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(my_104T)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

keyword = "CNC" # input("請輸入想找的工作: ")
for page in range(1,11):
    print("/////////////////////////////////////////")
    url = "https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}&order=15&asc=0&page={}&mode=s&jobsource=2018indexpoc".format(keyword,page)


    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")
    # print(soup.prettify())

    mytitle = soup.select('h2[class="b-tit"] a')
    # print(mytitle)
    # n=0
    for a in mytitle:
        print("==============================================")
        Title = a.text
        article_url = "https://www.104.com.tw/job/ajax/content/"+a["href"].split("//")[1].split("?")[0].split("/")[2]
        print(Title)
        print(article_url)

        a_res = requests.get(article_url, headers=headers)
        json_d = json.loads(a_res.text, encoding="utf-8")
        # pprint.pprint(json_d)
        weblist = json_d["data"]
        # pprint.pprint(weblist)


        # 職稱
        jobName = weblist["header"]["jobName"]
        # 公司名稱
        custName = weblist["header"]["custName"]
        # 工作內容
        jobDescription = weblist["jobDetail"]["jobDescription"]
        # 職務類別
        industry = weblist["industry"]
        # 工作待遇
        salary = weblist["jobDetail"]["salary"]
        # 學歷要求
        edu = weblist["condition"]["edu"]
        # 其他條件
        other = "\n" + weblist["condition"]["other"]
        # 工作經歷
        workExp = weblist["condition"]["workExp"]
        # 工作地點
        addressRegion = weblist["jobDetail"]["addressRegion"]
        # 福利制度
        welfare = "\n" + weblist["welfare"]["welfare"]
        # 聯絡人
        hrName = "聯絡人: " + weblist["contact"]["hrName"] + "\n"
        email = "聯絡email:" + weblist["contact"]["email"] + "\n"
        phone = "聯絡電話: " + weblist["contact"]["phone"] + "\n"
        connect = hrName + email + phone


        # 擅長工具
        def spe():
            specialty_r = weblist["condition"]["specialty"]
            n = 0
            for a in specialty_r:
                n += 1
                yield str(n) + ". " + a["description"]


        specialty = ",".join(list(spe())).replace(",", "\n")  # 將 list 變成 string 型式後，所有","用換行符號取代


        # 語文條件
        def lan():
            language_r = weblist["condition"]["language"]
            n = 0
            for b in language_r:
                n += 1
                yield b["language"] + ":" + b["ability"]
        language = ",".join(list(lan())).replace(",", "\n")


        # 科系要求
        def maj():
            major_r = weblist["condition"]["major"]
            for c in major_r:
                yield c
        major = ",".join(list(maj())).replace(",", "\n")


        # 工作技能
        def ski():
            skill_r = weblist["condition"]["skill"]
            for d in skill_r:
                yield d["description"]
        skill = ",".join(list(ski())).replace(",", "\n")

        my_104 = [jobName, custName, jobDescription, industry, salary, addressRegion, edu, workExp, major, language,
                  specialty, skill, other, welfare, connect]
        try:
            with open("my104.csv", mode="a", newline="", encoding="Big5", errors="ignore") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(my_104)
                print("寫入成功")
        except:
            pass









