import json 
import os 
import requests
import random
import time

# mainPath = r"C:\Users\rahul-al\Desktop\New Asana JSON\Done"
# access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkzNjMzNDk0LCJpYXQiOjE2OTM1NDcwOTQsImp0aSI6ImZlYTA0ZjEwYmFhMTRjNDE5MGI4MjgwYjgzZDNkY2U2IiwidXNlcl9pZCI6IjAwNTU3NjA5LTFhOTQtNDI0Yy04ZGYxLWVlNzk2ZTk5NGU5MCJ9.r5SLiFBFOELop_C_s4XqnOmrqYfAqzXrXRcS-FSsCRo"


# headers = {
#     "Authorization": "Bearer " + access,
#     # "Content-Type": "multipart/form-data;boundary=---WebKitFormBoundary7MA4YWxkTrZu0gW"
# }


# # userID = "327d31ee-2132-422e-bafe-7935397e2426"
# userID = "e347ceae-0d61-4661-8cd5-748b30d9708e"    # local
# workoutId = "40c5cc3d-8083-489e-a5d8-bb96d51bbd07"   # morning

# mainURL = "http://localhost:8000"
# # mainURL = "https://api.cimpl-yoga.atomicloops.link"
# createAsanaURL = mainURL + "/yoga/asana/"
# linkAsanaToWorkoutURL = mainURL + "/yoga/workout-asana/multiple-create/"
# postlogURL = mainURL + "/yoga/metrics/"
# logateachstepURL = mainURL + "/logs/"

# workasanaList = []
# jsonlist = os.listdir(mainPath)

# mainvectorPath = r"C:\Users\rahul-al\Desktop\New Asana JSON\Yoga Vector\Yoga Vector"

# vectorList = os.listdir(mainvectorPath)

# print(vectorList)



# #  creating asana 
# for asana in jsonlist:
#     try:
#         cpath = mainPath + "\\" + asana
#         vectorPath = mainvectorPath + "\\" + asana.split(".")[0]  + ".svg"
#         print("For asana: ", asana)
#         if asana.endswith(".json") == False:
#             raise Exception(f"{asana} Not a json file")
#         with open(cpath, "r") as jsonFile:
#             jsondata = json.load(jsonFile)
#         # workasanaList.append({
#         #     "asanaId": data["id"],
#         #     "workoutId": workoutId
#         # })
#         otherNames = jsondata["metadata"]["otherNames"]
#         family = jsondata["metadata"]["family"]
#         family = family.replace(" ", "")
#         senddata = {
#             "name": jsondata["name"],
#             "otherNames": ",".join(otherNames) if otherNames else "",
#             "family": family.capitalize()
#             # "data": data
#             # "file": jsondata.read()
#         }
#         # with open(cpath, 'r') as json_file:
#         #     senddata['file'] = json_file.read()
#         # print(senddata)
#         files = {'file': (asana, open(cpath, 'rb')), 'imgFile': (asana.split(".")[0] + ".svg", open(vectorPath, 'rb'))}
#         # res = requests.post(createAsanaURL, headers=headers, data=senddata)
#         res = requests.post(createAsanaURL, headers=headers, data=senddata, files=files)
#         # res = requests.post(createAsanaURL, headers=headers, json=data)
#         html = res.text
#         if res.status_code != 201:
#             print("DATA: ", senddata)
#             raise Exception("Error in creating asana: " + html)
#         resJson = res.json()
#         asanaId = resJson["data"]["id"]
#         workasanaList.append({
#             "asanaId": asanaId,
#             "workoutId": workoutId
#         })


#         #  generating random logs 
#         jsondata = resJson["data"]["data"]["steps"]
#         print("Has ", len(jsondata), " steps")
#         for index,step in enumerate(jsondata):
#             allAngles = step["angles"]
#             tth = step["timeToHold"]
#             angleData = []
#             for _ in range(tth):
#                 tempData = []
#                 for angle in allAngles:
#                     minval = angle["tolerance"]["lower"]
#                     maxval = angle["tolerance"]["upper"]
#                     randomval = random.randint(minval, maxval)
#                     # print(f"Step: {index+1}, Angle: {angle['comments']}, Value: {randomval} tth: {tth}")
#                     tempData.append(randomval)
#                 angleData.append(tempData)
#             # print(angleData)
#             res = requests.post(logateachstepURL, headers=headers, json={
#                 "userId": userID,
#                 "workoutId": workoutId,
#                 "asanaId": asanaId,
#                 "data" : {
#                     "stepNumber": index+1,
#                     "allAngles": angleData
#                 }
#             })
#             if res.status_code != 201:
#                 raise Exception("Error in logging data: " + html)
#             if len(jsondata) > 1:
#                 # print("Success in logging data for step: ", index+1 , " for asana: ", asanaId)
#                 sleepTime = int(random.randint(0, int(tth*2.5)))
#                 time.sleep(tth  + sleepTime)

#         res = requests.post(postlogURL, headers=headers, json={
#             "userId": userID,
#             "workoutId": workoutId,
#             "asanaId": asanaId
#         })
#         print(res.text)
#         # break
#     except Exception as e:
#         print(f"Error in creating {asana}: ", e)
#         continue



# #  linking asanas to workout
# res  = requests.post(linkAsanaToWorkoutURL, headers=headers, json=workasanaList)
# html = res.text
# if res.status_code != 201:
#     raise Exception("Error in linking asana to workout: " + html)
# else:
#     print("Success in linking asana to workout")




data = {"name": "Vrikshasana", "steps": [{"name": "step 1", "angles": [{"value": 230, "vertex": ["RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"], "comments": "right_hand", "tolerance": {"lower": 200, "upper": 245}}, {"value": 130, "vertex": ["LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST"], "comments": "left_hand", "tolerance": {"lower": 110, "upper": 150}}, {"value": 173, "vertex": ["RIGHT_WRIST", "RIGHT_SHOULDER", "RIGHT_HIP"], "comments": "right_wrist_shoulder_hip", "tolerance": {"lower": 143, "upper": 193}}, {"value": 196, "vertex": ["LEFT_WRIST", "LEFT_SHOULDER", "LEFT_HIP"], "comments": "left_wrist_shoulder_hip", "tolerance": {"lower": 176, "upper": 216}}, {"value": 235, "vertex": ["RIGHT_SHOULDER", "RIGHT_HIP", "RIGHT_KNEE"], "comments": "right_shoulder_hip_knee", "tolerance": {"lower": 215, "upper": 275}}, {"value": 179, "vertex": ["LEFT_SHOULDER", "LEFT_HIP", "LEFT_KNEE"], "comments": "left_shoulder_hip_knee", "tolerance": {"lower": 159, "upper": 199}}, {"value": 179, "vertex": ["LEFT_SHOULDER", "LEFT_HIP", "LEFT_ANKLE"], "comments": "left_shoulder_hip_ankle", "tolerance": {"lower": 159, "upper": 199}}, {"value": 34, "vertex": ["RIGHT_HIP", "RIGHT_KNEE", "RIGHT_ANKLE"], "comments": "right_lower_body", "tolerance": {"lower": 14, "upper": 54}}, {"value": 178, "vertex": ["LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE"], "comments": "left_lower_body", "tolerance": {"lower": 158, "upper": 210}}, {"value": 191, "vertex": ["RIGHT_ELBOW", "RIGHT_SHOULDER", "RIGHT_HIP"], "comments": "right_elbow_shoulder_hip", "tolerance": {"lower": 171, "upper": 220}}, {"value": 188, "vertex": ["LEFT_ELBOW", "LEFT_SHOULDER", "LEFT_HIP"], "comments": "left_elbow_shoulder_hip", "tolerance": {"lower": 155, "upper": 208}}, {"value": 172, "vertex": ["LEFT_ANKLE", "LEFT_HIP", "LEFT_WRIST"], "comments": "left_ankle_hip_wrist", "tolerance": {"lower": 152, "upper": 192}}, {"value": 33, "vertex": ["LEFT_ANKLE", "LEFT_HIP", "RIGHT_ANKLE"], "comments": "left_right_leg", "tolerance": {"lower": 13, "upper": 53}}, {"value": 30, "vertex": ["LEFT_SHOULDER", "LEFT_WRIST", "RIGHT_SHOULDER"], "comments": "left_right_hand_angle", "tolerance": {"lower": 10, "upper": 50}}], "imageURL": "https://www.arhantayoga.org/wp-content/uploads/2022/03/Tree-Pose-%E2%80%93-Vrikshasana.jpg", "timeToHold": 5, "instructions": "left foot to the floor , while the right foot is placed on the left thigh.  Both hands should be joined together in the Namaskar Mudra (prayer pose) on above head"}], "metadata": {"do": "DESC", "svg": "https://yoga-ai-cimpl-dev.s3.ap-south-1.amazonaws.com/yoga-ai/yoga-vector/Vrikshasana.svg", "dont": "DESC", "time": 5, "level": "Beginner", "family": "standing", "demoUrl": "https://youtu.be/qpuY0jXimtQ", "otherNames": ["Plough Pose, Plow Pose"], "description": "Angushtamadhye or Angushta Ma Dyai"}}




def random_logs_generator(jsonData):
    timeToHold = jsonData["timeToHold"]
    angles = jsonData["angles"]
    angleData = []
    for _ in range(timeToHold):
        tempData = []
        for angle in angles:
            minval = angle["tolerance"]["lower"]
            maxval = angle["tolerance"]["upper"]
            randomval = random.randint(minval, maxval)
            tempData.append(randomval)
        angleData.append(tempData)
    return angleData


print(random_logs_generator(data["steps"][0]))