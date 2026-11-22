// Job Hunt: live federal job postings from USAJOBS, near a place.
// GET /functions/v1/live-jobs?loc=Salt%20Lake%20City,%20UT&radius=50
// Secrets (Supabase → Edge Functions → Secrets): USAJOBS_KEY, USAJOBS_EMAIL.
// The key stays on the server; the app only ever sees the job list.

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  const key = Deno.env.get("USAJOBS_KEY"), email = Deno.env.get("USAJOBS_EMAIL");
  if (!key || !email) return Response.json({ error: "not_configured" }, { status: 503, headers: CORS });

  const u = new URL(req.url);
  const loc = (u.searchParams.get("loc") || "").slice(0, 80);
  const radius = Math.min(100, Math.max(10, Number(u.searchParams.get("radius")) || 50));
  const keyword = (u.searchParams.get("q") || "").slice(0, 60);
  if (!loc && !keyword) return Response.json({ error: "need_loc" }, { status: 400, headers: CORS });

  const q = new URLSearchParams({ ResultsPerPage: "250", SortField: "opendate", SortDirection: "desc" });
  if (loc) { q.set("LocationName", loc); q.set("Radius", String(radius)); }
  if (keyword) q.set("Keyword", keyword);

  const r = await fetch("https://data.usajobs.gov/api/search?" + q, {
    headers: { "Host": "data.usajobs.gov", "User-Agent": email, "Authorization-Key": key },
  });
  if (!r.ok) return Response.json({ error: "usajobs_" + r.status }, { status: 502, headers: CORS });
  const data = await r.json();
  const items = data?.SearchResult?.SearchResultItems || [];

  const jobs = items.map((it: any) => {
    const d = it.MatchedObjectDescriptor || {};
    const pay = (d.PositionRemuneration || [])[0] || {};
    const place = (d.PositionLocation || [])[0] || {};
    const ua = d.UserArea?.Details || {};
    return {
      id: String(it.MatchedObjectId || d.PositionID || ""),
      title: d.PositionTitle || "",
      company: d.OrganizationName || d.DepartmentName || "U.S. Government",
      dept: d.DepartmentName || "",
      location: d.PositionLocationDisplay || place.LocationName || "",
      lat: place.Latitude ?? null,
      lon: place.Longitude ?? null,
      payMin: pay.MinimumRange ? Number(pay.MinimumRange) : null,
      payMax: pay.MaximumRange ? Number(pay.MaximumRange) : null,
      payUnit: pay.RateIntervalCode === "PH" ? "hour" : pay.RateIntervalCode === "PA" ? "year" : null,
      schedule: ((d.PositionSchedule || [])[0] || {}).Name || "",
      summary: String(ua.JobSummary || d.QualificationSummary || "").slice(0, 400),
      applyUrl: (d.ApplyURI || [])[0] || d.PositionURI || "",
      posted: d.PublicationStartDate || "",
      closes: d.ApplicationCloseDate || "",
      remote: !!(ua.RemoteIndicator),
    };
  }).filter((j: any) => j.id && j.title);

  return Response.json({ count: jobs.length, total: data?.SearchResult?.SearchResultCountAll ?? jobs.length, jobs },
    { headers: { ...CORS, "Cache-Control": "public, max-age=3600" } });
});
