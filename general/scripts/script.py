import json
import random
from datetime import datetime, timedelta

def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def generate_patient_data(num_records):
    patients = []
    salutations = ["Mr.", "Mrs.", "Ms.", "Master", "Miss"]
    genders = ["Male", "Female", "Other"]
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    phone_types = ["mobile", "home", "work"]
    relative_types = ["parent", "spouse", "sibling", "child", "friend"]
    auth_levels = ["full", "limited", "none"]

    first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Saanvi", "Aanya", "Aadhya", "Aaradhya", "Ananya", "Pari", "Diya", "Myra", "Sara", "Anika"]
    last_names = ["Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Shah", "Mehta", "Jain", "Reddy", "Naidu", "Menon", "Nair", "Iyer", "Iyengar"]

    for i in range(num_records):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1,100)}@example.com"
        
        dob_start = datetime(1950, 1, 1)
        dob_end = datetime(2010, 1, 1)
        dob = random_date(dob_start, dob_end)
        dob_str = dob.strftime("%d-%m-%Y")

        patient = {
            "salutation": random.choice(salutations),
            "name": name,
            "provided_dob": dob_str,
            "biological_dob": dob_str,
            "is_approx_dob": random.choice([True, False]),
            "gender": random.choice(genders),
            "blood_group": random.choice(blood_groups),
            "email": email,
            "phones": [
                {
                    "type": random.choice(phone_types),
                    "number": f"+91{random.randint(7000000000, 9999999999)}",
                    "caregiver_name": f"{random.choice(first_names)} {random.choice(last_names)}"
                }
            ],
            "addresses": [],
            "relatives": []
        }

        if random.choice([True, False]):
            patient["addresses"].append({
                "line1": f"{random.randint(1, 200)}, {random.randint(1,10)}th Cross",
                "line2": f"{random.randint(1,10)}th Main",
                "city": "Bengaluru",
                "state": "Karnataka",
                "pincode": "560001",
                "location": {
                    "lat": round(random.uniform(12.8, 13.1), 4),
                    "long": round(random.uniform(77.5, 77.7), 4)
                }
            })

        if random.choice([True, False]):
             patient["relatives"].append({
                "patient_id": None, # This would need to be a valid patient ID
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "number": f"+91{random.randint(7000000000, 9999999999)}",
                "type": random.choice(relative_types),
                "auth_level": random.choice(auth_levels)
             })

        patients.append(patient)

    return patients

if __name__ == "__main__":
    patients_data = generate_patient_data(20)
    with open("create_patients.json", "w") as f:
        json.dump(patients_data, f, indent=2)
    print("Generated create_patients.json with 20 patient records.")
