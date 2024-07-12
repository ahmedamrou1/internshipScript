from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
from os.path import join, dirname
import smtplib, ssl
from email.message import EmailMessage
from dotenv import load_dotenv

"""
Before use, create a .env file and structure it like .env.example for proper SMTP access

If you are not on a Mac, remove the notifyLocal function call shown below
"""

def notifyLocal(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

def notifyEmail(company):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        mail = EmailMessage()
        mail['from'] = mail['to'] = email
        mail['subject'] = f"Github posting: {company}"
        mail.set_content(f"A new internship has been posted to GitHub: {company}. View it here: {url}")
        print(mail)
        server.login(email, password)
        server.send_message(mail, email, email)

dotenv_path = join(dirname(__file__), '.env') #get path of .env file
load_dotenv(dotenv_path) #load env variables to your system
email = os.environ.get("EMAILADDRESS") 
password = os.environ.get("EMAILPASS") #you thought I would hardcode my password???

url = 'https://github.com/Ouckah/Summer2025-Internships/blob/main/README.md'
firstRun = True #var to load in companies list without emailing recepient the first time
port = 465 #SSL
companies = [] #stores company names

while True:
    with urlopen(url) as response:
        soup = BeautifulSoup(response, 'html.parser') 
        for row in soup.find_all('tr'): #for each table row on the readme page of this GitHub repo
            company = row.find('td') #find the first table data tag which contains the company name
            if company and company.contents[0] != "↳": #ignore multiple listings for the same company
                if company.contents[0] not in companies: #if this company has not been added to companies list
                    if not firstRun: #ignore the first run which is just for initializing the list
                        notifyLocal("New intern posting", company.contents[0] + "\n" + url) #remove this if not on Mac
                        notifyEmail(company.contents[0]) #send an email to your specified account
                    companies.append(company.contents[0]) #add the company to the list
        print(companies)
        if companies: #if the first run is over and companies were added, begin notification process for new lisitings
            firstRun = False
        sleep(120) #repeat every 2 minutes