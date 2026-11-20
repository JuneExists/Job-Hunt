"""Adds birth-work and starter therapy-type jobs (ids start with "bw").
1) Named doula organizations checked online in Nov 2026 (Pomelo Care, The Doula Network, Malama Health,
   Mamatoto Village, Ancient Song, Uzazi Village) plus Bornbir for finding private clients.
2) In every city that has a named hospital: Childbirth Educator, OB/GYN Medical Assistant,
   Perinatal Patient Navigator, Mental Health Technician. Plus a WIC Breastfeeding Peer Counselor in every city.
Pay for hospital and WIC roles is a typical range, not a posted wage. Contract doula pay varies, so it's left blank."""
import json, re, urllib.parse

src = open("gen_local.py").read()
ns = {}
exec(src[:src.index("CITY = [")], ns)          # loads the city table S and hospital names H without generating anything
S, H = ns["S"], ns["H"]
B = {"H":"Health insurance","D":"Dental","V":"Vision","R":"Retirement (401k)","P":"Paid time off","F":"Flexible schedule","T":"Tuition help","E":"Employee discount","B":"Bonus / tips"}
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
gsearch = lambda q: "https://www.google.com/search?q=" + urllib.parse.quote(q)

def job(id, title, company, ty, pmn, pmx, yrs, edu, certs, skills, bens, summary, **kw):
    j = {"id": id, "library": True, "title": title, "company": company, "category": "care", "type": ty,
         "payMin": pmn, "payMax": pmx, "payUnit": "hour", "minAge": 18, "teen": False, "minYears": yrs, "education": edu,
         "certs": certs, "skills": skills, "benefits": [B[b] for b in bens], "summary": summary, "remote": False}
    j.update(kw); return j

out = []
DOULA_SKILLS = ["Doula", "Childbirth education", "Postpartum care", "Prenatal care", "Compassion", "Communication"]
DOULA_CERTS = ["Doula certification", "CPR / First Aid"]
# ---- named organizations ----
out.append(job("bwn-pomelo-doula", "Doula (contract)", "Pomelo Care", "contract", None, None, 1, None, DOULA_CERTS, DOULA_SKILLS, "F",
  "Support families in pregnancy, birth and postpartum through Pomelo's doula network. Pomelo handles insurance credentialing and billing for you. Hiring by state; check that yours is open.",
  states=["CA","MA","PA","GA","MO","NV","VA","DE","KS","NY","LA"], applyUrl="https://job-boards.greenhouse.io/pomelocare"))
out.append(job("bwn-pomelo-virtual", "Virtual Doula", "Pomelo Care", "full-time", None, None, 5, None, ["Doula certification"], DOULA_SKILLS + ["Video calls"], "F",
  "Support expecting parents by video from home. Asks for about 5 years of doula experience (or labor & delivery nursing).",
  remote=True, applyUrl="https://job-boards.greenhouse.io/pomelocare"))
out.append(job("bwn-doula-network", "Doula", "The Doula Network", "contract", None, None, 1, None, DOULA_CERTS, DOULA_SKILLS, "F",
  "Join a network of birth and full-spectrum doulas serving families, including Medicaid members. Postings are by state, and some roles are virtual.",
  states=["CA"], applyUrl="https://job-boards.greenhouse.io/thedoulanetwork"))
out.append(job("bwn-malama", "Community Doula (contract)", "Malama Health", "contract", None, None, 1, None, DOULA_CERTS, DOULA_SKILLS, "F",
  "Support pregnant and postpartum Medicaid members as part of Malama's doula network. Hybrid, statewide roles.",
  states=["NY","MN","LA"], applyUrl="https://apply.workable.com/malama-health/"))
out.append(job("bwn-mamatoto", "Perinatal Support / Doula", "Mamatoto Village", "full-time", None, None, 1, None, ["Doula certification"], DOULA_SKILLS, "",
  "DC nonprofit offering perinatal support and building career pathways in maternal health.",
  states=["DC"], location="Washington, DC", lat=38.89, lon=-76.95, findUrl=gsearch("Mamatoto Village careers")))
out.append(job("bwn-ancient-song", "Full-Spectrum Doula", "Ancient Song Doula Services", "part-time", None, None, 1, None, ["Doula certification"], DOULA_SKILLS, "F",
  "Brooklyn birth justice organization providing doula care, doula training and community education.",
  states=["NY"], location="New York City, NY", lat=40.68, lon=-73.94, findUrl=gsearch("Ancient Song Doula Services jobs")))
out.append(job("bwn-uzazi", "Village Doula / Community Health Worker", "Uzazi Village", "part-time", None, None, 1, None, ["Doula certification"], DOULA_SKILLS + ["Community outreach"], "F",
  "Kansas City nonprofit working to end maternal health disparities, with a community doula and home-visiting program.",
  states=["MO","KS"], location="Kansas City, MO", lat=39.06, lon=-94.55, findUrl=gsearch("Uzazi Village jobs")))
out.append(job("bwn-bornbir", "Independent Birth & Postpartum Doula (find clients)", "Bornbir", "contract", None, None, 1, None, ["Doula certification"], DOULA_SKILLS, "F",
  "Self-employed: expecting parents post what support they want (birth doula, postpartum doula, childbirth classes), and you reach out. Lots of requests across Utah.",
  remote=True, applyUrl="https://www.bornbir.com/ut/doula/jobs"))

# ---- every city ----
for st, (name, cities, uni) in S.items():
    for (c, lat, lon) in cities:
        h = H.get(st, {}).get(c)
        base = dict(states=[st], location=f"{c}, {st}", lat=lat, lon=lon)
        k = f"{slug(st)}-{slug(c)}"
        if h:
            out.append(job(f"bw-{k}-cbe", "Childbirth Educator", h, "part-time", 24.0, 36.0, 1, None, ["Childbirth educator certification"],
              ["Childbirth education", "Teaching", "Public speaking", "Doula", "Prenatal care"], "FRP",
              f"Teach childbirth, breastfeeding and newborn care classes for expecting families at {h}. Doula and teaching experience count a lot.",
              findUrl=gsearch(f"{h} childbirth educator jobs"), **base))
            out.append(job(f"bw-{k}-obma", "Medical Assistant, OB/GYN & Women's Health", h, "full-time", 18.0, 24.0, 1, "highschool", ["Medical assistant certification"],
              ["Medical assistant", "Patient care", "Vitals", "Scheduling", "Prenatal care"], "HDVRPT",
              f"Room patients, take vitals and help providers in the OB/GYN and women's health clinics at {h}. Prenatal and postpartum experience is a plus.",
              findUrl=gsearch(f"{h} medical assistant OB/GYN jobs"), **base))
            out.append(job(f"bw-{k}-nav", "Perinatal Patient Navigator", h, "full-time", 21.0, 28.0, 2, "bachelor", [],
              ["Patient care", "Prenatal care", "Case management", "Communication", "Doula"], "HDVRPT",
              f"Guide pregnant and new parents through appointments, insurance and community resources at {h}. A great fit for doulas and medical assistants.",
              findUrl=gsearch(f"{h} patient navigator maternal jobs"), **base))
            out.append(job(f"bw-{k}-mht", "Mental Health Technician", h, "full-time", 17.0, 23.0, 0, "highschool", [],
              ["Compassion", "Patience", "De-escalation", "Teamwork", "Patient care"], "HDVRPT",
              f"Support patients day to day in a behavioral health unit at {h}. A common first step into therapy work, and many places train you.",
              findUrl=gsearch(f"{h} mental health technician jobs"), **base))
        out.append(job(f"bw-{k}-wic", "Breastfeeding Peer Counselor", f"WIC Program ({c} area)", "part-time", 16.0, 22.0, 0, "highschool", [],
          ["Lactation support", "Communication", "Compassion", "Doula", "Postpartum care"], "F",
          f"Help new parents with breastfeeding through the WIC program around {c}. WIC trains you; most programs ask that you've breastfed a baby yourself.",
          findUrl=gsearch(f"WIC breastfeeding peer counselor jobs {c} {st}"), **base))

L = [j for j in json.load(open("jobs-library.json")) if not j["id"].startswith("bw")]
base = [j for j in L if not j["id"].startswith("loc")]; loc = [j for j in L if j["id"].startswith("loc")]
json.dump(base + out + loc, open("jobs-library.json", "w"), separators=(",", ":"))
print("birth-work & therapy jobs:", len(out), "| library total:", len(base + out + loc))
