import requests, pickle, datetime,sys
from bs4 import BeautifulSoup, SoupStrainer
def store_organized(building_name, building_data): 
    
    organized = organize(building_data)
    with open(building_name+"_organized","wb") as f:
        pickle.dump(organized, f) 

def main(args):
    #download_BA()   #only download when you actually need to update the data   
    building = "BA"
    time = "14" 
    print("You requested a room in "+building+" at "+time) 
        
    """
    with open("BA_organized",'rb') as f:
        availability = pickle.load(f)
    print(availability)     
    
    if(building == "BA"):
        if(True):
             print(availability[1][(int(time))-7]) 
        else: 
            print("invalid time")
    else:
        print("Invalid buidling") 
        
    """
    download_BA() 
    with open("BA_fulldata",'rb') as f:
        BA_data = pickle.load(f)
       
    #preorganized data in format [hour][day]
    room = BA_data['2155']
    for hour in room:
        print(hour[3]) 
        
    
def nitialize():
    #Pulls original room and building name data from OSM website. No longer needed if using Pickles
    osm_url = 'http://osm.utoronto.ca/bookings/f?p=200:3:::NO::P3_BLDG:BA'

    base_url = 'http://osm.utoronto.ca/bookings/f?p=200:5:284129947570601::::P5_BLDG,P5_ROOM,P5_CALENDAR_DATE:'
    testfile = open('osm.utoronto.ca/bookings/osm.html','r').read()
    soup = BeautifulSoup(testfile,'lxml')


     #Extract Building Names    
    building_table = soup.find(None,id='P3_BLDG')
    buildings = building_table.findAll('option')
    building_list = []
    for b in buildings[1:]:
        building_list.append(b['value'])
    print(building_list)
    with open("BuildingList",'rb') as f:
        pickle.dump(building_list,f)
 

    #Extract Room Names for BA 
    links = soup.find(None, id='P3_ROOM') 
    rooms = links.findAll('option')
    room_list = []  
    for room in rooms[1:]:
        room_list.append(room['value'])
    print(room_list)

    #Save the file. Nomally i'd do this in a loop over all buildings, but i can probably do manually and for select
    #buildings for now 
    pickle.dump(room_list, open( "BA.p", "wb" ) )


    loop_room(room_list) 
"""
    test_url = base_url + "BA," + rooms[4]['value']+ ",20151115"

    print(test_url)

    r = requests.get(test_url).text
    parse_room(r)
"""

def organize(building_data):
   
    master = [[[] for i in range(16)] for j in range(7)]

    #at this stage we take the all of the room data for a whole building and compile it.
    # we're also inverting the data structure from 16 by 7 to 7 by 16 because it's a more sensible hierarchy
    for room_key in building_data: 
        room = building_data[room_key] 
        for hour in range(16): #get a one hour block across a week
            for day in range(7):  # get a particular block in a week  
                if(room[hour][day]=="Empty"): 
                    master[day][hour].append(room_key) #append room name to directory of free rooms aka master if the room is empty at that tiem
    return master 

def download_BA(): 

    with open("BA.p", "rb") as f:
        room_list = pickle.load(f)
    
    BA_data = loop_room(room_list) 
    with open("BA_fulldata", 'wb') as f:
        pickle.dump(BA_data,f) 
    store_organized("BA",BA_data)  

def loop_room(room_list):
    #Iterates over the list of rooms in BA, and scrapes the booking data.
    base_url = 'http://osm.utoronto.ca/bookings/f?p=200:5:284129947570601::::P5_BLDG,P5_ROOM,P5_CALENDAR_DATE:'
    building = 'BA'
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
