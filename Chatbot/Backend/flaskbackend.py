
from re import fullmatch
from typing_extensions import final
from flask import Flask,json,request,render_template
import mysql.connector
import time

app = Flask(__name__)


def get_data_C(rcat):
  try :
    connection = mysql.connector.connect(host ="localhost", user = "root",passwd ="He@dshotkiller123")
    cursor = connection.cursor()
    all_info = [] #contains the data brought out of the database
    ngo_responses = []#will contain the individual accordian rich responses per ngo
    cursor.execute("show databases")
    all_states = cursor.fetchall()
    for state in all_states:
      cursor.execute("use {}".format(state[0]))
      for cat in rcat:
        try:
          base_query = "select * from ngo where Purpose like '%{}%'".format(cat)
          cursor.execute(base_query)
          all_info.extend(cursor.fetchall())
        except:
          pass

    ngo_responses.extend(create_accordion(all_info))
    dialogflow_response =(create_response(ngo_responses))
    return dialogflow_response

  except Exception as e:
    print(e)
    return {"fulfillmentMessages": [{"text": {"text": ["We ran into a problem. Try again later."]}}]}

  pass
#Category, State and City
def get_data_SCatc(rcat,rstate,rcity):
  try :
    connection = mysql.connector.connect(host ="localhost", user = "root",passwd ="He@dshotkiller123")
    cursor = connection.cursor()
    all_info = [] #contains the data brought out of the database
    ngo_responses = []#will contain the individual accordian rich responses per ngo
    cursor.execute("use {}".format(rstate[0].replace(" ","")))
    for cat in rcat:
      base_query = "select * from ngo where Purpose like '%{}%' and City = '{}'".format(cat,rcity[0])
      cursor.execute(base_query)
      all_info.extend(cursor.fetchall())
    ngo_responses.extend(create_accordion(all_info))
    dialogflow_response = create_response(ngo_responses)
    return dialogflow_response

  except Exception as e:
    print(e)
    return {"fulfillmentMessages": [{"text": {"text": ["We ran into a problem. Try again later."]}}]}


#Category and State.
def get_data_SCat(rcat,rstate):
  try :
    connection = mysql.connector.connect(host ="localhost", user = "root",passwd ="He@dshotkiller123")
    cursor = connection.cursor()
    all_info = [] #contains the data brought out of the database
    ngo_responses = []#will contain the individual accordian rich responses per ngo
    for state in rstate :
      cursor.execute("use {}".format(state.replace(" ","")))
      for cat in rcat:
        base_query = "select * from ngo where Purpose like '%{}%'".format(cat)
        cursor.execute(base_query)
        all_info.extend(cursor.fetchall())

    ngo_responses.extend(create_accordion(all_info))
    dialogflow_response = create_response(ngo_responses)
    return dialogflow_response

  except Exception as e:
    print(e)
    return {"fulfillmentMessages": [{"text": {"text": ["We ran into a problem. Try again later."]}}]}
  

#Category and City
def get_data_Catc(rcat,rcity):
  try :
    connection = mysql.connector.connect(host ="localhost", user = "root",passwd ="He@dshotkiller123")
    cursor = connection.cursor()
    all_info = [] #contains the data brought out of the database
    ngo_responses = []#will contain the individual accordian rich responses per ngo
    cursor.execute("show databases")
    all_states = cursor.fetchall()
    for state in all_states:
      cursor.execute("use {}".format(state[0]))
      for city in rcity :
        for cat in rcat:
          try:
            base_query = "select * from ngo where Purpose like '%{}%' and City = '{}'".format(cat,city)
            cursor.execute(base_query)
            all_info.extend(cursor.fetchall())
          except:
            pass

  

   
    ngo_responses.extend(create_accordion(all_info))
    dialogflow_response = create_response(ngo_responses)
    return dialogflow_response

  except Exception as e:
    print(e)
    return {"fulfillmentMessages": [{"text": {"text": ["We ran into a problem. Try again later."]}}]}

#generating accordion json objects for each ngo that was returned in some query
def create_accordion(ngo_data):
  temp_responses = []
  unique_ngos = list(set(ngo_data))
  for ngo in unique_ngos:
        #rich response object per ngo -[Accordion TYPE]
    info = {
            "type": "accordion",
            "text": "<b><i>Address</i></b> : {}</br><b><i>Email-Id</i></b> : {}</br><b><i>Phone</i></b> : {}</br><b><i>Telephone</i></b> : {}</br><b><i>Mobile</i></b> : {}</br><b><i>Purpose</i></b> : {}</br><b><i>Website : <a href = {} target = '_blank' rel='noopener noreferrer'>Visit Website</a> </b></i>".format(str(ngo[1]).strip(),str(ngo[3]).strip(),str(ngo[4]).strip(),str(ngo[5]).strip(),str(ngo[6]).strip(),str(ngo[7]).strip(),"'https://ngodarpan.gov.in/index.php/home/sectorwise'"),
            "title": "{}".format(ngo[0]),#title is ngo name
            "subtitle": "{}".format(ngo[2]) #subtitle here is State,City
            }
        #adding the final list to overall rich responses
    temp_responses.append(info)
  return temp_responses

#based on whether or not we could find returnable ngos we generate a response.
def create_response(ngo_accordions):
  if len(ngo_accordions) != 0 :
      #updating the final response Json
      return {"fulfillmentMessages": [{"text": {"text": ["Here's what I was able to find"]}},{"payload": {"richContent": [ngo_accordions,[{"type": "chips","options": [{"text": "Continue Searching"},{"text": "Take me back"}]}]]}}]}
  else:
      return {"fulfillmentMessages": [{"text": {"text": ["Sorry I wasn't able to find an NGO with these specifications"]}}]}



#route that handles the dialogflow webhook
@app.route('/dialogflow',methods =['POST'])
def db_search():
    req = request.get_json(silent = True, force = True) # parsing into json object
    print(req)

    #extracting information from the POST request
    query_result =  req.get('queryResult')
    if query_result.get('action') == "get.ngo": # if we have multiple possible requests being asked to the same endpoint then we need to uniquely identify what action is being done

        parsed_params = query_result.get('parameters')
        user_city = parsed_params.get('geo-city') #Location - City
        user_state = parsed_params.get('geo-state')#Location - State
        request_category = parsed_params.get('ngocats')#Category - Area of work of the NGO

        #for log purposes.
        print(user_city,user_state,request_category)

        #calling the required function based on the parameters we obtained in the query. Category is compulsory(ensured by DF)
        if len(user_state) != 0 and len(user_city) != 0 :
          final_response = get_data_SCatc(request_category,user_state,user_city)
        elif len(user_city) == 0 and len(user_state) != 0 :
          final_response = get_data_SCat(request_category,user_state)
        elif len(user_state) == 0 and len(user_city) !=0:
          final_response = get_data_Catc(request_category,user_city)
        elif len(user_city) ==0 and len(user_state) == 0 :
          final_response = get_data_C(request_category)
        else:
           return {"fulfillmentMessages": [{"text": {"text": ["We ran into a problem! Please try again in sometime!"]}}]}

        return final_response #auto formating response based on what we encounter in the code and then just returning either text or Rich based on what we get



#currently the testing website
@app.route('/home',methods =['POST','GET'])
def renderpage():
    return render_template("humanitytech.html")

if __name__ == "__main__":
    app.run(port =5000,debug = True)


  