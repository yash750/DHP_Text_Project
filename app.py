from flask import Flask, render_template, request
import psycopg2
import requests
import nltk
nltk.download('all')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import re
import json
from werkzeug.urls import url_quote


app = Flask(__name__)

# Making connection to database
conn = psycopg2.connect(database = "text_analysis",user = 'yash', password = 'uUx09LnYoYxhLckJry8uNTOm94X89ZSm', host = 'dpg-cnmn0euv3ddc73fkmfg0-a', port= 5432)

@app.route("/",methods=['GET', 'POST'])
def portal():
    return render_template("signin.html")

@app.route("/analyze",methods = ['POST'])
def analyze():
    if request.method == 'POST':
        cur = conn.cursor()
        URL = request.form['address']
        URL = str(URL)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content,'html.parser')

        title = soup.title.string

        editor_details_div=soup.find('div', class_='editor editor-date-logo editor-details-new-change')
        info_element = editor_details_div.find('div')  

        info = info_element.text.strip() if info_element else None

        h1 = soup.findAll('h1')
        h2 = soup.findAll('h2')
        h3 = soup.findAll('h3')
        p = soup.findAll('p')

        head = ''
        para=[]

        for i in h1:
            cleantext = re.sub(r'<.*?>','',str(i))
            head = head + cleantext+'\n'
        for j in h2:
            c = re.sub(r'<.*?>','',str(j))
            head = head + c +'\n'
        for k in h3:
            d = re.sub(r'<.*?>','',str(k))
            head = head + d +'\n'

        filtered_sentence = []
        sent = 0
        words = 0
        stop_words = set(stopwords.words('english'))
        for z in p:
            e = re.sub(r'<.*?>','',str(z))
            para.append(e.strip())
            sent = sent + 1
            for w in word_tokenize(e.strip()):
                words = words+len(word_tokenize(e.strip()))
                if w not in stop_words:
                    filtered_sentence.append(w)
            filtered_sentence.append('\n')

        result_string = ' '.join(filtered_sentence)
        stop = words - len(filtered_sentence)
        num_stopwords = stop

        pos_dict = {}
        for i in para:
            word_list = word_tokenize(i) 
            x = nltk.pos_tag(word_list, tagset='universal')
            for i in x:
                if i[1] in pos_dict:
                    pos_dict[i[1]] += 1
                else:
                    pos_dict[i[1]] = 1
    
        with open("pos_dict.json", 'w'):
            # Use json.dump() to write the dictionary to the file
                a = json.dumps(pos_dict)
        cur.execute('''
            CREATE TABLE IF NOT EXISTS DETAILS (
            id serial PRIMARY KEY,
            url VARCHAR,
            no_of_words INT,
            no_of_sentences INT,
            content varchar,
            no_of_stopwords INT,
            headlines VARCHAR,
            postages varchar,
            other_info varchar)''')
        
        cur.execute(
            '''INSERT INTO DETAILS \
                (url,no_of_words,no_of_sentences,content,no_of_stopwords,headlines,postages,other_info) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
                (URL,words,sent,result_string,num_stopwords,head,a,info))
        
        cur.execute('''SELECT no_of_words,no_of_sentences,postages,headlines,content,other_info  FROM DETAILS ORDER BY ID DESC LIMIT 1''')
        data = cur.fetchall()
        conn.commit()   
        cur.close()

        return render_template('details.html',data = data)
    

@app.route("/admin",methods=['GET',"POST"])
def admin():
    #if request.method == 'POST':
        return render_template('verify.html')
    
@app.route("/verify_admin",methods = ["POST"])
def verify_admin():
    code = 'yash1234'
    if request.method == "POST":
        password = request.form['password']
        if password == code:
            cur = conn.cursor()
            cur.execute('''SELECT ID , URL FROM DETAILS ''')
            urls = cur.fetchall()

            conn.commit()
            cur.close()

            return render_template("url_view.html", urls = urls)
        
        else:
            return render_template('verify.html')

@app.route("/viewdetail/<id>",methods=["GET","POST"])
def viewdetail(id):
    cur = conn.cursor()
    cur.execute('''SELECT no_of_words,no_of_sentences,postages,headlines,content  FROM DETAILS where id = %s''',(id,))
    data = cur.fetchall()

    return render_template('details.html',data = data)



# Handling sign in page.
@app.route("/signin",methods=["POST"])
def signin():
    #if request.method == 'POST':
    # return {"le": 8787}
    return render_template('index.html')

@app.route("/index",methods=["GET", "POST"])
def index():
    #if request.method == 'POST':
    # return {"le": 8787}
    return render_template('index.html')



if __name__=='__main__':
    app.run(debug=True, port=8000)
    conn.close()
    
