import os
import datetime as dt1
import calendar as cl1

def read1( file1 ):
    with open( file1, 'r', encoding='utf-8' ) as f1:
        str1 = f1.read()
    return str1

def write1( file1, str1 ):
    with open( file1, 'w', encoding='utf-8' ) as f1:
        f1.write( str1 )
    return 0

def generate_calendar1( y1, m1 ):
    cal1 = [""]*42
    date1 = dt1.date( y1, m1, 1 )
    wd1 = date1.weekday()              # weekday 0-6   Mon-Sun
    if wd1 > 5:
        wd1 = wd1 - 7
    wd1 = wd1 + 1
    cal_max1 = cl1.monthrange( y1, m1 )[1]
    for i1 in range( cal_max1 ):
        str1 = str( i1+1 )
        i2 = i1 + wd1
        cal1[i2] = str1
    return wd1, cal1

def generate_calendars(y1, m1, str0, count):
    for i1 in range( 12 ): 
        str1 = generate_html1( y1, m1, str0 ) 
        file1 = path1 + "calendar/calendar_" + str(y1) + f'{m1:02}' + ".html" 
        write1( file1, str1 ) 
        y1, m1 = prev_next1( 1, y1, m1 ) 

def get_schedule1(y1, m1, cal1, wd1, str0 ):

    # カレンダー情報を格納用リスト生成
    cal2 = [""]*len( cal1 )
    # print(cal1)

    # スケジュール実行ファイルを1行ずつ格納
    a1 = str0.split( "\n" )

    # スケジュール実行ファイルを1行ずつ読み込む
    for i1 in range( len( a1 ) ):

        # 実行ファイル1行のデータを時間と文言に分割
        a2 = a1[i1].strip().split( " " )

        # 時間を年月日週で分割
        a3 = a2[0].split( "/" )

        # 年月日週が正しく入力されている場合
        if len( a3 ) == 4:

          # 年月日週を取得
            y2,m2,d2,w2 = a3[0],a3[1],a3[2],a3[3]

            # 年に「*」または数値が入力されている場合
            if "*" in y2 or int( y2 ) == y1:
                # 月に「*」または数値が入力されている場合
                if "*" in m2 or int( m2 ) == m1:

                    # 日付と1行のデータを取得
                    d1,a4 = a3[2],a2

                    # 1行のデータから文言データを抽出
                    del a4[0]
                    str1 = str( " ".join( a4 ) ).strip()

                    # 日に「*」が入力されている場合
                    if d2 == "*":

                      # 週に「*」または数値が入力されている場合
                      if w2 == "*":
                        for index in range(len(cal2)):
                          cal2[index] += str1 + "<br>"

                      # 数値が入っていれば週で実行
                      else:

                        # 7日で割ったあまりで判定（1:月曜日,2:火曜日,3:水曜日,4:木曜日,5:金曜日,6:土曜日,7:日曜日）
                        for index in range(len(cal2)):
                          if index % 7 == int(w2):
                            cal2[index] += str1 + "<br>"

                    # 日に数値が入力されている場合
                    else:
                      cal2[ int(d1)-1 + wd1 ] = cal2[ int(d1)-1 + wd1 ] + str1 + "<br>"

    cal3 = []
    for i1 in range( len( cal1 ) ):
      try:
        if int(cal1[i1]) > 0:
          cal3.append( cal1[i1] )
          cal3.append( cal2[i1] )
      except:
        cal3.append( "" )
        cal3.append( "" )

    return cal3

def generate_ymd1():
    now1 = dt1.datetime.now()
    y1 = now1.year
    m1 = now1.month
    d1 = now1.day
    return y1, m1, d1

def prev_next1( n1, y1, m1 ):
    m2 = m1 + n1
    y2 = y1 + m2//12
    m2 = m2%12
    if m2 == 0:
        y2 = y2 - 1
        m2 = 12
    return y2, m2

def generate_html1( y1, m1, str0 ):
    wd1, cal1 = generate_calendar1( y1, m1 )
    cal2 = get_schedule1( y1, m1, cal1, wd1, str0 )
    str1 = generate_html0( y1, m1, cal2 )
    return str1

def generate_html0( y1, m1, cal1 ):
    m0 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ]
    y2, m2 = prev_next1( -1, y1, m1 )
    prev1 = str( y2 ) + f'{m2:02}'
    y2, m2 = prev_next1(  1, y1, m1 )
    next1 = str( y2 ) + f'{m2:02}'
    str1 = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>crawling_calendar</title>
  <style media="screen">
.header0 {{
  height: 30px;
  line-height: 30px;
  text-align: left;
  font-size: 40px;
  padding: 10px;
  margin: 0;
  display: inline-block;
  _display: inline;
  font-weight: bold;
}}
table {{
  table-layout: fixed;
  width: 100%;
}}
th {{
  text-align: center;
  padding: 0px;
}}
td {{
  text-align: left;
  vertical-align: top;
  padding: 5px;
  height: 60px;
}}
.calendar0 {{
  background: #EEEEE8;
}}
.header1 {{
  font-size: 13px;
  padding: 5px;
}}
.calendar_table1 {{
  height: 60%;
  padding: 5px;
}}
.days1 {{
  background: #FFFFFF;
}}
.day1 {{
  font-weight: bold;
  font-size: 14px;
}}
.content1 {{
  border-radius: 5px;
  background: #F0FFF0;
  font-size: 14px;
  font-family: 'Meiryo UI';
  color: #000000;
}}
.w1 {{
  color: #FF0000;
  background: #FFF0F0;
}}
.w7 {{
  color: #0000A0;
  background: #F6F0FF;
}}
  </style>
</head>
<body class="calendar0">
  <div class="calendar1">
    <table>
      <tr>
        <td>
          <div class="header0">{_str01} </div>{_str02} {_str03}
        </td>
        <td></td>
        <td></td>
        <td>
          <a href = "./calendar_{_str04}.html">先月</a>
          <a href = "./calendar_{_str05}.html">来月</a><br>
        </td>
      </tr>
    </table>
'''.format( _str01 = m1, _str02 = y1, _str03 = m0[m1-1], _str04 = prev1, _str05 = next1 ).strip()

    str2 = '''
    <table class="header1">
      <tr>
        <th>Sunday</th>
        <th>Monday</th>
        <th>Tuesday</th>
        <th>Wednesday</th>
        <th>Thursday</th>
        <th>Friday</th>
        <th>Saturday</th>
      </tr>
    </table>
    <table class="calendar_table1">
      <tr class="days1">
        <td class = w1><div class=day1>{0[0]}</div><cr><div class=content1>{0[1]}</div></td>
        <td class = w2><div class=day1>{0[2]}</div><cr><div class=content1>{0[3]}</div></td>
        <td class = w3><div class=day1>{0[4]}</div><cr><div class=content1>{0[5]}</div></td>
        <td class = w4><div class=day1>{0[6]}</div><cr><div class=content1>{0[7]}</div></td>
        <td class = w5><div class=day1>{0[8]}</div><cr><div class=content1>{0[9]}</div></td>
        <td class = w6><div class=day1>{0[10]}</div><cr><div class=content1>{0[11]}</div></td>
        <td class = w7><div class=day1>{0[12]}</div><cr><div class=content1>{0[13]}</div></td>
      </tr>
      <tr class="days1">
        <td class = w1><div class=day1>{0[14]}</div><cr><div class=content1>{0[15]}</div></td>
        <td class = w2><div class=day1>{0[16]}</div><cr><div class=content1>{0[17]}</div></td>
        <td class = w3><div class=day1>{0[18]}</div><cr><div class=content1>{0[19]}</div></td>
        <td class = w4><div class=day1>{0[20]}</div><cr><div class=content1>{0[21]}</div></td>
        <td class = w5><div class=day1>{0[22]}</div><cr><div class=content1>{0[23]}</div></td>
        <td class = w6><div class=day1>{0[24]}</div><cr><div class=content1>{0[25]}</div></td>
        <td class = w7><div class=day1>{0[26]}</div><cr><div class=content1>{0[27]}</div></td>
      </tr>
      <tr class="days1">
        <td class = w1><div class=day1>{0[28]}</div><cr><div class=content1>{0[29]}</div></td>
        <td class = w2><div class=day1>{0[30]}</div><cr><div class=content1>{0[31]}</div></td>
        <td class = w3><div class=day1>{0[32]}</div><cr><div class=content1>{0[33]}</div></td>
        <td class = w4><div class=day1>{0[34]}</div><cr><div class=content1>{0[35]}</div></td>
        <td class = w5><div class=day1>{0[36]}</div><cr><div class=content1>{0[37]}</div></td>
        <td class = w6><div class=day1>{0[38]}</div><cr><div class=content1>{0[39]}</div></td>
        <td class = w7><div class=day1>{0[40]}</div><cr><div class=content1>{0[41]}</div></td>
      </tr>
      <tr class="days1">
        <td class = w1><div class=day1>{0[42]}</div><cr><div class=content1>{0[43]}</div></td>
        <td class = w2><div class=day1>{0[44]}</div><cr><div class=content1>{0[45]}</div></td>
        <td class = w3><div class=day1>{0[46]}</div><cr><div class=content1>{0[47]}</div></td>
        <td class = w4><div class=day1>{0[48]}</div><cr><div class=content1>{0[49]}</div></td>
        <td class = w5><div class=day1>{0[50]}</div><cr><div class=content1>{0[51]}</div></td>
        <td class = w6><div class=day1>{0[52]}</div><cr><div class=content1>{0[53]}</div></td>
        <td class = w7><div class=day1>{0[54]}</div><cr><div class=content1>{0[55]}</div></td>
      </tr>
      <tr class="days1">
        <td class = w1><div class=day1>{0[56]}</div><cr><div class=content1>{0[57]}</div></td>
        <td class = w2><div class=day1>{0[58]}</div><cr><div class=content1>{0[59]}</div></td>
        <td class = w3><div class=day1>{0[60]}</div><cr><div class=content1>{0[61]}</div></td>
        <td class = w4><div class=day1>{0[62]}</div><cr><div class=content1>{0[63]}</div></td>
        <td class = w5><div class=day1>{0[64]}</div><cr><div class=content1>{0[65]}</div></td>
        <td class = w6><div class=day1>{0[66]}</div><cr><div class=content1>{0[67]}</div></td>
        <td class = w7><div class=day1>{0[68]}</div><cr><div class=content1>{0[69]}</div></td>
      </tr>
      <tr class="days1">
        <td class = w1><div class=day1>{0[70]}</div><cr><div class=content1>{0[71]}</div></td>
        <td class = w2><div class=day1>{0[72]}</div><cr><div class=content1>{0[73]}</div></td>
        <td class = w3><div class=day1>{0[74]}</div><cr><div class=content1>{0[75]}</div></td>
        <td class = w4><div class=day1>{0[76]}</div><cr><div class=content1>{0[77]}</div></td>
        <td class = w5><div class=day1>{0[78]}</div><cr><div class=content1>{0[79]}</div></td>
        <td class = w6><div class=day1>{0[80]}</div><cr><div class=content1>{0[81]}</div></td>
        <td class = w7><div class=day1>{0[82]}</div><cr><div class=content1>{0[83]}</div></td>
      </tr>
    </table>
  </div>
</body>
</html>
'''.format( cal1 ).strip()
    return str1 + str2

path1 = os.path.dirname(__file__) + "/var/www/bs-tool/crawling_calendar/"
str0 = read1( path1 + "schedule.txt"  )

y1, m1, d1 = generate_ymd1()

str1 = generate_html1( y1, m1, str0 )

file1 = path1 + "calendar/calendar.html"
write1( file1, str1 )

generate_calendars(y1, m1, str0, 12)

y1, m1 = prev_next1( -12, y1, m1 ) 

generate_calendars(y1, m1, str0, 12)
