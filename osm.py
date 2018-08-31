import requests, pickle, datetime,sys,json, os
from bs4 import BeautifulSoup
import boto3

bucket = None


blist = ['BA','SF','GB','MS','RS','WB','MP']

def search(query):
    campus = {}

    for b in blist:
        with open(b + "_fulldata", "rb") as f:
            campus[b] = pickle.load(f)

    #the dictionaries are not indexed in [day][hour]
    for hour in range(16):
        for day in range(7):
            for building in campus:
                for room in campus[building]:
                    if query in campus[building][room][hour][day]:

                        print(building+"in "+room+" at " + str(hour+7) + " on " +str(day))

 
    

def store_organized(building_name, building_data): 
    organized = organize(building_data)
    filename = building_name+"_organized.json"
    filepath = '/tmp/'+filename
    with open(filepath,"w") as f:
        json.dump(organized, f)


    client = boto3.client('s3')
    client.upload_file(filepath, 'roomplz-data', filename)

    print("Done uploading " + filename)

def main(args):
    
    if "-d" in args:
        if "GB" == args[2]:
            print("Will download GB")
            download("GB")
        if "BA" == args[2]:
            print("Will download BA")
            download("BA")
        if "SF" == args[2]:
            print("Will download SF")
            download("SF")   
        if "MS" == args[2]:
            print("Will download MS")
            download("MS")

    else:
        for b in blist:
            download(b)


def nitialize():
    #Pulls original room and building name data from OSM website. No longer needed if using Pickles
    osm_url = 'https://www.ace.utoronto.ca/ws/f?p=200:3:::NO::P3_BLDG:'

    testfile = requests.get(osm_url).text
    
    soup = BeautifulSoup(testfile)


     #Extract Building Names    
    building_table = soup.find(None,id='P3_BLDG')
    buildings = building_table.findAll('option')
    building_list = {}
    for b in buildings[1:]:
        building_list[b['value']] = [] #setup dictionary 
    print(building_list)
 
    for building in building_list:
        url = osm_url+building
        print(url)
        html = requests.get(url).text
        soup = BeautifulSoup(html)
        links = soup.find(None, id='P3_ROOM') 
        rooms = links.findAll('option')
        room_list = []  
        for room in rooms[1:]:
            room_list.append(room['value'])
        print(room_list)
        building_list[building].extend(room_list)
    
    print(building_list) 
    with open("BuildingandRooms.json","w") as f:
        json.dump(building_list, f)

   
  

def organize(building_data):
   
    master = [[dict() for i in range(16)] for j in range(7)]

    #at this stage we take the all of the room data for a whole building and compile it.
    # we're also inverting the data structure from 16 by 7 to 7 by 16 because it's a more sensible hierarchy
    #change iteration to by day from 22 to 7.
    for room_key in building_data:
        print("compiling data for " + room_key)  
        room = building_data[room_key] 
        for day in range(7): #get a one hour block across a week
            for hour in range(15,-1,-1):  # get a particular block in a week  
                if(room[hour][day]=="Empty"): 
                    if hour < 15: 
                        #check next hour to see if open
                        if room_key in master[day][hour+1]:
                            #THe room is free in the next hour. increment duration
                            master[day][hour][room_key] = master[day][hour+1][room_key]+1
                        else:
                            master[day][hour][room_key] = 1
                   
                    else:  
                        master[day][hour][room_key] = 1
                   # master[day][hour].append(room_key) #append room name to directory of free rooms aka master if the room is empty at that tiem
    return master 

def download(building_name): 

    # To update room_list, run nitialize function
    room_list = {"AB": ["107", "114"], "AH": ["100", "103", "105", "107", "108", "302", "304", "306", "400", "402"], "AP": ["120", "124"], "BA": ["1130", "1160", "1170", "1180", "1190", "1200", "1210", "1220", "1230", "1240", "2135", "2139", "2145", "2155", "2159", "2165", "2175", "2179", "2185", "2195", "3008", "3116", "B024", "B025", "B026"], "BC": ["20"], "BF": ["214", "215", "315", "316", "323"], "BI": ["131"], "BL": ["112", "113", "114", "205", "305", "306", "312", "313", "325", "327"], "BR": ["200"], "BT": ["101"], "BW": ["DH", "PDR", "SCR"], "CB": ["114"], "CR": ["103", "106", "107", "403", "404", "405", "406"], "EM": ["001", "105", "108", "119", "203", "205", "302", "319"], "ES": ["1016M", "1050", "4000", "4001", "B142", "B149"], "EX": ["100", "200", "300", "310", "320"], "FG": ["103", "129", "139", "77"], "GB": ["119", "120", "220", "221", "244", "248", "303", "304", "404", "405"], "GI": ["---"], "HA": ["316", "401", "403", "409", "410"], "HI": ["CART"], "HS": ["100", "106", "108", "610", "614", "618", "696", "705", "715"], "IN": ["204", "209", "223", "312", "313"], "KP": ["108", "113"], "LA": ["211", "212", "213", "214", "248", "340", "341"], "LM": ["123", "155", "157", "158", "159", "161", "162"], "MB": ["128"], "MC": ["102", "252", "254"], "MP": ["102", "103", "118", "134", "137", "202", "203"], "MS": ["2158", "2170", "2172", "2173", "2290", "2394", "3153", "3154", "3278", "3290", "4171", "4279"], "MU": ["108N", "154S", "202N", "208N", "23N", "260S", "302N", "61S", "63S"], "MY": ["150", "315", "330", "350", "360", "370", "380", "420", "430", "440", "480", "490"], "NF": ["003", "004", "006", "007", "008", "009", "113", "119", "205", "231", "235", "332"], "NL": ["6"], "OI": ["10200", "10204", "11200", "11204", "2198", "2199", "2205", "2211", "2212", "2214", "2227", "2279", "2281", "2286", "2289", "2295", "2296", "3310", "3311", "3312", "4410", "4414", "4416", "4418", "4420", "4426", "5150", "5160", "5170", "5230", "5240", "5250", "5260", "5270", "5280", "5290", "7192", "8170", "8180", "8200", "8201", "8214", "8220", "8280", "C154", "G162"], "RL": ["14190"], "RS": ["208", "211", "310"], "RT": ["---", "100", "1007", "1065", "127", "133", "134", "134A", "134B", "134C", "134D", "134E", "134F", "134G", "134H", "142", "147", "151", "157", "2015", "2030", "2050D", "2060", "2062", "2064", "2066", "2068", "2070", "2072", "2074", "2076", "2078", "2080", "2082", "2084", "2086", "2088", "287", "3003", "3005", "3007", "3009", "3011", "3013", "3015", "3017", "3062", "3064", "3066", "3068", "3070", "3072", "3074", "3076", "3078", "3080", "3082", "3084", "3086", "3090", "3094", "3096", "3097", "3098", "354", "368", "371B", "371C", "374", "392", "394", "4001", "4005", "4057", "448", "470", "5037", "548", "570", "6024", "7024", "8024", "9005", "L1010", "L1020", "L1025", "L1030", "L1035", "L1043", "L1045", "L1047", "L1049", "L1051", "L1058", "L1060", "M1041", "M1043", "M1045", "M1047", "M1049", "M1051"], "RU": ["1016", "132", "140", "150", "201", "203", "205", "207", "218", "220", "222", "224", "230", "232", "234", "235", "236", "238", "240", "251", "255", "256", "420", "428", "444", "453", "490A", "490B", "490C", "490D", "490E", "490F", "720", "721", "727", "730", "738", "740", "744", "750", "753", "758", "759", "841", "907", "954"], "RW": ["110", "117", "140", "142", "143"], "SF": ["1101", "1105", "2202", "3202"], "SK": ["100", "114", "218", "222", "346", "348", "418", "548", "702", "720"], "SS": ["1069", "1070", "1071", "1072", "1073", "1074", "1078", "1080", "1083", "1084", "1085", "1086", "1087", "1088", "2101", "2102", "2104", "2105", "2106", "2108", "2110", "2111", "2112", "2114", "2116", "2117", "2118", "2119", "2120", "2125", "2127", "2135", "581"], "TC": ["22", "24"], "TF": ["101", "102", "103", "2", "200", "201", "202", "203"], "UC": ["140", "144", "148", "152", "161", "163", "175", "177", "179", "244", "248", "255", "256", "257", "261", "330", "44", "51", "52", "53", "55", "57", "63", "65", "67", "69", "85", "87", "A101", "B203", "D301", "F204"], "VC": ["101", "112", "115", "206", "211", "212", "213", "215", "304", "323", "FOY1"], "WB": ["116", "119", "130", "219"], "WE": ["69", "74", "75", "76"], "WI": ["1016", "1017", "2006", "523", "524"], "WO": ["20", "25", "30", "35"], "WW": ["119", "120", "121", "126"]}

    data = loop_room(building_name,room_list[building_name]) 
    store_organized(building_name,data)

def loop_room(building,room_list):
    #Iterates over the list of rooms in BA, and scrapes the booking data.
    base_url = 'https://www.ace.utoronto.ca/ws/f?p=200:5:::::P5_BLDG,P5_ROOM,P5_CALENDAR_DATE:'

    i = datetime.datetime.now()
    date = i.strftime("%Y%m%d")
    building_data = {}
    # This dictionary holds the arrays that show a room's schedule this week
    
    for room in room_list:
        request_url = base_url + building +','+ room +','+ date
        print(request_url) 
        r = requests.get(request_url).text
        sched = parse_room(r)
        building_data[room] = sched #Store the parsed schedule in the dictionary, with the room number as key
        print_room(sched) 
        print("****\n") 
    
    
    return building_data


def parse_room(html):
    more_soup = BeautifulSoup(html)
    booking = more_soup.find('table',attrs =  {'class': 't3SmallWeekCalendar'}) 

    day = booking.findAll('tr')
    room_sched = []
    for hour in day[2:]:
        week = [] 
        periods = hour.findAll('td')
        for block in periods:
            if(block.text.strip() == ""):
                week.append("Empty")
            else:
                week.append(block.text.strip())
        room_sched.append(week)

    return room_sched  

def print_room(room_sched):
    
    for row in room_sched:
        print("| ",end="")
        for day in row:
            if day == "Empty":
                print("     ",end = " | ")
            else:
                print(day.strip()[:5],end=' | ')
        print()


def init_s3():
    client = boto3.client('s3')
    response = client.list_buckets()
    print(response)
    for b in response['Buckets']:
        if b['Name'] == 'roomplz-data':
            break
    else:
        response = client.create_bucket(
            ACL= "private",
            Bucket= "roomplz-data",
            CreateBucketConfiguration= {
                "LocationConstraint": "us-west-2"
            }
        )
        print(response)



if __name__=="__main__":
    main(sys.argv)
#nitialize()

    # init_s3()