/**
 * Job Hunt Helper — Google Apps Script backend
 * ---------------------------------------------
 * Runs inside YOUR Google account, for free. It:
 *   1. Sends application emails from your Gmail with your resume attached.
 *   2. Watches your inbox for replies from companies you applied to.
 *   3. Emails you and sends a push notification to your phone (or a text) when a company responds.
 *   4. Puts interviews on your Google Calendar and reminds you the day before and 2 hours before.
 *
 * UPDATING? If you already set this up: paste the new version over the old one,
 * then Deploy → Manage deployments → pencil icon → Version: "New version" → Deploy.
 * The Web app URL stays the same. Approve the new Calendar permission if asked.
 *
 * SETUP (about 10 minutes, once):
 *   1. Upload your resume PDF to Google Drive. Open it, and copy the ID from
 *      the link: drive.google.com/file/d/<THIS PART>/view
 *   2. Go to script.google.com → New project. Delete what's there and paste
 *      this whole file in. Fill in the CONFIG section just below.
 *   3. Click Deploy → New deployment → gear icon → "Web app".
 *        Execute as: Me
 *        Who has access: Only myself      ← important: keeps strangers out
 *      Click Deploy, approve the permissions, and copy the Web app URL.
 *   4. Back in the editor, pick "setup" in the function dropdown and click Run.
 *      That turns on the reply checker (every 10 minutes) and sends you a
 *      test email + text so you know alerts work.
 *   5. Paste the Web app URL into the Setup tab of the Job Hunt site.
 */

// ============================ CONFIG ============================
const CONFIG = {
  // Google Drive file ID of your resume (a PDF or a Google Doc both work).
  // Paste your resume's Drive link in Job Hunt (Me → Your resume) and it shows you this ID.
  RESUME_FILE_ID: 'PASTE_YOUR_RESUME_FILE_ID_HERE',

  // Where reply alerts go. Leave blank to use your own Gmail address.
  NOTIFY_EMAIL: '',

  // ---- Phone push notifications (free, works on iPhone and Android) ----
  // The Job Hunt Setup tab fills this in for you when you copy the script.
  // To do it by hand:
  // 1. Install the free "ntfy" app: iPhone https://apps.apple.com/app/id1625396347
  //    Android https://play.google.com/store/apps/details?id=io.heckel.ntfy
  // 2. Open it, allow notifications, tap +, type a channel ("topic") name only
  //    you would guess, like "june-jobs-7f3k9q", and tap Subscribe.
  //    (Anyone who knows the name can see the alerts, so make it random.)
  // 3. Put the same name between the quotes below.
  NTFY_TOPIC: '',

  // ---- Text message alerts (optional): fill in ONE of the two options ----

  // Option A: an email address that turns into a text on your phone.
  // Most big carriers have shut theirs down; Google Fi still works
  // (5551234567@msg.fi.google.com). Paid relays like
  // +15551234567@sendemailtotext.com also work for any carrier.
  SMS_EMAIL: '',

  // Option B (most reliable): Twilio. Costs about a penny per text; US
  // numbers need a quick registration in the Twilio console first.
  TWILIO_ACCOUNT_SID: '',
  TWILIO_AUTH_TOKEN: '',
  TWILIO_FROM_NUMBER: '', // your Twilio number, like +15551234567
  MY_PHONE_NUMBER: '',    // your cell, like +15551234567

  // Also text you for automatic "we received your application" emails?
  // (Those always still get an email alert.)
  TEXT_ON_CONFIRMATIONS: false,

  // Gmail label added to every application thread.
  LABEL: 'Job Applications',
};
// ================================================================

const PREFIX = 'app_';

/** Web app entry point. The Job Hunt site opens links to this URL. */
function doGet(e) {
  const p = (e && e.parameter) || {};
  try {
    if (p.action === 'send') return page_(sendApplication_(p));
    if (p.action === 'track') return page_(trackApplication_(p));
    if (p.action === 'interview') return page_(saveInterview_(p));
    if (p.action === 'check') { checkReplies(); return page_(statusHtml_('Checked just now.')); }
    return page_(statusHtml_(''));
  } catch (err) {
    return page_('<h2>Something went wrong</h2><p>' + esc_(err.message) + '</p>');
  }
}

/** Sends one application email with the resume attached. */
function sendApplication_(p) {
  const id = clean_(p.id) || ('j' + Date.now());
  const existing = getApp_(id);
  if (existing && existing.sentAt) {
    return '<h2>Already sent ✓</h2><p>Your application to <b>' + esc_(existing.company) +
      '</b> went out on ' + new Date(existing.sentAt).toLocaleString() +
      '. It was not sent twice.</p>';
  }
  const to = String(p.to || '').trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(to)) throw new Error('That email address doesn\'t look right: ' + to);
  if (p.attach !== '0' && CONFIG.RESUME_FILE_ID.indexOf('PASTE') === 0) throw new Error('Add your resume\'s Drive file ID to CONFIG first.');

  const subject = String(p.subject || 'Application').slice(0, 250);
  const body = String(p.body || '');
  // attach=0 (used for thank-you notes) sends without the resume.
  const options = p.attach === '0' ? {} : { attachments: [DriveApp.getFileById(CONFIG.RESUME_FILE_ID).getBlob()] };
  if (p.name) options.name = String(p.name);

  const msg = GmailApp.createDraft(to, subject, body, options).send();
  const thread = msg.getThread();
  thread.addLabel(label_());

  const app = {
    id: id, company: String(p.company || to.split('@')[1]), role: String(p.role || ''),
    method: 'email', to: to, domain: domainOf_(p.domain || to),
    threadId: thread.getId(), sentAt: Date.now(), repliedAt: null, replySnippet: '',
  };
  saveApp_(app);
  return '<h2>Sent ✓</h2><p>Your application to <b>' + esc_(app.company) + '</b>' +
    (app.role ? ' for <b>' + esc_(app.role) + '</b>' : '') + ' was emailed to ' + esc_(to) +
    ' with your resume attached.</p><p>You\'ll get an email and a text when they reply. You can close this tab.</p>';
}

/** Starts watching for replies to an application you submitted on a company's site. */
function trackApplication_(p) {
  const id = clean_(p.id) || ('j' + Date.now());
  const company = String(p.company || '').trim();
  if (!company) throw new Error('Missing company name.');
  const app = getApp_(id) || {
    id: id, company: company, role: String(p.role || ''), method: 'form', to: '',
    domain: domainOf_(p.domain || ''), threadId: '', sentAt: Date.now(), repliedAt: null, replySnippet: '',
  };
  saveApp_(app);
  return '<h2>Watching for replies ✓</h2><p>I\'ll email and text you when <b>' + esc_(company) +
    '</b> writes back' + (app.domain ? ' (from ' + esc_(app.domain) + ')' : '') + '. You can close this tab.</p>';
}

/** Adds (or moves) an interview on your Google Calendar, with reminders. */
function saveInterview_(p) {
  const id = clean_(p.id);
  if (!id) throw new Error('Missing interview id.');
  const start = new Date(p.start);
  if (isNaN(start.getTime())) throw new Error('That interview time didn\'t make sense.');
  const mins = Math.max(15, Math.min(480, Number(p.mins) || 60));
  const end = new Date(start.getTime() + mins * 60000);
  const company = String(p.company || 'Interview');
  const title = '🎤 Interview: ' + company + (p.role ? ' (' + p.role + ')' : '');
  const desc = [p.kind ? 'Type: ' + p.kind : '', p.notes || '', 'Added by Job Hunt'].filter(String).join('\n\n');
  const cal = CalendarApp.getDefaultCalendar();
  const key = 'int_' + id;
  const old = props_().getProperty(key);
  let ev = null;
  if (old) { try { ev = cal.getEventById(JSON.parse(old).eventId); } catch (e) {} }
  if (ev) {
    ev.setTime(start, end); ev.setTitle(title); ev.setLocation(String(p.where || '')); ev.setDescription(desc);
  } else {
    ev = cal.createEvent(title, start, end, { location: String(p.where || ''), description: desc });
    ev.removeAllReminders(); ev.addPopupReminder(24 * 60); ev.addPopupReminder(120);
  }
  props_().setProperty(key, JSON.stringify({ id: id, company: company, role: String(p.role || ''), where: String(p.where || ''),
    start: start.getTime(), eventId: ev.getId(), sent24: false, sent2: false }));
  return '<h2>On your calendar ✓</h2><p><b>' + esc_(title) + '</b><br>' + esc_(start.toLocaleString()) +
    (p.where ? '<br>' + esc_(p.where) : '') + '</p><p>You\'ll get a reminder the day before and 2 hours before. You can close this tab.</p>';
}

/** Sends push + email reminders 1 day and 2 hours before each interview. */
function checkInterviews_() {
  const all = props_().getProperties(), now = Date.now();
  Object.keys(all).forEach(function (k) {
    if (k.indexOf('int_') !== 0) return;
    const iv = JSON.parse(all[k]);
    if (now > iv.start + 86400000) { props_().deleteProperty(k); return; }
    const when = new Date(iv.start).toLocaleString();
    let changed = false;
    if (!iv.sent24 && now >= iv.start - 86400000 && now < iv.start) {
      const t = '🎤 Interview tomorrow: ' + iv.company;
      sendPush_(t, when + (iv.where ? ' · ' + iv.where : '') + '\nYou\'ve got this! Open Job Hunt for your prep list.', '', false);
      MailApp.sendEmail(CONFIG.NOTIFY_EMAIL || Session.getEffectiveUser().getEmail(), t, 'Your interview with ' + iv.company +
        (iv.role ? ' for ' + iv.role : '') + ' is ' + when + (iv.where ? ' at ' + iv.where : '') + '.\n\nYou\'ve got this!');
      iv.sent24 = true; changed = true;
    }
    if (!iv.sent2 && now >= iv.start - 7200000 && now < iv.start) {
      sendPush_('⏰ Interview in 2 hours: ' + iv.company, when + (iv.where ? ' · ' + iv.where : ''), '', false);
      iv.sent2 = true; iv.sent24 = true; changed = true;
    }
    if (changed) props_().setProperty(k, JSON.stringify(iv));
  });
}

/** Runs every 10 minutes (set up by setup()). Looks for new replies and upcoming interviews. */
function checkReplies() {
  try { checkInterviews_(); } catch (e) { Logger.log(e); }
  const me = Session.getEffectiveUser().getEmail().toLowerCase();
  allApps_().forEach(function (app) {
    if (app.repliedAt) return;
    const hit = findReply_(app, me);
    if (!hit) return;
    app.repliedAt = hit.date.getTime();
    app.replyFrom = hit.from;
    app.replySubject = hit.subject;
    app.replySnippet = hit.snippet;
    app.confirmation = isAutoConfirmation_(hit.subject + ' ' + hit.snippet);
    saveApp_(app);
    hit.thread.addLabel(label_());
    notify_(app, hit);
  });
}

function findReply_(app, me) {
  const after = Math.floor(app.sentAt / 1000);
  const threads = [];
  if (app.threadId) {
    try { threads.push(GmailApp.getThreadById(app.threadId)); } catch (e) {}
  }
  const parts = [];
  if (app.domain && !isGenericDomain_(app.domain)) parts.push('from:' + app.domain);
  if (app.company) parts.push('from:"' + app.company.replace(/"/g, '') + '"');
  if (app.company && app.method === 'form') parts.push('subject:"' + app.company.replace(/"/g, '') + '"');
  if (parts.length) {
    const q = '(' + parts.join(' OR ') + ') after:' + after + ' -from:me -in:sent -in:chats';
    GmailApp.search(q, 0, 10).forEach(function (t) { threads.push(t); });
  }
  for (let i = 0; i < threads.length; i++) {
    const msgs = threads[i].getMessages();
    for (let j = 0; j < msgs.length; j++) {
      const m = msgs[j];
      const from = m.getFrom();
      if (from.toLowerCase().indexOf(me) !== -1) continue;
      if (m.getDate().getTime() <= app.sentAt) continue;
      return {
        thread: threads[i], from: from, subject: m.getSubject(), date: m.getDate(),
        snippet: m.getPlainBody().replace(/\s+/g, ' ').trim().slice(0, 300),
        link: 'https://mail.google.com/mail/u/0/#all/' + threads[i].getId(),
      };
    }
  }
  return null;
}

function notify_(app, hit) {
  const to = CONFIG.NOTIFY_EMAIL || Session.getEffectiveUser().getEmail();
  const kind = app.confirmation ? 'confirmed your application' : 'replied';
  const subject = '📬 ' + app.company + ' ' + kind + (app.role ? ' (' + app.role + ')' : '');
  const body = app.company + ' ' + kind + '.\n\nFrom: ' + hit.from + '\nSubject: ' + hit.subject +
    '\n\n' + hit.snippet + '\n\nOpen in Gmail: ' + hit.link;
  MailApp.sendEmail(to, subject, body);
  sendPush_(subject, hit.subject + (hit.snippet ? '\n' + hit.snippet.slice(0, 160) : ''), hit.link, app.confirmation);
  if (!app.confirmation || CONFIG.TEXT_ON_CONFIRMATIONS) {
    sendText_(app.company + ' ' + kind + ' to your application' + (app.role ? ' for ' + app.role : '') +
      '. Subject: ' + hit.subject.slice(0, 80));
  }
}

function sendPush_(title, message, link, quiet) {
  if (!CONFIG.NTFY_TOPIC) return;
  const payload = { topic: CONFIG.NTFY_TOPIC, title: title.slice(0, 120), message: message.slice(0, 400),
    tags: [quiet ? 'envelope' : 'tada'], priority: quiet ? 3 : 4 };
  if (link) payload.click = link;
  UrlFetchApp.fetch('https://ntfy.sh/', {
    method: 'post', contentType: 'application/json', payload: JSON.stringify(payload), muteHttpExceptions: true,
  });
}

function sendText_(text) {
  text = text.slice(0, 300);
  if (CONFIG.TWILIO_ACCOUNT_SID && CONFIG.TWILIO_AUTH_TOKEN && CONFIG.TWILIO_FROM_NUMBER && CONFIG.MY_PHONE_NUMBER) {
    UrlFetchApp.fetch('https://api.twilio.com/2010-04-01/Accounts/' + CONFIG.TWILIO_ACCOUNT_SID + '/Messages.json', {
      method: 'post',
      payload: { To: CONFIG.MY_PHONE_NUMBER, From: CONFIG.TWILIO_FROM_NUMBER, Body: text },
      headers: { Authorization: 'Basic ' + Utilities.base64Encode(CONFIG.TWILIO_ACCOUNT_SID + ':' + CONFIG.TWILIO_AUTH_TOKEN) },
      muteHttpExceptions: true,
    });
  } else if (CONFIG.SMS_EMAIL) {
    MailApp.sendEmail(CONFIG.SMS_EMAIL, 'Job reply', text);
  }
}

/** Run this once from the editor. */
function setup() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'checkReplies') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('checkReplies').timeBased().everyMinutes(10).create();
  label_();
  const to = CONFIG.NOTIFY_EMAIL || Session.getEffectiveUser().getEmail();
  MailApp.sendEmail(to, '✅ Job Hunt alerts are on', 'This is a test. You\'ll get an email like this when a company replies.');
  sendPush_('✅ Job Hunt alerts are on', 'This is a test. You\'ll get one of these when a company replies.', '', false);
  sendText_('Job Hunt alerts are on. This is a test text.');
  Logger.log('Setup done. Reply checker runs every 10 minutes. Test email sent to ' + to);
}

// ---------------------------- helpers ----------------------------

function isAutoConfirmation_(s) {
  return /(thank(s| you) for (applying|your (application|interest))|application (has been )?(received|submitted)|we('ve| have) received your application|do not reply|no-?reply)/i.test(s);
}
function isGenericDomain_(d) {
  return /(gmail|yahoo|outlook|hotmail|icloud|greenhouse|lever|workday|myworkday|icims|smartrecruiters|indeed|linkedin|ziprecruiter|jobvite|ashbyhq|bamboohr)\./i.test(d);
}
function domainOf_(s) {
  s = String(s || '').trim().toLowerCase();
  if (!s) return '';
  if (s.indexOf('@') !== -1) s = s.split('@').pop();
  s = s.replace(/^https?:\/\//, '').replace(/^www\./, '').split('/')[0];
  return /^[a-z0-9.-]+\.[a-z]{2,}$/.test(s) ? s : '';
}
function clean_(s) { return String(s || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 60); }
function esc_(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
function label_() { return GmailApp.getUserLabelByName(CONFIG.LABEL) || GmailApp.createLabel(CONFIG.LABEL); }
function props_() { return PropertiesService.getScriptProperties(); }
function getApp_(id) { const v = props_().getProperty(PREFIX + id); return v ? JSON.parse(v) : null; }
function saveApp_(app) { props_().setProperty(PREFIX + app.id, JSON.stringify(app)); }
function allApps_() {
  const all = props_().getProperties();
  return Object.keys(all).filter(function (k) { return k.indexOf(PREFIX) === 0; })
    .map(function (k) { return JSON.parse(all[k]); })
    .sort(function (a, b) { return b.sentAt - a.sentAt; });
}

function statusHtml_(note) {
  const apps = allApps_();
  let rows = apps.map(function (a) {
    const st = a.repliedAt ? (a.confirmation ? '📨 Confirmation' : '📬 Replied') : '⏳ Waiting';
    return '<tr><td>' + esc_(a.company) + '</td><td>' + esc_(a.role || '') + '</td><td>' + (a.method === 'email' ? 'Email' : 'Website') +
      '</td><td>' + new Date(a.sentAt).toLocaleDateString() + '</td><td>' + st + '</td></tr>';
  }).join('');
  if (!rows) rows = '<tr><td colspan="5">No applications yet.</td></tr>';
  return '<h2>Your applications</h2>' + (note ? '<p>' + esc_(note) + '</p>' : '') +
    '<table><tr><th>Company</th><th>Role</th><th>How</th><th>Applied</th><th>Status</th></tr>' + rows + '</table>' +
    '<p><a href="?action=check">Check for replies now</a></p>';
}

function page_(inner) {
  return HtmlService.createHtmlOutput(
    '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:640px;margin:48px auto;padding:0 20px;color:#1d2a24}' +
    'h2{color:#1f5f4a}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:6px 8px;border-bottom:1px solid #ddd}a{color:#1f5f4a}</style>' +
    inner
  ).setTitle('Job Hunt').addMetaTag('viewport', 'width=device-width, initial-scale=1');
}
