import flask
from flask import Flask, render_template, request, redirect
import urllib2
from socket import gethostname, gethostbyname
import json

app = Flask(__name__)

baseURL = "http://api.indeed.com/ads/apisearch?publisher=9327050513995141&format=json&q="
#add in search parameter


def getUserAgent():
    header = str(request.headers.get('User-Agent'))
    print header
    useragent = ""
    for i in header:
        if i == ' ':
            break
        else:
            useragent += i
    return useragent

def getIP():
    return gethostbyname(gethostname())

@app.route('/', methods= ['GET','POST'])
def getJobData():
    #base url
    #need to add query to the end


    #mapping will be from company to a listing
    #so, a Dict
    #IF the result is nothing i.e. DoD has no job listings
    #it will be from
    allCompanies = ["Doctors on Demand"]
    allCompanies.append("Inkling")
    allCompanies.append("Instacart")
    allCompanies.append("Medallia")
    allCompanies.append("Thumbtack")
    allCompanies.append("Airbnb")
    allCompanies.append("Delphix")
    allCompanies.append("ClearSlide")
    allCompanies.append("Anki")
    allCompanies.append("Slack")
    allCompanies.append("StackExchange")
    allCompanies.append("Stripe")
    allCompanies.append("Shapeways")
    allCompanies.append("RobinHood")

    companyList = []
    for i in allCompanies:
         data = getJsonResponse(i)
         if (data[2] != 0):
             data.append(i)
             companyList.append(data)



    #default sort by relevance
    #perhaps users want to see a page within the radius of their
    #location
    return render_template('template.html', list = companyList)


def getJsonResponse(company):
    url = baseURL
    companyFormat = ""
    for i in company:
        if i == " ":
            companyFormat += "%20"
        else:
            companyFormat += i
    url += companyFormat
    url += "&limit=" + getLimit()
    url += "&latlong=1&co=us&userip="
    url += getIP()
    url += "&useragent=" + getUserAgent() + "&v=2"
    webUrl = urllib2.urlopen(url)
    counter = 0
    if webUrl.getcode() == 200:
        data = webUrl.read()
        result = json.loads(data)
        #total raw results
        data = [str(result["totalResults"])]
        allJobs = []
        for i in range (0, len(result["results"])):
            #need to check if the name of the company corresponds with the job site
            #listing
            if company == str(result["results"][i]["company"]) :
                job = [str(result["results"][i]["jobtitle"])]
                job.append(str(result["results"][i]["company"]))
                job.append(str(result["results"][i]["city"]))
                job.append(str(result["results"][i]["state"]))
                job.append(result["results"][i]["snippet"])
                job.append(str(result["results"][i]["url"]))
                job.append(str(result["results"][i]["formattedRelativeTime"]))
                counter+=1
                allJobs.append(job)
        data.append(allJobs)
    else:
        return "invalidUrl"
    data.append(counter)
    return data

def getLimit():
    return "30"


if __name__ == "__main__":
    app.run()
