"""Adds official hiring pages (applyUrl) to starter-library jobs from big employers.
Only well-known careers sites; everything else keeps its "Find openings" search link."""
import json
CAREERS = {
 "7-Eleven":"https://careers.7-eleven.com", "AMC Theatres":"https://careers.amctheatres.com", "Academy Sports + Outdoors":"https://careers.academy.com",
 "Albertsons / Safeway":"https://www.albertsonscompanies.com/careers", "Aldi":"https://careers.aldi.us", "Amazon":"https://hiring.amazon.com",
 "AmeriCorps":"https://americorps.gov/join", "Apple Store":"https://www.apple.com/careers/us/retail.html", "Bank of America":"https://careers.bankofamerica.com",
 "Barnes & Noble":"https://careers.barnesandnoble.com", "Best Buy":"https://jobs.bestbuy.com", "Boeing":"https://jobs.boeing.com",
 "Bright Horizons":"https://careers.brighthorizons.com", "CVS Pharmacy":"https://jobs.cvshealth.com", "Chase":"https://careers.jpmorgan.com",
 "Chick-fil-A":"https://www.chick-fil-a.com/careers", "Chipotle":"https://jobs.chipotle.com", "City Year":"https://www.cityyear.org/apply/",
 "Costco":"https://www.costco.com/jobs.html", "Care.com & local families":"https://www.care.com", "Dollar General":"https://careers.dollargeneral.com",
 "DoorDash, Uber Eats, Instacart":"https://dasher.doordash.com", "Dutch Bros Coffee":"https://www.dutchbros.com/careers",
 "FedEx Ground":"https://careers.fedex.com", "FedEx Office":"https://careers.fedex.com", "GameStop":"https://careers.gamestop.com",
 "H&R Block":"https://www.hrblock.com/careers/", "H-E-B":"https://careers.heb.com", "Hilton hotels":"https://jobs.hilton.com",
 "Hobby Lobby":"https://careers.hobbylobby.com", "In-N-Out Burger":"https://www.in-n-out.com/employment", "Intermountain Health":"https://careers.intermountainhealth.org",
 "Job Corps":"https://www.jobcorps.gov", "Kaiser Permanente":"https://www.kaiserpermanentejobs.org", "KinderCare":"https://www.kindercare.com/careers",
 "Kohl's":"https://careers.kohls.com", "Kroger family stores":"https://www.krogerfamilycareers.com", "Lowe's":"https://talent.lowes.com",
 "Marriott hotels":"https://careers.marriott.com", "Mayo Clinic":"https://jobs.mayoclinic.org", "McDonald's":"https://careers.mcdonalds.com",
 "Meijer":"https://jobs.meijer.com", "Michaels":"https://careers.michaels.com", "National Park Service":"https://www.nps.gov/aboutus/workwithus.htm",
 "National Park Service / U.S. Forest Service":"https://www.nps.gov/aboutus/workwithus.htm", "Old Navy":"https://careers.gapinc.com",
 "Olive Garden":"https://www.darden.com/careers", "PNC Bank":"https://careers.pnc.com", "Panera Bread":"https://careers.panerabread.com",
 "PetSmart":"https://careers.petsmart.com", "Petco":"https://careers.petco.com", "Publix":"https://jobs.publix.com",
 "Raising Cane's":"https://www.raisingcanes.com/careers", "Ross Dress for Less":"https://jobs.rossstores.com", "Rover / Wag":"https://www.rover.com/become-a-sitter/",
 "Sephora":"https://jobs.sephora.com", "Sheetz":"https://jobs.sheetz.com", "Starbucks":"https://careers.starbucks.com", "T-Mobile":"https://careers.t-mobile.com",
 "TJ Maxx / Marshalls":"https://jobs.tjx.com", "TSA":"https://jobs.tsa.gov", "Taco Bell":"https://jobs.tacobell.com", "Target":"https://jobs.target.com",
 "Tesla":"https://www.tesla.com/careers", "The Home Depot":"https://careers.homedepot.com", "Trader Joe's":"https://www.traderjoes.com/home/careers",
 "UPS":"https://www.jobs-ups.com", "USPS":"https://about.usps.com/careers/", "Ulta Beauty":"https://careers.ulta.com",
 "Universal Orlando Resort":"https://www.universalorlandojobs.com", "Verizon":"https://mycareer.verizon.com", "Walgreens":"https://jobs.walgreens.com",
 "Walmart":"https://careers.walmart.com", "Walt Disney World":"https://jobs.disneycareers.com", "Disneyland Resort":"https://jobs.disneycareers.com",
 "Wegmans":"https://jobs.wegmans.com", "Wells Fargo":"https://www.wellsfargojobs.com", "Whole Foods Market":"https://careers.wholefoodsmarket.com",
 "U.S. Bank":"https://careers.usbank.com", "Truist":"https://careers.truist.com", "Banner Health":"https://www.bannerhealth.com/careers",
 "Cleveland Clinic":"https://jobs.clevelandclinic.org",
}
L = json.load(open("jobs-library.json"))
n = 0
for j in L:
    u = CAREERS.get(j["company"])
    if u and j["id"].startswith("lib"): j["applyUrl"] = u; n += 1
json.dump(L, open("jobs-library.json","w"), separators=(",",":"))
print("hiring pages added to", n, "jobs from", len(CAREERS), "employers")
