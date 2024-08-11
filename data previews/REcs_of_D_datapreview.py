import pandas as pd
import xlrd
# Load Anime_data.csv
data1 = pd.read_csv("Anime_data.csv")
print(data1.head())
print(data1.columns)

# Load anime_Mal_data.csv
data2 = pd.read_excel("anime_Mal_data3.xlsx")
print(data2.head())
print(data2.columns)
#Removing unwanted columns
del data1["Popularity"]
del data1["Members"]
del data1["Link"]
del data1["Producer"]
del data1["Anime_id"]
print(data1.columns)
def data2_cleaning():
    del data2["anime_id"]
    del data2["anime_url"]
    del data2["synopsis"]
    del data2["type"]
    del data2["source_type"]
    del data2["num_episodes"]
    del data2["status"]
    del data2["start_date"]
    del data2["end_date"]
    del data2["season"]
    del data2["studios"]
    del data2["genres"]
    del data2["score_count"]
    del data2["score"]
    del data2["score_rank"]
    del data2["watching_count"]
    del data2["popularity_rank"]
    del data2["members_count"]
    del data2["favorites_count"]
    del data2["completed_count"]
    del data2["on_hold_count"]
    del data2["dropped_count"]
    del data2["plan_to_watch_count"]
    del data2["total_count"]
    del data2["score_10_count"]
    del data2["score_09_count"]
    del data2["score_08_count"]
    del data2["score_07_count"]
    del data2["score_06_count"]
    del data2["score_05_count"]
    del data2["score_04_count"]
    del data2["score_03_count"]
    del data2["score_02_count"]
    del data2["score_01_count"]
    del data2["pics"]
    del data2["clubs"]

data2_cleaning()
print(data2.columns)

# error = []
# error2 = 0
# usable_anime_titles = []
# for title in data1["Title"]:
#     for title2 in data2["title"]:
#         if title == title2:
#             usable_anime_titles.append(title)
#         else:
#             error.append(title)
#             error2 = error2 +1
# #print(usable_anime_titles)
# #print(error)
# print(error2)

#checking the count of the names
value_counts_result = data1['Title'].value_counts()

print(value_counts_result)
#cleaning the data and sorting in alphabetical order
##   REALLY IMPORTANT ##
data1.drop_duplicates(subset=['Title'], inplace=True)
data2.drop_duplicates(subset=['title'], inplace=True)

data2["title"] = data2["title"].str.replace(",", "").astype(int)

data1.sort_values(by="Title", inplace=True)
data2.sort_values(by= "title", inplace=True)
## REALLY IMPORTANT ##

#find the similar namesin both datasets and adding them to a list and also add th unmatched names to error_list
usable_anime_titles_ = set(data1["Title"]) & set(data2["title"])
error_ = set(data1["Title"]) - usable_anime_titles_

usable_anime_titles_ = list(usable_anime_titles_)
error_ = list(error_)

# print("Usable Anime Titles:", usable_anime_titles_)
# print("Error Titles:", error_)
print("Usable Anime Titles:", len(usable_anime_titles_))
print("Error Titles:", len(error_))
usable_anime_titles_.sort()
# making the lists for the datas
genres = []
Synopsies = []
Types = []
Studios = []
Ratings = []
Scoredbynumbers = []
Episodecount = []
Sources = []
Aired_date = []
image_urls = []
#filling the lists with the wanted data 
for title in data1["Title"] :
    if title in usable_anime_titles_:
        genres.append(data1.loc[data1["Title"] == title, "Genre"].values[0])
        Synopsies.append(data1.loc[data1["Title"] == title, "Synopsis"].values[0])
        Types.append(data1.loc[data1["Title"] == title, "Type"].values[0])
        Studios.append(data1.loc[data1["Title"] == title, "Studio"].values[0])
        Ratings.append(data1.loc[data1["Title"] == title, "Rating"].values[0])
        Scoredbynumbers.append(data1.loc[data1["Title"] == title, "ScoredBy"].values[0])
        Episodecount.append(data1.loc[data1["Title"] == title, "Episodes"].values[0])
        Sources.append(data1.loc[data1["Title"] == title, "Source"].values[0])
        Aired_date.append(data1.loc[data1["Title"] == title, "Aired"].values[0])
for title in data2["title"]:
    if title in usable_anime_titles_:
        image_urls.append(data2.loc[data2["title"] == title, "main_pic"].values[0])
# for Debugging
print("##############################################################")
print("usable_anime_titles: "+str(len(usable_anime_titles_)))
print("Genres: "+str(len(genres)))
print("Synopsies: "+str(len(Synopsies)))
print("Types: "+str(len(Types)))
print("Studios: "+str(len(Studios)))
print("Ratings: "+str(len(Ratings)))
print("ScoredbyNumbers: "+str(len(Scoredbynumbers)))
print("Episodecount: "+str(len(Episodecount)))
print("Sources: "+str(len(Sources)))
print("Aireddate: "+str(len(Aired_date)))
print("image URLs: "+str(len(image_urls)))


#creating the dictionary for the Dataframe
dataframe_data = {"Title":usable_anime_titles_ , "Genre": genres, "Synopsis": Synopsies, "Type":Types,"Studio":Studios,"Rating":Ratings,"Scoredby":Scoredbynumbers,"Episodes":Episodecount,"Source":Sources,"Aired": Aired_date,"Image_url":image_urls }
df = pd.DataFrame(dataframe_data)
print(df.head())
