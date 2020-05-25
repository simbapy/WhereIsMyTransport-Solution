import os
import json
import re
import time

def extract_data(source_dir, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        for name in files:
            with open(os.path.join(root,name), 'r', encoding='utf-8') as file:
                data = json.load(file)
            calls = []
            for log in data:
                if log["responseStatusCode"] == 200 or log["responseStatusCode"] == 201:
                    if re.search("journeys",log["requestUri"]):
                        call_type = "journeys"
                        content = json.loads(log['responseContentBody'])
                        try:
                            origin = content['geometry']['coordinates'][0]
                        except KeyError:
                            origin = content['legs'][0]['geometry']['coordinates'][0]
                        try:
                            destination = content['geometry']['coordinates'][1]
                        except KeyError:
                            destination = content['legs'][-1]['geometry']['coordinates'][-1]
                        try:
                            modes = content['only']['modes']
                        except KeyError:
                            modes = []
                            for leg in content['legs']:
                                if leg['type'] == 'Walking':
                                    pass
                                else:
                                    modes.append(leg['line']['mode'])
                        try:
                            total_travel_time = content['itineraries'][0]['duration']
                        except IndexError:
                            total_travel_time = None
                        except KeyError:
                            total_travel_time = content['duration']
                        timestamp = log['requestTimestamp']

                        event = {
                                    "Type": call_type,
                                    "Data": {
                                        "Origin": origin,
                                        "Destination": destination,
                                        "Modes_Used": modes,
                                        "Total_Travel_Time": total_travel_time,
                                        "Timestamp": timestamp
                                    }
                                }
                        calls.append(event)
                    elif re.search("api/stops/([A-Za-z]+[\d]+[\w]*|[\d]+[A-Za-z]+[\w]*|(\d+)|(\w+))/timetables",log["requestUri"]):
                        call_type = 'timetables'
                        content = json.loads(log['responseContentBody'])
                        try:
                            agency_id = content[0]['line']['agency']['id']
                            agency_name = content[0]['line']['agency']['name']
                        except IndexError:
                            try:
                                agency_id = content['agency']['id']
                                agency_name = content['agency']['name']
                            except KeyError:
                                continue
                            except TypeError:
                                continue
                        
                        timestamp = log['requestTimestamp']

                        event = {
                                    "Type": call_type,
                                    "Data": {
                                        "AgencyName": agency_name,
                                        "AgencyID": agency_id,
                                        "Timestamp": timestamp
                                    }
                                }
                        calls.append(event)
                    elif re.search("stops",log["requestUri"]) and not re.search("timetables",log["requestUri"]):
                        call_type = 'stops'
                        content = json.loads(log['responseContentBody'])
                        try:
                            agency_id = content['agency']['id']
                        except TypeError:
                            try:
                                agency_id = content[0]['agency']['id']
                            except IndexError:
                                continue
                        try:
                            agency_name = content['agency']['name']
                        except TypeError:
                            agency_name = content[0]['agency']['name']
                        try:
                            if content['geometry']['type'] == 'MultiPoint':
                                num_stops = len(content['geometry']['coordinates'])
                            else:
                                num_stops = 1
                        except TypeError:
                            if content[0]['geometry']['type'] == 'MultiPoint':
                                num_stops = len(content[0]['geometry']['coordinates'])
                            else:
                                num_stops = 1
                        timestamp = log['requestTimestamp']

                        event = {
                                    "Type": call_type,
                                    "Data": {
                                        "AgencyName": agency_name,
                                        "AgencyID": agency_id,
                                        "NumberOfStops": num_stops,
                                        "Timestamp": timestamp
                                    }
                                }
                        calls.append(event)
                    else:
                        continue

                else:
                    continue
            
            try:
                timestamp = timestamp.replace(":","-")
                if len(calls) >0:
                    with open(os.path.join(destination_dir,"Calls-{}.json".format(timestamp)), "w") as file:
                        #json.dumps(calls, indent=4, sort_keys=True)
                        json.dump(calls, file, ensure_ascii=False, indent=4)
                else:
                    raise UnboundLocalError
            except UnboundLocalError:
                continue
            
        


if __name__ == "__main__":
    source_dir = r"" # path-to-folder-with-logs-you-wish-to-summarize
    destination_dir = r"" # path-to-folder-you-wish-to-save-json-summaries
    extract_data(source_dir, destination_dir)
    