# Job Hunt

A phone-friendly job search app: find jobs that fit you, apply fast, track applications, and get ready for interviews. It runs entirely in the browser, so there's no server to set up.

Art for the profile pictures by **June Whitaker** · [@june.the.human](https://www.instagram.com/june.the.human/)

## What's in this folder

| File | What it is |
| --- | --- |
| `index.html` | The whole app, including the built-in library of about 128,500 jobs and volunteer spots |
| `presets/` | The 20 profile pictures |
| `jobs-library.json` | The job library as a separate file, in case you want to edit it |
| `Code.gs` | Optional Google script for one-tap emailing and reply alerts |

## Put it online (pick one, all free)

**Netlify Drop (easiest, about 1 minute)**
1. Go to https://app.netlify.com/drop
2. Drag the whole `job-hunt` folder onto the page.
3. You get a link like `https://something.netlify.app`. Sign up (free) to keep it and pick a nicer name.

**GitHub Pages**
1. Make a new public repository on GitHub and upload everything in this folder.
2. Open Settings → Pages, set the source to the `main` branch, and save.
3. Your site appears at `https://YOUR-NAME.github.io/REPO-NAME/` after a minute or two.

**Any other web host** (Neocities, Cloudflare Pages, your own site): upload the folder's contents as they are.

You can also just double-click `index.html` to try it on your own computer.

## How it works without a server

- **Accounts:** Each person picks a username and password the first time they open it. The password is stored only as a scrambled one-way hash.
- **Saving:** Everything (profile, jobs, tracker, reviews) is saved in that person's own browser, on that device. Use **Me → Backup** to save a file and load it on another phone.
- **Forgot password:** Because data stays on the device, a forgotten password means starting over on that device (or loading a backup).
- **Reviews:** Ratings and comments are saved on each person's own device. Sharing reviews between everyone would need an online database, like Firebase or Supabase, added later.
- **Reading postings and resumes:** Done by built-in rules in the app. No AI service is needed.
- **ZIP codes and distances:** Looked up with free public services (zippopotam.us for ZIP codes, OpenStreetMap for cities).
- **Resume PDFs:** Made in the browser with jsPDF, loaded from cdnjs.

## Optional: one-tap emailing + reply alerts

Open the app's **Setup** tab, or follow the steps at the top of `Code.gs`. It runs free in your own Google account and:
- emails applications from your Gmail with your resume attached
- alerts you (email + phone push through the free ntfy app) when a company replies
- puts interviews on your Google Calendar with reminders

Each person who wants this sets up their own copy.

## Editing the job library

`index.html` has the library built in (look for `id="libData"`). To change jobs, edit `jobs-library.json`, then paste its contents between the `<script type="application/json" id="libData">` and `</script>` tags in `index.html`. Each job can have a `states` list (like `["UT","ID"]`) to show it only to people in those states, and `location`, `lat` and `lon` so it shows a distance. The 4,114 local city, school, hospital, transit, university and state-government jobs were made with `gen_local.py`: edit its city lists and job templates and run it again to regenerate them.

There are also 398 named local businesses (indie bookstores, coffee shops, bakeries, ice cream shops, record stores and family restaurants) across all 50 states and DC, shown to people in that state with distances. Businesses can close or change, so each one links to a search for current openings. The 58 small-business jobs (coffee shops, bakeries, bookstores, studios, salons and more) show for everyone, with a "Find openings" search near their ZIP code.

Pay ranges in the library are typical starting ranges and change over time. The app labels them "typical" and links to live openings.


## How jobs load
Jobs are split into small per-state files in `jobs/` (made by `split_library.py`): `US.json` for national and remote jobs, `XX.json` for each state, and `towns-XX.json`, a tiny list of 2,016 towns (10,000+ people). The app turns each town into about 50 jobs at real local employers (city, schools, library, county, post office and big chains), so 100,000+ jobs load as a few hundred KB for your state. Town and county data comes from the plotly/datasets and kelvins/US-Cities-Database projects on GitHub.
