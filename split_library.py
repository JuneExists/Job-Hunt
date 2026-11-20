"""Splits jobs-library.json into small per-state files the app loads on demand:
  jobs/US.json         jobs with no state (national, remote, chains "in most areas")
  jobs/XX.json         jobs for state XX
  jobs/towns-XX.json   compact town list [town, county, population, lat, lon]; the app turns each town into ~50 jobs"""
import json, os, collections
os.makedirs("jobs", exist_ok=True)
for f in os.listdir("jobs"): os.remove(os.path.join("jobs", f))
L = json.load(open("jobs-library.json"))
us, by = [], collections.defaultdict(list)
for j in L:
    if not j.get("states"): us.append(j)
    else:
        for st in j["states"]: by[st].append(j)
dump = lambda path, data: json.dump(data, open(path, "w"), separators=(",", ":"))
dump("jobs/US.json", us)
for st, a in by.items(): dump(f"jobs/{st}.json", a)
towns = json.load(open("towns.json")); tb = collections.defaultdict(list)
for t in sorted(towns, key=lambda t: -t["pop"]): tb[t["st"]].append([t["c"], t["county"], t["pop"], t["lat"], t["lon"]])
for st, a in tb.items(): dump(f"jobs/towns-{st}.json", a)
sizes = {f: os.path.getsize("jobs/" + f) for f in os.listdir("jobs")}
print("files:", len(sizes), "| US.json", sizes["US.json"] // 1024, "KB | biggest state:", max((v, k) for k, v in sizes.items() if not k.startswith("towns") and k != "US.json"),
      "| UT:", (sizes.get("UT.json", 0) + sizes.get("towns-UT.json", 0)) // 1024, "KB | all towns files:", sum(v for k, v in sizes.items() if k.startswith("towns")) // 1024, "KB")
