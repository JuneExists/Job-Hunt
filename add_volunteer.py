"""Adds volunteer and low-pay stipend opportunities (ids start with "vol"; all have volunteer: true).
National organizations with local chapters or programs in most cities, every named hospital's volunteer program,
remote volunteering, stipend service programs, and a few Salt Lake City favorites.
Ages are the usual minimums; each program sets its own."""
import json, re, urllib.parse
src = open("gen_local.py").read(); ns = {}
exec(src[:src.index("CITY = [")], ns)
S, H = ns["S"], ns["H"]
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
gsearch = lambda q: "https://www.google.com/search?q=" + urllib.parse.quote(q)
B = {"F":"Flexible schedule","T":"Tuition help","H":"Health insurance"}

def vol(id, title, company, cat, age, skills, summary, ty="volunteer", pmn=None, pmx=None, unit="hour", bens="F", **kw):
    j = {"id": id, "library": True, "volunteer": True, "title": title, "company": company, "category": cat, "type": ty,
         "payMin": pmn, "payMax": pmx, "payUnit": unit, "minAge": age, "teen": age < 18, "minYears": 0, "education": None,
         "certs": [], "skills": skills, "benefits": [B[b] for b in bens], "summary": summary, "remote": False}
    j.update(kw); return j

out = []
# ---- remote + stipend programs ----
out.append(vol("vol-crisis-text-line", "Volunteer Crisis Counselor", "Crisis Text Line", "care", 18, ["Active listening", "Compassion", "Communication", "Typing"],
  "Text with people who are struggling, from home. Free training online; you commit to a few hours a week.", remote=True, findUrl=gsearch("Crisis Text Line volunteer crisis counselor")))
out.append(vol("vol-smithsonian", "Digital Volunteer (transcription)", "Smithsonian Transcription Center", "brainy", 13, ["Typing", "Attention to detail", "Reading"],
  "Type up handwritten historical documents, diaries and specimen labels for the Smithsonian, any time, from anywhere.", remote=True, findUrl=gsearch("Smithsonian Transcription Center volunteer")))
out.append(vol("vol-zooniverse", "Citizen Science Volunteer", "Zooniverse", "brainy", 13, ["Attention to detail", "Computers"],
  "Help real research projects by sorting photos of animals, galaxies and more. No experience needed.", remote=True, findUrl=gsearch("Zooniverse volunteer projects")))
out.append(vol("vol-psi", "Volunteer Peer Support / Coordinator", "Postpartum Support International", "care", 18, ["Compassion", "Postpartum care", "Active listening", "Doula"],
  "Support parents with postpartum depression and anxiety through PSI's volunteer network. Great for doulas and people with lived experience.", remote=True, findUrl=gsearch("Postpartum Support International volunteer")))
out.append(vol("vol-peace-corps", "Peace Corps Volunteer (stipend)", "Peace Corps", "people", 18, ["Teaching", "Adaptable", "Community outreach"],
  "Live and work abroad for about 2 years in education, health or farming. Living costs are covered, with a payment when you finish.",
  ty="temporary", bens="H", remote=True, findUrl=gsearch("Peace Corps apply")))


# ---- more remote / from home ----
for id_, title, comp, cat, age, skills, summ in [
  ("vol-be-my-eyes", "Video Helper (on your phone)", "Be My Eyes", "care", 17, ["Communication", "Patience", "Friendly"], "Answer short video calls from blind and low-vision people who need a quick pair of eyes, like reading a label. Help whenever your phone rings."),
  ("vol-7cups", "Volunteer Listener", "7 Cups", "care", 18, ["Active listening", "Compassion", "Typing"], "Give free, anonymous emotional support by text chat after a short online training."),
  ("vol-librivox", "Audiobook Reader", "LibriVox", "creative", 13, ["Reading", "Public speaking", "Computers"], "Record yourself reading chapters of public-domain books so anyone can listen free."),
  ("vol-learning-ally", "Volunteer Reader & Reviewer", "Learning Ally", "brainy", 18, ["Reading", "Attention to detail"], "Help make audiobooks for students with dyslexia and other reading differences."),
  ("vol-familysearch", "Record Indexing Volunteer", "FamilySearch", "brainy", 12, ["Typing", "Attention to detail", "Reading"], "Type up names and dates from old records so families can find their ancestors. Any amount of time, from home."),
  ("vol-hot", "Mapping Volunteer", "Humanitarian OpenStreetMap Team", "brainy", 13, ["Computers", "Attention to detail"], "Trace roads and buildings on satellite photos to help disaster responders. Training is built in."),
  ("vol-wikipedia", "Wikipedia Editor", "Wikimedia Foundation", "brainy", 13, ["Writing", "Research", "Attention to detail"], "Improve Wikipedia articles on topics you know, like art, music or your hometown."),
  ("vol-catchafire", "Skills-Based Volunteer", "Catchafire", "creative", 18, ["Graphic design", "Writing", "Social media", "Canva"], "Use your skills (design, writing, social media) on short projects for nonprofits. Great for building a portfolio."),
  ("vol-unv-online", "Online Volunteer", "UN Volunteers", "brainy", 18, ["Writing", "Research", "Graphic design", "Translation"], "Help United Nations partners online with design, writing, research and translation tasks."),
  ("vol-twb", "Volunteer Translator", "Translators without Borders (CLEAR Global)", "brainy", 18, ["Spanish", "Bilingual", "Writing"], "Translate health and crisis information for people in other languages. Needs strong skills in two languages."),
]:
    out.append(vol(id_, title, comp, cat, age, skills, summ, remote=True, findUrl=gsearch(f"{comp} volunteer")))
out.append(vol("vol-experience-corps", "Reading Tutor (ages 50+)", "AARP Foundation Experience Corps", "care", 50, ["Tutoring", "Patience", "Reading", "Teaching"],
  "Volunteers 50 and older help young kids learn to read in local schools. Some cities offer a small stipend.", findUrl=gsearch("AARP Foundation Experience Corps volunteer"), remote=True))
out.append(vol("vol-foodcorps", "FoodCorps Service Member (stipend)", "FoodCorps", "outdoors", 18, ["Teaching", "Gardening", "Cooking", "Childcare"],
  "A year of service teaching kids about healthy food and school gardens, for a living stipend and education award.", ty="temporary", bens="T", remote=True, findUrl=gsearch("FoodCorps apply")))
out.append(vol("vol-ace", "Conservation Corps Member (stipend)", "American Conservation Experience", "outdoors", 18, ["Outdoor work", "Teamwork", "Tools", "Hiking"],
  "Build trails and restore public lands in crews across the West, with a living stipend.", ty="temporary", bens="T", remote=True, findUrl=gsearch("American Conservation Experience apply")))
out.append(vol("vol-ucc", "Utah Conservation Corps Member (stipend)", "Utah Conservation Corps (USU)", "outdoors", 18, ["Outdoor work", "Teamwork", "Tools"],
  "Seasonal crews doing trail, habitat and fire-fuel work across Utah, with a living stipend and education award.", ty="temporary", bens="T",
  states=["UT"], location="Logan, UT", lat=41.74, lon=-111.81, findUrl=gsearch("Utah Conservation Corps apply")))

# ---- Salt Lake City favorites ----
SLC = dict(states=["UT"], location="Salt Lake City, UT")
out.append(vol("vol-ut-food-bank", "Warehouse Volunteer", "Utah Food Bank", "hands-on", 8, ["Teamwork", "Packing & shipping", "Lifting"],
  "Sort and pack food for families across Utah. Kids can come with an adult; groups welcome.", lat=40.70, lon=-111.92, findUrl=gsearch("Utah Food Bank volunteer"), **SLC))
out.append(vol("vol-ut-best-friends", "Animal Care Volunteer", "Best Friends Animal Society - Utah", "care", 18, ["Animals", "Pet care", "Cleaning", "Compassion"],
  "Walk dogs, socialize cats and help adoptions at Best Friends' Salt Lake City lifesaving center.", lat=40.73, lon=-111.90, findUrl=gsearch("Best Friends Animal Society Salt Lake City volunteer"), **SLC))
out.append(vol("vol-ut-rmhc", "House Volunteer", "Ronald McDonald House Charities Intermountain Area", "care", 16, ["Cooking", "Cleaning", "Compassion"],
  "Cook meals, tidy up and welcome families staying near their kids in the hospital.", lat=40.76, lon=-111.83, findUrl=gsearch("Ronald McDonald House Intermountain Area volunteer"), **SLC))
out.append(vol("vol-ut-primary-childrens", "Hospital Volunteer", "Intermountain Primary Children's Hospital", "care", 16, ["Childcare", "Compassion", "Patience"],
  "Play with kids, help families and support staff at Utah's children's hospital.", lat=40.77, lon=-111.84, findUrl=gsearch("Primary Children's Hospital volunteer"), **SLC))
out.append(vol("vol-ut-voa", "Volunteer", "Volunteers of America, Utah", "people", 16, ["Compassion", "Cooking", "Teamwork"],
  "Serve meals and help at youth and family programs in Salt Lake City.", lat=40.75, lon=-111.90, findUrl=gsearch("Volunteers of America Utah volunteer"), **SLC))


for id_, title, comp, cat, age, skills, summ, lat, lon in [
  ("vol-ut-humane", "Animal Care Volunteer", "Humane Society of Utah", "care", 16, ["Animals", "Pet care", "Cleaning"], "Walk dogs, socialize cats and help with adoptions in Murray.", 40.66, -111.90),
  ("vol-ut-slcpl", "Library Volunteer", "Salt Lake City Public Library", "brainy", 14, ["Organization", "Reading", "Customer service"], "Shelve books, help at events and support kids' programs at the Main Library and branches.", 40.76, -111.88),
  ("vol-ut-aviary", "Volunteer", "Tracy Aviary", "outdoors", 16, ["Animals", "Public speaking", "Outdoor work"], "Help with birds, gardens and education programs at Liberty Park.", 40.74, -111.87),
  ("vol-ut-red-butte", "Garden Volunteer", "Red Butte Garden", "outdoors", 16, ["Gardening", "Outdoor work", "Teamwork"], "Plant, weed and help at concerts and events in the University of Utah's botanical garden.", 40.77, -111.82),
  ("vol-ut-hogle", "Zoo Volunteer", "Utah's Hogle Zoo", "outdoors", 16, ["Animals", "Public speaking", "Customer service"], "Talk with guests, help at animal encounters and support education programs.", 40.75, -111.81),
  ("vol-ut-nhmu", "Museum Volunteer", "Natural History Museum of Utah", "brainy", 16, ["Public speaking", "Science", "Customer service"], "Help guests explore exhibits and assist with hands-on activities and collections.", 40.76, -111.82),
  ("vol-ut-road-home", "Shelter Volunteer", "The Road Home", "people", 16, ["Compassion", "Cooking", "Teamwork"], "Serve meals and help at family and community shelters in Salt Lake County.", 40.75, -111.90),
  ("vol-ut-ccs", "Dining Hall Volunteer", "Catholic Community Services of Utah", "people", 14, ["Cooking", "Teamwork", "Compassion"], "Serve meals at the St. Vincent de Paul Dining Hall and help in the food pantry.", 40.75, -111.91),
  ("vol-ut-irc", "Refugee Family Mentor", "International Rescue Committee - Salt Lake City", "care", 18, ["Compassion", "Communication", "Bilingual"], "Help newly arrived refugee families learn the city, practice English and get settled.", 40.72, -111.89),
]:
    out.append(vol(id_, title, comp, cat, age, skills, summ, lat=lat, lon=lon, findUrl=gsearch(f"{comp} volunteer"), **SLC))

# ---- every city ----
for st, (name, cities, uni) in S.items():
    for (c, lat, lon) in cities:
        k = f"{slug(st)}-{slug(c)}"; base = dict(states=[st], location=f"{c}, {st}", lat=lat, lon=lon)
        h = H.get(st, {}).get(c)
        if h:
            out.append(vol(f"vol-{k}-hosp", "Hospital Volunteer", h, "care", 16, ["Compassion", "Customer service", "Patience"],
              f"Greet visitors, deliver flowers and help patients and families at {h}. Many hospitals take volunteers 16 and up.", findUrl=gsearch(f"{h} volunteer"), **base))
        out.append(vol(f"vol-{k}-redcross", "Volunteer", "American Red Cross", "people", 16, ["Customer service", "Teamwork", "Reliability"],
          f"Help at blood drives, support families after home fires or join disaster response near {c}. Training provided.", findUrl=gsearch(f"American Red Cross volunteer {c} {st}"), **base))
        out.append(vol(f"vol-{k}-habitat", "Build Volunteer", "Habitat for Humanity", "hands-on", 16, ["Tools", "Teamwork", "Outdoor work"],
          f"Help build and repair affordable homes around {c}. No experience needed; crew leaders teach you on site.", findUrl=gsearch(f"Habitat for Humanity volunteer {c} {st}"), **base))
        out.append(vol(f"vol-{k}-mow", "Meal Delivery Driver", "Meals on Wheels", "people", 18, ["Driving", "Reliability", "Friendly"],
          f"Deliver meals and a friendly check-in to older neighbors around {c}. Usually about an hour, once a week.", findUrl=gsearch(f"Meals on Wheels volunteer {c} {st}"), **base))
        out.append(vol(f"vol-{k}-bbbs", "Mentor (Big)", "Big Brothers Big Sisters", "care", 18, ["Patience", "Communication", "Reliability"],
          f"Spend a few hours a month as a mentor to a kid around {c}. Matched by interests.", findUrl=gsearch(f"Big Brothers Big Sisters volunteer {c} {st}"), **base))
        out.append(vol(f"vol-{k}-bgc", "Club Volunteer", "Boys & Girls Clubs of America", "care", 16, ["Childcare", "Tutoring", "Sports"],
          f"Help with homework, games and sports at a Boys & Girls Club around {c}.", findUrl=gsearch(f"Boys & Girls Club volunteer {c} {st}"), **base))
        stname = S[st][0]
        out.append(vol(f"vol-{k}-salvation", "Volunteer", "The Salvation Army", "people", 14, ["Customer service", "Compassion", "Teamwork"],
          f"Ring bells at the holidays, sort donations or help at the food pantry around {c}.", findUrl=gsearch(f"Salvation Army volunteer {c} {st}"), **base))
        out.append(vol(f"vol-{k}-specialoly", "Coach or Event Volunteer", f"Special Olympics {stname}", "care", 15, ["Sports", "Coaching", "Patience", "Friendly"],
          f"Coach athletes with intellectual disabilities or help at games and events around {c}.", findUrl=gsearch(f"Special Olympics {stname} volunteer {c}"), **base))
        out.append(vol(f"vol-{k}-ymca", "Program Volunteer", "YMCA", "care", 14, ["Childcare", "Sports", "Friendly"],
          f"Help with youth sports, camps and community programs at a Y around {c}.", findUrl=gsearch(f"YMCA volunteer {c} {st}"), **base))
        out.append(vol(f"vol-{k}-ja", "Classroom Volunteer", "Junior Achievement", "brainy", 18, ["Teaching", "Public speaking", "Communication"],
          f"Teach short, ready-made lessons about money and careers to students around {c}. Everything is provided.", findUrl=gsearch(f"Junior Achievement volunteer {c} {st}"), **base))
        out.append(vol(f"vol-{k}-girlscouts", "Troop Leader or Event Volunteer", "Girl Scouts", "care", 18, ["Childcare", "Leadership", "Crafts"],
          f"Lead a troop or help at camps and events for girls around {c}.", findUrl=gsearch(f"Girl Scouts volunteer {c} {st}"), **base))
        out.append(vol(f"vol-{k}-casa", "Court Appointed Special Advocate (CASA)", "CASA for Children", "care", 21, ["Compassion", "Communication", "Writing"],
          f"Get trained to speak up in court for a child in foster care around {c}. About 10 to 15 hours a month.", findUrl=gsearch(f"CASA volunteer {c} {st}"), **base))


# ---- more every-city programs (national groups with local chapters nearly everywhere) ----
for st, (name, cities, uni) in S.items():
    stname = S[st][0]
    for (c, lat, lon) in cities:
        k = f"{slug(st)}-{slug(c)}"; base = dict(states=[st], location=f"{c}, {st}", lat=lat, lon=lon)
        for sfx, title, comp, cat, age, skills, summ in [
          ("taxaide", "Tax Preparer Volunteer", "AARP Foundation Tax-Aide", "brainy", 18, ["Math", "Attention to detail", "Customer service", "Computers"],
             f"Get free IRS training, then help neighbors around {c} file their taxes, January to April. You don't need to be an AARP member or retired."),
          ("restore", "ReStore Volunteer", "Habitat for Humanity ReStore", "hands-on", 14, ["Customer service", "Lifting", "Teamwork", "Cash handling"],
             f"Sort donated furniture and building supplies, help shoppers and run the register at a ReStore around {c}."),
          ("unitedway", "Volunteer", "United Way", "people", 14, ["Teamwork", "Event planning", "Communication"],
             f"Pick from reading buddy programs, school supply drives, tax help and one-day service projects around {c}."),
          ("scouting", "Leader or Merit Badge Counselor", "Scouting America", "care", 18, ["Leadership", "Teaching", "Outdoor work"],
             f"Lead a troop or pack, or teach a merit badge in a skill you know, around {c}. Free online training."),
          ("4h", "4-H Volunteer Leader", f"{stname} 4-H", "care", 18, ["Teaching", "Leadership", "Animals", "Crafts"],
             f"Lead a club or teach a project (art, cooking, animals, robotics) for kids around {c} through the state's 4-H program."),
          ("toys", "Toy Drive Volunteer (fall & winter)", "Marine Toys for Tots", "people", 14, ["Teamwork", "Organization", "Lifting"],
             f"Sort, wrap and hand out donated toys for families around {c} during the holiday season."),
          ("aws", "Event Volunteer", "Alzheimer's Association", "people", 14, ["Event planning", "Teamwork", "Customer service"],
             f"Help run the Walk to End Alzheimer's and community events around {c}, or train to lead education talks."),
        ]:
            out.append(vol(f"vol-{k}-{sfx}", title, comp, cat, age, skills, summ, findUrl=gsearch(f"{comp} volunteer {c} {st}"), **base))

# ---- more remote / from home ----
for id_, title, comp, cat, age, skills, summ in [
  ("vol-upchieve", "Online Tutor", "UPchieve", "brainy", 18, ["Tutoring", "Teaching", "Math", "Writing"], "Tutor low-income high schoolers by chat in math, science, writing or college prep, whenever you have 30 minutes."),
  ("vol-schoolhouse", "Peer Tutor", "Schoolhouse.world", "brainy", 13, ["Tutoring", "Teaching", "Math", "Public speaking"], "Lead small free Zoom tutoring sessions in subjects you've shown you know. Teens welcome."),
  ("vol-trevor", "Crisis Counselor", "The Trevor Project", "care", 18, ["Active listening", "Compassion", "Typing"], "Support LGBTQ+ young people by chat or text from home after free training."),
  ("vol-citizen-archivist", "Citizen Archivist", "U.S. National Archives", "brainy", 13, ["Typing", "Research", "Attention to detail"], "Transcribe and tag historical records from the National Archives, any time, from anywhere."),
  ("vol-pgdp", "Proofreader", "Distributed Proofreaders (Project Gutenberg)", "brainy", 13, ["Reading", "Attention to detail", "Writing"], "Check one page at a time of old books being turned into free ebooks."),
  ("vol-bookshare", "Book Proofreader", "Bookshare (Benetech)", "brainy", 13, ["Reading", "Attention to detail", "Computers"], "Proofread scanned books so students with disabilities can read them."),
  ("vol-dosomething", "Campaign Volunteer", "DoSomething.org", "people", 13, ["Leadership", "Social media", "Event planning"], "Pick from quick cause campaigns you can run at school or online. Built for ages 13 to 25."),
  ("vol-taproot", "Pro Bono Volunteer", "Taproot Foundation", "brainy", 18, ["Project management", "Marketing", "Graphic design", "Writing"], "Use work skills on short pro bono projects for nonprofits. Good portfolio pieces."),
  ("vol-moth-light", "Mapathon Volunteer", "Missing Maps", "brainy", 13, ["Computers", "Attention to detail"], "Join online or in-person mapathons to map places that aren't on any map yet."),
  ("vol-ftc-penpal", "Pen Pal for an Older Adult", "Love For Our Elders", "people", 13, ["Writing", "Friendly", "Compassion"], "Write handwritten letters to older adults in care homes who would love some mail."),
]:
    out.append(vol(id_, title, comp, cat, age, skills, summ, remote=True, findUrl=gsearch(f"{comp} volunteer")))

# ---- more Salt Lake City / Utah favorites ----
for id_, title, comp, cat, age, skills, summ, lat, lon, loc in [
  ("vol-ut-fourth-street", "Clinic Volunteer", "Fourth Street Clinic", "care", 18, ["Compassion", "Customer service", "Spanish"], "Help at the front desk, pharmacy and patient programs for people experiencing homelessness. Medical students and MAs welcome.", 40.76, -111.90, "Salt Lake City, UT"),
  ("vol-ut-neighborhood-house", "Volunteer", "Neighborhood House", "care", 16, ["Childcare", "Tutoring", "Compassion"], "Read, play and help with homework in child care and adult day programs on the west side.", 40.74, -111.91, "Salt Lake City, UT"),
  ("vol-ut-asian-assoc", "Volunteer", "Asian Association of Utah", "people", 16, ["Tutoring", "Bilingual", "Compassion"], "Tutor English, help with youth programs and support refugee and immigrant families.", 40.72, -111.89, "Salt Lake City, UT"),
  ("vol-ut-wcg", "Garden Volunteer", "Wasatch Community Gardens", "outdoors", 12, ["Gardening", "Outdoor work", "Teamwork"], "Plant, weed and harvest at community gardens and help at youth garden programs.", 40.74, -111.88, "Salt Lake City, UT"),
  ("vol-ut-treeutah", "Tree Planting Volunteer", "TreeUtah", "outdoors", 10, ["Outdoor work", "Gardening", "Teamwork"], "Plant and care for trees at Saturday events around the valley. Families welcome.", 40.76, -111.89, "Salt Lake City, UT"),
  ("vol-ut-umfa", "Museum Volunteer", "Utah Museum of Fine Arts", "creative", 16, ["Art", "Public speaking", "Customer service"], "Greet guests, help at art-making events and train as a gallery guide at the U's art museum.", 40.76, -111.84, "Salt Lake City, UT"),
  ("vol-ut-leonardo", "Museum Volunteer", "The Leonardo", "brainy", 14, ["Science", "Art", "Public speaking"], "Run hands-on science and art activities for visitors downtown.", 40.76, -111.89, "Salt Lake City, UT"),
  ("vol-ut-clark", "Volunteer", "Clark Planetarium", "brainy", 14, ["Science", "Public speaking", "Customer service"], "Help guests with exhibits and star shows at The Gateway.", 40.77, -111.90, "Salt Lake City, UT"),
  ("vol-ut-kostopulos", "Camp Volunteer", "Camp Kostopulos", "outdoors", 14, ["Childcare", "Patience", "Outdoor work"], "Help campers with disabilities swim, climb and do crafts at camp up Emigration Canyon.", 40.78, -111.79, "Salt Lake City, UT"),
  ("vol-ut-nac", "Adaptive Sports Volunteer", "National Ability Center", "outdoors", 16, ["Sports", "Coaching", "Patience"], "Help people with disabilities ski, ride horses, climb and more. Training provided.", 40.68, -111.48, "Park City, UT"),
  ("vol-ut-bike-collective", "Shop Volunteer", "Bicycle Collective", "hands-on", 14, ["Tools", "Repair", "Teaching"], "Fix up donated bikes and teach people to repair their own. You'll learn as you go.", 40.74, -111.90, "Salt Lake City, UT"),
  ("vol-ut-pride", "Volunteer", "Utah Pride Center", "people", 16, ["Event planning", "Customer service", "Compassion"], "Help at the community center, youth programs and the Utah Pride Festival.", 40.76, -111.90, "Salt Lake City, UT"),
  ("vol-ut-ywca", "Volunteer", "YWCA Utah", "care", 18, ["Childcare", "Compassion", "Teamwork"], "Help in children's programs, events and donation drives supporting women and families.", 40.76, -111.88, "Salt Lake City, UT"),
  ("vol-ut-encircle", "Volunteer", "Encircle", "care", 18, ["Compassion", "Friendly", "Event planning"], "Help at a home for LGBTQ+ youth and families with events, tutoring and hosting.", 40.76, -111.87, "Salt Lake City, UT"),
  ("vol-ut-sharing-place", "Grief Group Volunteer", "The Sharing Place", "care", 18, ["Compassion", "Active listening", "Childcare"], "Get trained to support kids and teens in grief support groups.", 40.68, -111.84, "Salt Lake City, UT"),
]:
    out.append(vol(id_, title, comp, cat, age, skills, summ, lat=lat, lon=lon, states=["UT"], location=loc, findUrl=gsearch(f"{comp} volunteer")))


L = [j for j in json.load(open("jobs-library.json")) if not j["id"].startswith("vol")]
for j in L:   # stipend service programs already in the starter list move into the volunteer section
    if j["company"] in ("AmeriCorps", "City Year"): j["volunteer"] = True
base = [j for j in L if not j["id"].startswith("loc")]; loc = [j for j in L if j["id"].startswith("loc")]
json.dump(base + out + loc, open("jobs-library.json", "w"), separators=(",", ":"))
print("volunteer listings:", len(out), "| library total:", len(base + out + loc))
