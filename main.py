import urllib.request
import json
import datetime
h = open("header.txt",'r')
xmls = h.read()
h.close()
add = datetime.timedelta(days=1)
d = datetime.datetime.now() + datetime.timedelta(hours=15)
end = d + datetime.timedelta(days=7)
now = d
print(end)
file = open("epg.xml","w",encoding='utf8')
file.write(xmls)
while now <= end:
    print(now)
    date = now.year.__str__() + '{0:02}'.format(now.month) + '{0:02}'.format(now.day)
    print(date)
    urlstr = "https://tvguide.myjcom.jp/api/getEpgInfo/?channels=2_1024_32736_20201017%2C2_1040_32738_20201017%2C2_1064_32741_20201017%2C2_1048_32739_20201017%2C2_1072_32742_20201017%2C2_1056_32740_20201017%2C2_23608_32391_20201017%2C3_103_4_20201017%2C3_141_4_20201017%2C3_151_4_20201017%2C3_161_4_20201017%2C3_171_4_20201017%2C3_181_4_20201017&rectime=&rec4k="
    urlstr = urlstr.replace("20201017",date)

    req = urllib.request.Request(urlstr, headers={'User-Agent' : "Magic Browser"})
    jreq = urllib.request.urlopen(req)
    jstr = jreq.read().decode("UTF-8")

    j = json.loads(jstr)
    for x in j.items():
        for y in x:
            for i in y:
                if i.__str__()[0] == '{':
                    progtemp = "<programme start=\"20201017002500 +0900\" stop=\"20201017003000 +0900\" channel=\"21 Junior AL\">\n<title lang=\"jp\">Title</title>\n<desc lang=\"jp\">Describe</desc>\n<category lang=\"jp\">Category</category>\n</programme>\n"
                    cn = i['channelName']
                    cn = cn.replace("NHK東京\u3000総合", "NHK G")
                    cn = cn.replace("フジテレビ", "Fuji TV")
                    cn = cn.replace("日本テレビ", "Nippon TV")
                    cn = cn.replace("テレビ朝日", "TV Asahi")
                    cn = cn.replace("テレビ東京", "TV Tokyo")
                    cn = cn.replace("ＮＨＫＢＳプレミアム", "NHK Premium")
                    cn = cn.replace("ＢＳ日テレ", "BS NTV")
                    cn = cn.replace("ＢＳ朝日１", "BS Asahi")
                    cn = cn.replace("ＢＳ－ＴＢＳ", "BS TBS")
                    cn = cn.replace("BSテレ東", "BS TV Tokyo")
                    cn = cn.replace("ＢＳフジ・181", "BS Fuji")
                    progtemp = progtemp.replace("20201017002500",i['programStart'].__str__())
                    progtemp = progtemp.replace("20201017003000", i['programEnd'].__str__())
                    progtemp = progtemp.replace("21 Junior AL", cn)
                    progtemp = progtemp.replace("Title", i['title'].replace("<","[").replace(">","]").replace("&","&amp;").replace("'","&apos;").replace('"',"&quot;"))
                    progtemp = progtemp.replace("Describe", i['commentary'].replace("<","[").replace(">","]").replace("&","&amp;").replace("'","&apos;").replace('"',"&quot;"))
                    progtemp = progtemp.replace("Category", i['duration'].__str__())
                    file.write(progtemp)
    now = now + add
file.write("\n</tv>")
file.close()



