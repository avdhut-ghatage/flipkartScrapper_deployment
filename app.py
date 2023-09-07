from flask import Flask
from flask import render_template, request,jsonify, got_request_exception
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import datetime
#logging.basicConfig(filename="scrapper.log" , level=logging.INFO, format="%(asctime)s")

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url= "https://www.flipkart.com/search?q="+searchString
            uclient=uReq(flipkart_url)
            flipkartPage= uclient.read()
            uclient.close()
            flipkart_html= bs(flipkartPage, "html.parser")
            bigboxes=flipkart_html.findAll("div",{"class":"_1AtVbE col-12-12"})
            count=True
            reviews = []
            
            fw= open("Search_history.csv", "a")
            ct = datetime.datetime.now()
            fw.write(f"{searchString} : {ct}\n")

            for box in bigboxes:
                try:
                    try:
                        title=box.find_all("a",{"class":"IRpwTa"})[0]["title"],box.find_all("div",{"class":"_3eWWd-"})[0].text
            
                    except IndexError:
                        try:
                            title=box.find_all("div",{"class":"_2WkVRV"})[0].text,box.find_all("a",{"class":"IRpwTa"})[0]["title"]  
                        except:
                            try:
                                title=box.find_all("div",{"class":"_4rR01T"})[0].text

                            except:
                                title=box.find_all("a",{"class":"s1Q9rs"})[0]["title"]


                    try:   
                        rating=box.find_all("div",{"class":"_3LWZlK"})[0].text
                    except:
                        rating="No Rating"
                    price=box.find_all("div",{"class":"_30jeq3"})[0].text

                    mydict={"Product":searchString, "Name": title,"Rating":rating, "Price":price}
                    reviews.append(mydict)
                    count=False
                    
                except:
                    if count ==True:
                        del bigboxes[0]
                    else:
                        break
        
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0")
