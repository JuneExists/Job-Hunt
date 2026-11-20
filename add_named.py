"""Turns library_named.txt (real, named local small businesses) into nb### jobs placed before the loc jobs."""
import json
from collections import Counter
VALID=set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split())
B={"F":"Flexible schedule","E":"Employee discount","B":"Bonus / tips"}
R={"books":("Bookseller","creative",13,17,16,"Reading;Customer service;Organization","F;E","independent bookstore"),
 "coffee":("Barista","people",13,17,16,"Barista;Customer service;Cash handling","F;B;E","local coffee shop"),
 "bakery":("Bakery Counter & Baker's Assistant","hands-on",13,17,16,"Baking;Customer service;Food safety","F;E","local bakery"),
 "icecream":("Ice Cream Scooper","people",11,15,14,"Customer service;Cash handling;Friendly","F;B;E","local ice cream shop"),
 "records":("Record Store Clerk","creative",12,16,16,"Music;Customer service;Organization","F;E","independent record store"),
 "restaurant":("Host / Server","people",12,16,16,"Customer service;Teamwork;Multitasking","F;B;E","locally owned restaurant"),
 "deli":("Deli Counter Clerk","people",13,17,16,"Food prep;Customer service;Knife skills","F;E","local deli"),
 "donut":("Donut Shop Team Member","people",12,16,15,"Customer service;Food prep;Early mornings","F;B;E","local donut shop"),
 "pizza":("Pizza Maker / Server","hands-on",13,17,15,"Food prep;Teamwork;Customer service","F;B;E","local pizzeria"),
 "boutique":("Sales Associate","people",13,17,16,"Customer service;Style;Sales","F;E","local boutique"),
 "market":("Market Clerk","people",13,17,16,"Customer service;Stocking;Cash handling","F;E","local market"),
 "candy":("Candy Shop Clerk","people",11,15,14,"Customer service;Cash handling;Friendly","F;E","local candy shop"),
 "bbq":("Counter & Kitchen Crew","hands-on",13,17,16,"Food prep;Customer service;Teamwork","F;B;E","local barbecue restaurant"),
 "gifts":("Sales Associate","people",12,16,16,"Customer service;Gift wrapping;Cash handling","F;E","local gift shop"),
 "tourist":("Seasonal Team Member","outdoors",13,16,15,"Customer service;Cash handling;Teamwork","F;E","famous local attraction")}
C={}
for line in open('named_contacts.txt'):
    if line.strip() and not line.startswith('#'):
        b,c,e,ph=[x.strip() for x in line.rstrip('\n').split('|')]; C[(b,c)]=(e,ph)
out=[];seen=set()
for line in open('library_named.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    st,biz,city,lat,lon,role=line.split('|')
    assert st in VALID and role in R and (biz,city) not in seen,(st,biz,role); seen.add((biz,city))
    lat,lon=float(lat),float(lon); assert 18<lat<72 and -170<lon<-66,biz
    title,cat,pmn,pmx,age,skills,bens,kind=R[role]
    out.append({"library":True,"smallBiz":True,"named":True,"title":title,"company":biz,"category":cat,"type":"part-time",
      "payMin":float(pmn),"payMax":float(pmx),"payUnit":"hour","minAge":age,"teen":age<18,"minYears":0,"education":None,"certs":[],
      "skills":skills.split(';'),"benefits":[B[b] for b in bens.split(';')],
      "summary":f"{biz} is a {kind} in {city}. Ask about openings, or check their website and social media for hiring posts.",
      "remote":False,"states":[st],"location":f"{city}, {st}","lat":lat,"lon":lon})
    e,ph=C.get((biz,city),("",""))
    if e: out[-1]["applyEmail"]=e; out[-1]["domain"]=e.split("@")[1]
    if ph: out[-1]["phone"]=ph
L=[j for j in json.load(open('jobs-library.json')) if not j['id'].startswith('nb')]
for i,j in enumerate(out,1): j['id']=f"nb{i:03d}"
base=[j for j in L if not j['id'].startswith('loc')]; loc=[j for j in L if j['id'].startswith('loc')]
json.dump(base+out+loc,open('jobs-library.json','w'),separators=(',',':'))
c=Counter(j['states'][0] for j in out)
print("with email:",sum(1 for j in out if j.get("applyEmail")),"| named:",len(out),"states:",len(c),"min/state:",min(c.values()),"| total:",len(base+out+loc))
