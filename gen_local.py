"""Generates local job leads for every state: city, schools, hospitals, transit, flagship university, state government.
These are real kinds of employers that exist in each place; pay is a typical national starting range."""
import json, urllib.parse

# state: (name, [(city, lat, lon), ...], (university, city, lat, lon))
S = {
 "AL":("Alabama",[("Birmingham",33.52,-86.80),("Montgomery",32.37,-86.30),("Huntsville",34.73,-86.59)],("University of Alabama","Tuscaloosa",33.21,-87.57)),
 "AK":("Alaska",[("Anchorage",61.22,-149.90),("Fairbanks",64.84,-147.72),("Juneau",58.30,-134.42)],("University of Alaska Fairbanks","Fairbanks",64.86,-147.83)),
 "AZ":("Arizona",[("Phoenix",33.45,-112.07),("Tucson",32.22,-110.97),("Mesa",33.42,-111.83),("Flagstaff",35.20,-111.65)],("University of Arizona","Tucson",32.23,-110.95)),
 "AR":("Arkansas",[("Little Rock",34.75,-92.29),("Fayetteville",36.06,-94.16),("Fort Smith",35.39,-94.40)],("University of Arkansas","Fayetteville",36.07,-94.17)),
 "CA":("California",[("Los Angeles",34.05,-118.24),("San Diego",32.72,-117.16),("San Jose",37.34,-121.89),("San Francisco",37.77,-122.42),("Sacramento",38.58,-121.49),("Fresno",36.74,-119.79)],("University of California, Berkeley","Berkeley",37.87,-122.26)),
 "CO":("Colorado",[("Denver",39.74,-104.99),("Colorado Springs",38.83,-104.82),("Fort Collins",40.59,-105.08),("Grand Junction",39.06,-108.55)],("University of Colorado Boulder","Boulder",40.01,-105.27)),
 "CT":("Connecticut",[("Bridgeport",41.19,-73.20),("Hartford",41.76,-72.69),("New Haven",41.31,-72.92)],("University of Connecticut","Storrs",41.81,-72.25)),
 "DE":("Delaware",[("Wilmington",39.74,-75.55),("Dover",39.16,-75.52)],("University of Delaware","Newark",39.68,-75.75)),
 "DC":("Washington DC",[("Washington",38.91,-77.04)],("University of the District of Columbia","Washington",38.94,-77.06)),
 "FL":("Florida",[("Jacksonville",30.33,-81.66),("Miami",25.76,-80.19),("Tampa",27.95,-82.46),("Orlando",28.54,-81.38),("Tallahassee",30.44,-84.28),("Pensacola",30.42,-87.22)],("University of Florida","Gainesville",29.65,-82.32)),
 "GA":("Georgia",[("Atlanta",33.75,-84.39),("Savannah",32.08,-81.09),("Augusta",33.47,-81.97),("Columbus",32.46,-84.99)],("University of Georgia","Athens",33.95,-83.38)),
 "HI":("Hawaii",[("Honolulu",21.31,-157.86),("Hilo",19.72,-155.08),("Kahului",20.89,-156.47)],("University of Hawaii at Manoa","Honolulu",21.30,-157.82)),
 "ID":("Idaho",[("Boise",43.62,-116.20),("Idaho Falls",43.49,-112.03),("Pocatello",42.87,-112.45),("Coeur d'Alene",47.68,-116.78)],("University of Idaho","Moscow",46.73,-117.00)),
 "IL":("Illinois",[("Chicago",41.88,-87.63),("Aurora",41.76,-88.32),("Rockford",42.27,-89.09),("Springfield",39.80,-89.64),("Peoria",40.69,-89.59)],("University of Illinois Urbana-Champaign","Champaign",40.11,-88.24)),
 "IN":("Indiana",[("Indianapolis",39.77,-86.16),("Fort Wayne",41.08,-85.14),("Evansville",37.97,-87.57),("South Bend",41.68,-86.25)],("Indiana University Bloomington","Bloomington",39.17,-86.53)),
 "IA":("Iowa",[("Des Moines",41.59,-93.62),("Cedar Rapids",41.98,-91.67),("Davenport",41.52,-90.58),("Sioux City",42.50,-96.40)],("University of Iowa","Iowa City",41.66,-91.53)),
 "KS":("Kansas",[("Wichita",37.69,-97.34),("Kansas City",39.11,-94.63),("Topeka",39.05,-95.68),("Overland Park",38.98,-94.67)],("University of Kansas","Lawrence",38.96,-95.25)),
 "KY":("Kentucky",[("Louisville",38.25,-85.76),("Lexington",38.04,-84.50),("Bowling Green",36.99,-86.44)],("University of Kentucky","Lexington",38.03,-84.50)),
 "LA":("Louisiana",[("New Orleans",29.95,-90.07),("Baton Rouge",30.45,-91.15),("Shreveport",32.53,-93.75),("Lafayette",30.22,-92.02)],("Louisiana State University","Baton Rouge",30.41,-91.18)),
 "ME":("Maine",[("Portland",43.66,-70.26),("Bangor",44.80,-68.77),("Lewiston",44.10,-70.21)],("University of Maine","Orono",44.90,-68.67)),
 "MD":("Maryland",[("Baltimore",39.29,-76.61),("Frederick",39.41,-77.41),("Annapolis",38.98,-76.49)],("University of Maryland","College Park",38.99,-76.94)),
 "MA":("Massachusetts",[("Boston",42.36,-71.06),("Worcester",42.26,-71.80),("Springfield",42.10,-72.59),("Lowell",42.63,-71.32)],("University of Massachusetts Amherst","Amherst",42.39,-72.53)),
 "MI":("Michigan",[("Detroit",42.33,-83.05),("Grand Rapids",42.96,-85.67),("Lansing",42.73,-84.56),("Flint",43.01,-83.69),("Traverse City",44.76,-85.62)],("University of Michigan","Ann Arbor",42.28,-83.74)),
 "MN":("Minnesota",[("Minneapolis",44.98,-93.27),("St. Paul",44.95,-93.09),("Rochester",44.02,-92.47),("Duluth",46.79,-92.10)],("University of Minnesota Twin Cities","Minneapolis",44.97,-93.23)),
 "MS":("Mississippi",[("Jackson",32.30,-90.18),("Gulfport",30.37,-89.09),("Hattiesburg",31.33,-89.29)],("University of Mississippi","Oxford",34.37,-89.54)),
 "MO":("Missouri",[("Kansas City",39.10,-94.58),("St. Louis",38.63,-90.20),("Springfield",37.21,-93.29),("Columbia",38.95,-92.33)],("University of Missouri","Columbia",38.94,-92.33)),
 "MT":("Montana",[("Billings",45.78,-108.50),("Missoula",46.87,-113.99),("Bozeman",45.68,-111.04),("Great Falls",47.50,-111.30)],("University of Montana","Missoula",46.86,-113.98)),
 "NE":("Nebraska",[("Omaha",41.26,-95.93),("Lincoln",40.81,-96.70),("Grand Island",40.93,-98.34)],("University of Nebraska-Lincoln","Lincoln",40.82,-96.70)),
 "NV":("Nevada",[("Las Vegas",36.17,-115.14),("Henderson",36.04,-114.98),("Reno",39.53,-119.81)],("University of Nevada, Reno","Reno",39.54,-119.82)),
 "NH":("New Hampshire",[("Manchester",42.99,-71.46),("Nashua",42.77,-71.47),("Concord",43.21,-71.54)],("University of New Hampshire","Durham",43.13,-70.93)),
 "NJ":("New Jersey",[("Newark",40.74,-74.17),("Jersey City",40.73,-74.08),("Paterson",40.92,-74.17),("Trenton",40.22,-74.76),("Atlantic City",39.36,-74.42)],("Rutgers University","New Brunswick",40.50,-74.45)),
 "NM":("New Mexico",[("Albuquerque",35.08,-106.65),("Las Cruces",32.32,-106.76),("Santa Fe",35.69,-105.94)],("University of New Mexico","Albuquerque",35.08,-106.62)),
 "NY":("New York",[("New York City",40.71,-74.01),("Buffalo",42.89,-78.88),("Rochester",43.16,-77.61),("Syracuse",43.05,-76.15),("Albany",42.65,-73.76),("Yonkers",40.93,-73.90)],("University at Buffalo","Buffalo",43.00,-78.79)),
 "NC":("North Carolina",[("Charlotte",35.23,-80.84),("Raleigh",35.78,-78.64),("Greensboro",36.07,-79.79),("Durham",35.99,-78.90),("Asheville",35.60,-82.55),("Wilmington",34.23,-77.94)],("University of North Carolina at Chapel Hill","Chapel Hill",35.91,-79.05)),
 "ND":("North Dakota",[("Fargo",46.88,-96.79),("Bismarck",46.81,-100.78),("Minot",48.23,-101.30)],("University of North Dakota","Grand Forks",47.92,-97.08)),
 "OH":("Ohio",[("Columbus",39.96,-83.00),("Cleveland",41.50,-81.69),("Cincinnati",39.10,-84.51),("Toledo",41.65,-83.54),("Akron",41.08,-81.52),("Dayton",39.76,-84.19)],("The Ohio State University","Columbus",40.01,-83.03)),
 "OK":("Oklahoma",[("Oklahoma City",35.47,-97.52),("Tulsa",36.15,-95.99),("Lawton",34.61,-98.39)],("University of Oklahoma","Norman",35.21,-97.44)),
 "OR":("Oregon",[("Portland",45.52,-122.68),("Eugene",44.05,-123.09),("Salem",44.94,-123.04),("Bend",44.06,-121.32),("Medford",42.33,-122.87)],("University of Oregon","Eugene",44.04,-123.07)),
 "PA":("Pennsylvania",[("Philadelphia",39.95,-75.17),("Pittsburgh",40.44,-80.00),("Allentown",40.60,-75.49),("Erie",42.13,-80.09),("Harrisburg",40.27,-76.88),("Scranton",41.41,-75.66)],("Penn State University","State College",40.80,-77.86)),
 "RI":("Rhode Island",[("Providence",41.82,-71.41),("Warwick",41.70,-71.42),("Cranston",41.78,-71.44)],("University of Rhode Island","Kingston",41.48,-71.53)),
 "SC":("South Carolina",[("Charleston",32.78,-79.93),("Columbia",34.00,-81.03),("Greenville",34.85,-82.40),("Myrtle Beach",33.69,-78.89)],("University of South Carolina","Columbia",33.99,-81.03)),
 "SD":("South Dakota",[("Sioux Falls",43.54,-96.73),("Rapid City",44.08,-103.23),("Aberdeen",45.46,-98.49)],("University of South Dakota","Vermillion",42.78,-96.93)),
 "TN":("Tennessee",[("Nashville",36.16,-86.78),("Memphis",35.15,-90.05),("Knoxville",35.96,-83.92),("Chattanooga",35.05,-85.31),("Clarksville",36.53,-87.36)],("University of Tennessee","Knoxville",35.95,-83.93)),
 "TX":("Texas",[("Houston",29.76,-95.37),("San Antonio",29.42,-98.49),("Dallas",32.78,-96.80),("Austin",30.27,-97.74),("Fort Worth",32.76,-97.33),("El Paso",31.76,-106.49),("Corpus Christi",27.80,-97.40),("Lubbock",33.58,-101.86)],("University of Texas at Austin","Austin",30.28,-97.74)),
 "UT":("Utah",[("Salt Lake City",40.76,-111.89),("West Valley City",40.69,-112.00),("Provo",40.23,-111.66),("Ogden",41.22,-111.97),("St. George",37.10,-113.58),("Logan",41.74,-111.83)],("University of Utah","Salt Lake City",40.76,-111.84)),
 "VT":("Vermont",[("Burlington",44.48,-73.21),("Rutland",43.61,-72.97),("Montpelier",44.26,-72.58)],("University of Vermont","Burlington",44.48,-73.20)),
 "VA":("Virginia",[("Virginia Beach",36.85,-75.98),("Richmond",37.54,-77.44),("Norfolk",36.85,-76.29),("Chesapeake",36.77,-76.29),("Roanoke",37.27,-79.94),("Alexandria",38.80,-77.05)],("University of Virginia","Charlottesville",38.03,-78.51)),
 "WA":("Washington",[("Seattle",47.61,-122.33),("Spokane",47.66,-117.43),("Tacoma",47.25,-122.44),("Vancouver",45.64,-122.66),("Bellingham",48.75,-122.48),("Yakima",46.60,-120.51)],("University of Washington","Seattle",47.66,-122.31)),
 "WV":("West Virginia",[("Charleston",38.35,-81.63),("Huntington",38.42,-82.45),("Morgantown",39.63,-79.96)],("West Virginia University","Morgantown",39.65,-79.96)),
 "WI":("Wisconsin",[("Milwaukee",43.04,-87.91),("Madison",43.07,-89.40),("Green Bay",44.51,-88.01),("Eau Claire",44.81,-91.50)],("University of Wisconsin-Madison","Madison",43.08,-89.41)),
 "WY":("Wyoming",[("Cheyenne",41.14,-104.82),("Casper",42.87,-106.31),("Jackson",43.48,-110.76)],("University of Wyoming","Laramie",41.31,-105.58)),
}
B = {"H":"Health insurance","D":"Dental","V":"Vision","R":"401(k) / retirement","P":"Paid time off","F":"Flexible schedule","T":"Tuition help","E":"Employee discount","L":"Parental leave","B":"Bonus / tips"}
GOV = "H;D;V;R;P"
# (title, company template, category, type, payMin, payMax, minAge, minYears, education, certs, skills, benefits, summary template)
CITY = [
 ("Lifeguard","City of {c}","outdoors","temporary",14,19,15,0,None,"Lifeguard certification","Swimming;CPR;Attention","F","Guard {c}'s public pools and splash pads. The city often pays for your certification."),
 ("Recreation Leader","City of {c}","outdoors","part-time",13,17,16,0,None,"","Kids;Sports;Leadership","F","Lead games, sports and after-school programs at {c} rec centers."),
 ("Summer Camp Counselor","City of {c}","care","temporary",13,17,16,0,None,"","Childcare;Energy;Leadership","F","Run day-camp activities for kids through {c} Parks & Recreation."),
 ("Library Page","{c} public library","brainy","part-time",12,16,15,0,None,"","Organization;Reading;Customer service","F;P","Shelve books and help patrons at {c}'s public library. Quiet and student-friendly."),
 ("311 Customer Service Rep","City of {c}","people","full-time",17,22,18,0,"highschool","","Phone skills;Customer service;Computers",GOV,"Answer residents' calls and requests for city services in {c}."),
 ("Parks Maintenance Worker (Seasonal)","City of {c}","outdoors","temporary",14,18,16,0,None,"","Outdoor work;Lifting;Teamwork","F","Mow, plant and keep {c}'s parks and trails clean in spring and summer."),
 ("Solid Waste Worker","City of {c}","hands-on","full-time",17,23,18,0,None,"Driver's license","Lifting;Safety;Reliability",GOV,"Collect trash and recycling on routes around {c}. Early mornings, steady city benefits."),
 ("Water Utility Maintenance Worker","City of {c}","hands-on","full-time",18,25,18,0,"highschool","Driver's license","Tools;Safety;Teamwork",GOV,"Repair water lines and keep {c}'s water system running. Paid training toward certifications."),
 ("911 Dispatcher Trainee","City of {c}","people","full-time",19,26,18,0,"highschool","","Typing;Calm under pressure;Communication",GOV,"Answer emergency calls and send help in {c}. Paid training; shifts around the clock."),
 ("Firefighter Recruit","{c} Fire Department","hands-on","full-time",20,28,18,0,"highschool","EMT (often trained on the job)","Physical fitness;Teamwork;Safety",GOV,"Train at the academy, then fight fires and answer medical calls in {c}."),
 ("Paraprofessional (Teacher Aide)","{c} public schools","brainy","full-time",14,19,18,0,"highschool","","Patience;Teaching;Organization","H;D;R;P","Help teachers and students in classrooms around {c}. Summers off."),
 ("School Bus Driver","{c} public schools","hands-on","part-time",18,24,21,0,"highschool","CDL license (paid training)","Driving;Safety;Kids","H;R;P;T","Drive students to and from school in {c}. Districts usually pay for your CDL training."),
 ("School Food Service Worker","{c} public schools","people","part-time",14,18,18,0,None,"Food handler's permit","Food prep;Teamwork;Cleaning","H;R;P;F","Prep and serve school breakfasts and lunches in {c}. School-day hours."),
 ("School Custodian","{c} public schools","hands-on","full-time",15,20,18,0,None,"","Cleaning;Reliability;Safety",GOV,"Keep schools in {c} clean and safe."),
 ("Patient Care Technician","Hospitals in {c}","care","full-time",17,22,18,0,"highschool","CNA certification","Patient care;Vital signs;Compassion","H;D;V;R;P;T","Help nurses care for patients at hospitals around {c}. Many hospitals train you."),
 ("Environmental Services Tech","Hospitals in {c}","hands-on","full-time",15,19,18,0,None,"","Cleaning;Attention to detail;Safety","H;D;V;R;P;T","Clean and disinfect patient rooms at hospitals in {c}. A common way into healthcare."),
 ("Bus Operator Trainee","{c}-area public transit","hands-on","full-time",20,27,21,0,"highschool","CDL license (paid training)","Driving;Customer service;Safety",GOV,"Drive city buses around {c}. Transit agencies pay for CDL training and offer union benefits."),
]
UNIV = [
 ("Dining Services Worker","{u}","people","part-time",13,17,16,0,None,"","Food prep;Customer service;Cleaning","F;E;P","Serve food and clean in campus dining halls at {u}. Often open to non-students."),
 ("Library Assistant","{u}","brainy","part-time",12,16,17,0,None,"","Organization;Customer service;Computers","F","Check out books and help students at {u}'s libraries."),
 ("Custodian","{u}","hands-on","full-time",16,20,18,0,None,"","Cleaning;Reliability;Safety","H;D;V;R;P;T","Clean campus buildings at {u}. Employees can often take classes for free or cheap."),
 ("Groundskeeper","{u}","outdoors","full-time",16,21,18,0,None,"Driver's license","Landscaping;Tools;Outdoor work","H;D;V;R;P;T","Keep {u}'s campus green and beautiful."),
 ("Research Lab Assistant","{u}","brainy","part-time",14,18,18,0,None,"","Lab safety;Accuracy;Organization","F;T","Prep supplies and help researchers in labs at {u}."),
 ("IT Help Desk Assistant","{u}","tech","part-time",15,20,18,0,None,"","Tech support;Computers;Customer service","F;T","Help students and staff fix computer and Wi-Fi problems at {u}."),
]
STATE = [
 ("Highway Maintenance Worker","State of {n} (Department of Transportation)","hands-on","full-time",18,24,18,0,"highschool","CDL license (often trained)","Driving;Tools;Safety",GOV,"Patch roads, plow snow and keep {n}'s highways safe. Apply on the state's job site."),
 ("State Park Seasonal Aide","{n} State Parks","outdoors","temporary",13,17,16,0,None,"","Outdoor work;Customer service;Cleaning","F","Collect fees, clean campgrounds and help visitors at {n} state parks."),
 ("Fish & Wildlife Technician","{n} wildlife agency","outdoors","temporary",15,20,18,0,"highschool","Driver's license","Outdoor work;Animals;Data entry","F","Help biologists count fish and wildlife and take care of public land in {n}."),
 ("Correctional Officer Trainee","{n} Department of Corrections","people","full-time",20,26,18,0,"highschool","","Communication;Calm under pressure;Safety",GOV,"Supervise people in state facilities. Paid academy training; age rules vary (18–21)."),
 ("Office Assistant","State of {n} agencies","brainy","full-time",16,21,18,0,"highschool","","Computers;Organization;Customer service",GOV,"Answer phones, file and help the public at state offices around {n}."),
 ("Child Welfare Caseworker","{n} family services agency","care","full-time",20,26,21,0,"bachelor","","Communication;Compassion;Writing",GOV,"Help keep kids safe and support families in {n}. Usually needs a bachelor's degree."),
]
def find_url(company, title, place):
    q = f"{company} {title} jobs" + (f" {place}" if place else "")
    return "https://www.google.com/search?q=" + urllib.parse.quote(q)

def make(t, st, place, lat, lon, fmt):
    title, comp, cat, ty, pmn, pmx, age, yrs, edu, certs, skills, bens, summ = t
    company = comp.format(**fmt); summary = summ.format(**fmt)
    return {"library": True, "title": title, "company": company, "category": cat, "type": ty, "payMin": float(pmn), "payMax": float(pmx), "payUnit": "hour",
            "minAge": age, "teen": age < 18, "minYears": yrs, "education": edu,
            "certs": [c for c in certs.split(";") if c and "(" not in c], "skills": skills.split(";"), "benefits": [B[b] for b in bens.split(";") if b],
            "summary": summary, "remote": False, "states": [st], "location": f"{place}, {st}" if place else "", "lat": lat, "lon": lon,
            "findUrl": find_url(company, title, f"{place} {st}" if place else st)}

out = []
for st, (name, cities, (u, ucity, ulat, ulon)) in S.items():
    for (c, lat, lon) in cities:
        for t in CITY: out.append(make(t, st, c, lat, lon, {"c": c}))
    for t in UNIV: out.append(make(t, st, ucity, ulat, ulon, {"u": u}))
    for t in STATE: out.append(make(t, st, "", None, None, {"n": name}))
lib = json.load(open("jobs-library.json"))
base = [j for j in lib if not j["id"].startswith("loc")]
for i, j in enumerate(out, 1): j["id"] = f"loc{i:04d}"
json.dump(base + out, open("jobs-library.json", "w"), separators=(",", ":"))
print("cities:", sum(len(v[1]) for v in S.values()), "| new local jobs:", len(out), "| library total:", len(base) + len(out))
