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

L = [j for j in json.load(open("jobs-library.json")) if not j["id"].startswith("vol")]
for j in L:   # stipend service programs already in the starter list move into the volunteer section
    if j["company"] in ("AmeriCorps", "City Year"): j["volunteer"] = True
base = [j for j in L if not j["id"].startswith("loc")]; loc = [j for j in L if j["id"].startswith("loc")]
json.dump(base + out + loc, open("jobs-library.json", "w"), separators=(",", ":"))
print("volunteer listings:", len(out), "| library total:", len(base + out + loc))
