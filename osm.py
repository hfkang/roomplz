import requests, pickle, datetime,sys,json 
from bs4 import BeautifulSoup

def search(query):
    campus = {}
    with open("SF_fulldata","rb") as f:
        campus['SF'] = pickle.load(f)
    with open("GB_fulldata","rb") as f:
        campus['GB'] = pickle.load(f)
    with open("BA_fulldata","rb") as f:
        campus['BA'] = pickle.load(f)

    #the dictionaries are not indexed in [day][hour]
    for day in range(7):
        for hour in range(16):
            for building in campus:
                for room in campus[building]:
                    if query in campus[building][room][hour][day]:
                        print(building+"in "+room+" at " + str(hour+7) + " on " +str(day))

 
    

def store_organized(building_name, building_data): 
    
    organized = organize(building_data)
    with open(building_name+"_organized","wb") as f:
        pickle.dump(organized, f)
    
    print(organized[4][13-7])  

def main(args):
    
    if "-d" == args[1]:
        if "GB" == args[2]:
            print("Will download GB")
            download("GB")
        if "BA" == args[2]:
            print("Will download BA")
            download("BA")
        if "SF" == args[2]:
            print("Will download SF")
            download("SF")   
    if "-engineering" == args[1]:
        download("BA")
        download("GB")
        download("SF")    

    if "-s" == args[1]:
        search(args[2])

def nitialize():
    #Pulls original room and building name data from OSM website. No longer needed if using Pickles
    osm_url = 'http://osm.utoronto.ca/bookings/f?p=200:3:::NO::P3_BLDG:'

    base_url = 'http://osm.utoronto.ca/bookings/f?p=200:5:284129947570601::::P5_BLDG,P5_ROOM,P5_CALENDAR_DATE:'
    
    testfile = requests.get(osm_url).text
    
    soup = BeautifulSoup(testfile,'lxml')


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
        soup = BeautifulSoup(html,'lxml')
        links = soup.find(None, id='P3_ROOM') 
        rooms = links.findAll('option')
        room_list = []  
        for room in rooms[1:]:
            room_list.append(room['value'])
        print(room_list)
        building_list[building].extend(room_list)
    
    print(building_list) 
    with open("BuildingandRooms","wb") as f:
        pickle.dump(building_list, f)

   
  

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

    with open("Building.json", "r") as f:
        room_list = json.load(f)
    
    data = loop_room(building_name,room_list[building_name]) 
    with open(building_name+"_fulldata", 'wb') as f:
        pickle.dump(data,f) 
    store_organized(building_name,data)  

def loop_room(building,room_list):
    #Iterates over the list of rooms in BA, and scrapes the booking data.
    base_url = 'http://osm.utoronto.ca/bookings/f?p=200:5:284129947570601::::P5_BLDG,P5_ROOM,P5_CALENDAR_DATE:'
    building = building
    i = datetime.datetime.now()
    date = i.strftime("%Y%m%d")
    


    building_data = {} #This dictionary holds the arrays that show a room's schedule this week
    
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
        periods = hour.findAll('div',{'class': 'calDragDrop'})
        for block in periods:
            if(block.text.strip() == ""):
                week.append("Empty")
            else:
                week.append(block.text.strip())
        room_sched.append(week)

    return room_sched  

def print_room(room_sched):
    for row in room_sched:
        for day in row:
            print(day,end=' | ')
        print()



if __name__=="__main__":
   main(sys.argv)
