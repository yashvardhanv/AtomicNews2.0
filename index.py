# A very simple Flask Hello World app for you to get started with...
from newsapi import NewsApiClient
from googletrans import Translator
# from time import sleep
# from newspaper.article import ArticleException, ArticleDownloadState
from newspaper import Article
from newspaper import Config
from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)
art = NewsApiClient(api_key='470a655fe44541d9a294810c9444edd9')
all_art = art.get_top_headlines()
articles = all_art['articles']


@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        topic= request.form['topic']
        return redirect(url_for('search',topic=topic))
    else:

        return render_template('home.html',articles=articles)


@app.route("/article",methods=['GET'])
def article():
    if request.method == 'POST':
        topic= request.form['topic']
        return redirect(url_for('search',topic=topic))
    else:
        url = str(request.args.get("art"))
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        config = Config()
        config.browser_user_agent = user_agent
        article = Article(url,config=config)
        article.download()
        article.parse()
        article.nlp()
        # print("ERRORS IN PARSING ARTICLE")
        return render_template('article.html', title='Article',article=article)

@app.route("/translated",methods=['GET'])
def translated():
    if request.method == 'POST':
        topic= request.form['topic']
        return redirect(url_for('search',topic=topic))
    else:
        url = str(request.args.get("url"))
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        config = Config()
        config.browser_user_agent = user_agent
        article = Article(url,config=config)
        article.download()
        article.parse()
        article.nlp()
        l1=[]
        tr = Translator()
        l1.append(tr.translate(str(article.title),dest='hi').text)
        l1.append(tr.translate(str(article.summary),dest='hi').text)
        l1.append(article.top_image)
        l1.append(article.authors)
        # print("ERRORS IN PARSING ARTICLE")
        return render_template('translate.html', title='Hindi',article=l1)

@app.route("/India",methods=['GET','POST'])
def India():
    if request.method == 'POST':
        topic= request.form['topic']
        return redirect(url_for('search',topic=topic))
    else:
        art_india = art.get_top_headlines(country='in')
        art_india = art_india['articles']
        return render_template('india.html',articles=art_india)

@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        topic= request.form['topic']
        return redirect(url_for('search',topic=topic))
    else:
        return render_template('contact.html')

@app.route("/<topic>",methods=['GET','POST'])
def search(topic):
    if request.method == 'POST':
        topic= request.form['topic']
        return redirect(url_for('search',topic=topic))
    else:
        topic= str(topic)

        topic_art = art.get_everything(q=topic,language='en',sort_by='relevancy',page=1)
        topic_art = topic_art['articles']
        return render_template('search.html',articles=topic_art)