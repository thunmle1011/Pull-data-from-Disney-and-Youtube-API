import requests
import csv
import json

#funtion to pull data from disney api
def disneyApi():
    url = "https://api.disneyapi.dev/characters"

    #page pagination
    params = {"page": "1"}

    #header for dataset
    header = ["films", "shortFilms", "tvShows", "videoGames", "parkAttractions", "allies", "enemies", "_id", "name", "url"]
    data = []

    #loop through all pages to get dataset
    for i in range(1, 150):

        params["page"] = i

        response = requests.get(url, params=params)
        characterData = response.json()

        #get data features
        for character in characterData["data"]:
            characters = [character["films"], character["shortFilms"], character["tvShows"], character["videoGames"], character["parkAttractions"],
            character["allies"], character["enemies"], character["_id"], character["name"], character["url"]]
            data.append(characters)

    #write data to csv file
    with open ("disneyCharacter.csv", "w", encoding="UTF-8", newline="") as csvWriter:
            writer = csv.writer(csvWriter)
            writer.writerow(header)
            writer.writerows(data)
            csvWriter.close()

#pull data by youtube api
def youtubeApi():
    #api key
    API_KEY = "AIzaSyDV0cSu-cRaia6FM7i-ijAusY4KOZs2bXE"
    CHANNEL_ID = "UC79Gv3mYp6zKiSwYemEik9A" #channel id for DataCamp channel
    #playlist for uploads video from DataCamp
    PLAYLIST_ID = "UU79Gv3mYp6zKiSwYemEik9A"


    nextPageToken = ""

    morePages = True
    videoIds = []

    #loop through all pages to get videoId
    while morePages == True:
        if nextPageToken is None:
            morePages = False
        else:
            url1 = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId={}&key={}&pageToken={}".format(PLAYLIST_ID, API_KEY, nextPageToken)

            IdData =  json.loads(requests.get(url1).text)
            #get videoId
            for item in IdData["items"]:
                videoIds.append(item["contentDetails"]["videoId"])
            nextPageToken = IdData.get("nextPageToken")

    #headers for dataset
    header = ["video_id", "title", "publishedAt", "viewCount", "likeCount"]
    videoList = []

    #loop through all videoIds to get details
    for i in range (len(videoIds)):
        url2 = "https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}".format(videoIds[i], API_KEY)
        
        data = json.loads(requests.get(url2).text)

        #get dataset features
        for item in data["items"]:
            videoDetails = [item["id"], item["snippet"]["title"], item["snippet"]["publishedAt"], item["statistics"]["viewCount"], item["statistics"]["likeCount"]]
            
        videoList.append(videoDetails)

    #write to csv file 
    with open ("videosDetailsFromDataCampChannel.csv", "w", encoding="UTF-8", newline="") as csvWriter:
        writer = csv.writer(csvWriter)
        writer.writerow(header)
        writer.writerows(videoList)
        csvWriter.close()


# function to display menu
def displayMenuBar():
    print("----------------Menu----------------")
    print("1. Pull data from disney api")
    print("2. Pull data from youtube api")
    print("3. Exit")
    print("------------------------------------")

#main program
# call display menu function
displayMenuBar()

# promp user to enter choice
choice = int(input("Enter your choice: "))

# corresponding tasks with choices
while(choice!=3):
    if (choice==1):
        print()
        disneyApi()
    elif (choice==2):
        print()
        youtubeApi()
    else:
        print("Invalid choice")
    print()
    displayMenuBar()
    choice = int(input("Enter your choice: "))
