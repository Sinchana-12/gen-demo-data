import json
import random
from pymongo import MongoClient
from bson import ObjectId
from collections import OrderedDict
from datetime import datetime, timedelta
from itertools import cycle

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["jano_core"]
collection = db["dls_session"]

# Target patient IDs
target_ids = [
    "685cf29e04a6c318938015f1", "685cf29f04a6c31893801620", "685cf2a004a6c3189380164f",
    "685cf2a104a6c3189380167e", "685cf2a104a6c318938016ad", "685cf2a304a6c318938016dc",
    "685cf2a304a6c3189380170b", "685cf2a504a6c31893801743", "685cf2a604a6c31893801772",
    "685cf2a604a6c318938017a1", "685cf2a704a6c318938017d0", "685cf2a804a6c318938017ff",
    "685cf2a904a6c3189380182e", "685cf2aa04a6c3189380185d", "685cf2aa04a6c3189380188c",
    "685cf2ab04a6c318938018bb", "685cf2ac04a6c318938018ea", "685cf2ad04a6c31893801919",
    "685cf2e704a6c31893801948"
]

# Load users data
with open("C:/Users/sinch/OneDrive/Desktop/collection_data/jano_core.users.json", encoding="utf-8") as f:
    all_users = json.load(f)

allowed_names = {"Dr. Prasad", "Shwetha Kumari", "Mahesh R", "Sumitha Lho", "Manjula SG"}
limited_users = [
    {"_id": u["_id"]["$oid"], "name": u["name"]}
    for u in all_users
    if u.get("name") in allowed_names and "_id" in u and "$oid" in u["_id"]
]

if len(limited_users) < 5:
    raise ValueError("Not enough allowed users to generate event pairs and consulting team roles.")

event_users = [limited_users[0], limited_users[1]]
event_user_cycler = cycle(event_users)

user_pairs = cycle([
    (limited_users[0], limited_users[1]),
    (limited_users[2], limited_users[3]),
    (limited_users[4], limited_users[0]),
])

org_id = "685005ce50ffc4656f440162"
team_id = "685005ce50ffc4656f440169"

# Load patients data
with open("C:/Users/sinch/OneDrive/Desktop/collection_data/jano_core.patients.json", encoding="utf-8") as f:
    patients = json.load(f)

# Load schedule data
with open("C:/Users/sinch/OneDrive/Desktop/collection_data/jano_core.reno_aptmt_schedule.json", encoding="utf-8") as f:
    schedule_data = json.load(f)

selected_schedule_ids = []
for i, schedule_entry in enumerate(schedule_data):
    if i < 3:
        selected_schedule_ids.append(str(schedule_entry["_id"]["$oid"]))
    else:
        break

schedule_id_cycler = cycle(selected_schedule_ids)

unique_stations = []
seen_station_ids = set()
for schedule_entry in schedule_data:
    for appointment in schedule_entry.get("appointments", []):
        station = appointment.get("station")
        if station and station.get("id") and station.get("code"):
            station_id_str = str(station["id"]["$oid"])
            if station_id_str not in seen_station_ids:
                unique_stations.append({
                    "id": station_id_str,
                    "code": station["code"]
                })
                seen_station_ids.add(station_id_str)

if not unique_stations:
    raise ValueError("No unique stations found in schedule data.")

timeslots = [
    {"start": "6", "end": "11"},
    {"start": "11", "end": "16"},
    {"start": "16", "end": "21"}
]

event_labels_cycle = cycle(["check_in", "in_progress", "resumed", "complete", "post"])
base_event_time = datetime.fromisoformat('2025-06-18T11:49:14.067+00:00')

inserted_count = 0

for patient in patients:
    pid = patient.get("_id", {}).get("$oid")
    if pid in target_ids:
        try:
            _id = ObjectId(pid)

            data_id_int = int.from_bytes(_id.binary, 'big') - 1
            data_id = ObjectId(data_id_int.to_bytes(12, 'big'))

            user1_for_consulting, user2_for_consulting = next(user_pairs)

            doc = OrderedDict()
            doc["_id"] = _id
            doc["type"] = "hd"
            doc["patient"] = {
                "id": _id,
                "name": patient.get("name", ""),
                "dob": patient.get("provided_dob", ""),
                "gender": patient.get("gender", "")
            }
            doc["org_id"] = org_id

            doc["schedule_id"] = next(schedule_id_cycler)

            # 👇 Add session_no calculation
            existing_sessions_count = collection.count_documents({
                "patient.id": _id,
                "schedule_id": doc["schedule_id"]
            })
            session_no = existing_sessions_count + 1
            doc["session_no"] = session_no

            selected_timeslot = random.choice(timeslots)
            start_hour = int(selected_timeslot["start"])
            end_hour = int(selected_timeslot["end"])
            duration_hours = end_hour - start_hour

            doc["scheduled_runtime"] = {
                "hours": duration_hours,
                "minutes": 0
            }

            doc["consulting_team"] = [
                {"role": "doctor"},
                {"role": "pre_tech", "id": user1_for_consulting["_id"], "name": user1_for_consulting["name"]},
                {"role": "pre_tech_asst", "id": user2_for_consulting["_id"], "name": user2_for_consulting["name"]},
                {"role": "post_tech", "id": user1_for_consulting["_id"], "name": user1_for_consulting["name"]},
                {"role": "post_tech_asst", "id": user2_for_consulting["_id"], "name": user2_for_consulting["name"]}
            ]
            doc["team_id"] = team_id

            selected_station = random.choice(unique_stations)
            doc["station"] = {
                "id": ObjectId(selected_station["id"]),
                "code": selected_station["code"]
            }

            events = []
            current_event_time = base_event_time
            num_events_to_generate = random.choice([1, 2, 6])

            for i in range(num_events_to_generate):
                event_label = next(event_labels_cycle)
                event_user = next(event_user_cycler)

                event = OrderedDict()
                event["label"] = event_label
                event["by"] = ObjectId(event_user["_id"])
                event["name"] = event_user["name"]
                event["on"] = current_event_time
                events.append(event)

                current_event_time += timedelta(minutes=random.randint(5, 15))

            doc["events"] = events

            if events:
                last_event = events[-1]
                doc["status"] = {
                    "label": last_event["label"],
                    "on": last_event["on"],
                    "by": str(last_event["by"]),
                    "name": last_event["name"]
                }
            else:
                doc["status"] = {
                    "label": "pending",
                    "on": base_event_time,
                    "by": "system",
                    "name": "System"
                }

            if events:
                first_event = events[0]
                last_event = events[-1]
                doc["audit"] = {
                    "created_by": str(first_event["by"]),
                    "created_on": first_event["on"],
                    "creator_name": first_event["name"],
                    "updated_by": str(last_event["by"]),
                    "updated_on": last_event["on"],
                    "updater_name": last_event["name"]
                }
            else:
                doc["audit"] = {
                    "created_by": "system",
                    "created_on": base_event_time,
                    "creator_name": "System",
                    "updated_by": "system",
                    "updated_on": base_event_time,
                    "updater_name": "System"
                }

            doc["data_id"] = data_id

            collection.replace_one({"_id": _id}, doc, upsert=True)
            print(f"✅ Inserted {pid} | session_no: {session_no} | schedule_id: {doc['schedule_id']} | scheduled_runtime: {doc['scheduled_runtime']['hours']}h | events: {len(doc['events'])} | status: {doc['status']['label']} | station: {doc['station']['code']}")
            inserted_count += 1

        except Exception as e:
            print(f"❌ Error for patient {pid}: {e}")

print(f"\n✅ Total documents inserted/updated: {inserted_count}")
