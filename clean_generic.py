"""Removes library jobs that don't name a real employer (like "Local restaurants"). Named local businesses replace them."""
import json
GENERIC = {"Hospitals","Hospitals & care centers","School districts","Universities","Universities & hospitals","Department stores",
 "Clinics & doctors' offices","Grocery store bakeries","Home improvement stores","Golf clubs","Senior living communities","Trucking companies",
 "Oil & gas companies","Print shops (shirts, stickers, embroidery)","Pro sports stadiums & arenas","Public libraries","City parks & recreation",
 "City parks departments","City arts programs / museums","Government & research firms","Wind farm operators","Remote call centers",
 "Remote creators & small businesses","Remote tech contractors","Remote tutoring companies","Ocean beach patrols","Washington orchards",
 "Alaska seafood processors","Alaska summer tour companies","Hawaii resorts","State parks departments","State parks & conservation corps",
 "State driver license offices","College & university dining halls"}
L = json.load(open("jobs-library.json"))
keep = [j for j in L if not (j["id"].startswith("sb") or (j["id"].startswith("lib") and (j["company"].startswith("Local") or j["company"] in GENERIC)))]
json.dump(keep, open("jobs-library.json","w"), separators=(",",":"))
print("removed", len(L) - len(keep), "unnamed jobs | left", len(keep))
