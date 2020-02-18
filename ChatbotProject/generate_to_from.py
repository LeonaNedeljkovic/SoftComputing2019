import sqlite3
import pandas as pd

timeframes='2006-03'

connection=sqlite3.connect('data\\databaseChatbot.db')
c=connection.cursor()
limit=5000
last_unix=0
cur_length=limit
counter=0
test_done=False
while cur_length==limit:
    df=pd.read_sql("SELECT * FROM parent_reply WHERE unix>{} AND parent NOT NULL AND parent!='False' AND score>0 ORDER BY unix ASC LIMIT {}".format(last_unix,limit),connection)
    last_unix=df.tail(1)['unix'].values[0]
    cur_length=len(df)
    if not test_done:
        with open("data\\from.txt",'a',encoding='utf8') as f:
            for content in df['parent'].values:
                f.write(str(content)+'\n')
        with open("data\\to.txt", 'a', encoding='utf8') as f:
            for content in df['comment'].values:
                f.write(str(content) + '\n')
        test_done=True
    else:
        with open("data\\from.txt",'a',encoding='utf8') as f:
            for content in df['parent'].values:
                f.write(str(content)+'\n')
        with open("data\\to.txt", 'a', encoding='utf8') as f:
            for content in df['comment'].values:
                f.write(str(content) + '\n')
    counter+=1
    if counter%20==0:
        print(counter*limit,'rows completed')

