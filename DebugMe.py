import requests

user = 19

r = requests.get("http://212.73.217.202:15020/raspberry/get_user/"+str(user))
result = r.json()
data = result["user"][0]
#print(data["user_id"])



print("result")
print(result)
print("\n")
print("data")
print(data)
print("\n")

print(result["user"][0])
