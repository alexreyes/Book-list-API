# importing the requests library 
import requests 
  
# api-endpoint 
URL = "https://reyes-personal-website-api.herokuapp.com/book2019"

r = requests.get(url = URL) 
  
# extracting data in json format 
data = r.json() 
print(data)
  
# api-endpoint  
URL = "https://reyes-personal-website-api.herokuapp.com/book2019/update"

r = requests.get(url = URL) 
  
# extracting data in json format 
print(r)
  