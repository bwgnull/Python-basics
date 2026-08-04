#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import textwrap

HOST = "127.0.0.1"
PORT = 8080

# ---------------------------------------------------------------------------
# Shared page shell. All per-page styling lives in CSS classes here instead
# of repeated inline styles, so individual page bodies stay short.
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = """<html>
<head><title>{title}</title>
<style>
  body {{
    font-family:'Courier New',monospace; font-size:22px; line-height:1.65;
    background-color:#02060a;
    background-image:
        linear-gradient(rgba(0,255,140,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,140,0.05) 1px, transparent 1px),
        radial-gradient(circle at 20% 20%, rgba(0,255,160,0.08), transparent 60%),
        linear-gradient(180deg, #03110a 0%, #020a06 60%, #000000 100%);
    background-size:42px 42px,42px 42px,cover,cover;
    background-attachment:fixed;
    color:#9dffc0; padding:6em 1.5em; margin:0; min-height:100vh;
  }}
  .shell {{
    max-width:{max_width}px; margin:0 auto; text-align:center;
    background:rgba(4,16,10,0.85); border:1px solid #1f5c3a; border-radius:10px;
    box-shadow:0 0 40px rgba(0,255,150,0.15), inset 0 0 64px rgba(0,60,30,0.25);
    padding:2.8em 3.2em;
  }}
  .banner {{
    color:#3dffa0; font-size:1.05em; letter-spacing:0.18em; text-transform:uppercase;
    margin:0 0 0.5em 0; border-bottom:1px dashed #1f5c3a; padding-bottom:0.8em;
  }}
  .home-btn {{
    display:inline-block; color:#5dffb0; background:#04140c; border:1px solid #1f5c3a;
    border-radius:6px; padding:0.35em 1em; font-size:0.85em; text-decoration:none;
    letter-spacing:0.04em;
  }}
  h1 {{ color:#5dffb0; text-shadow:0 0 14px rgba(93,255,176,0.5); margin-top:0.9em; font-size:2.9em; }}
  .footer {{ color:#3a8a63; font-size:0.95em; }}
  pre.art {{
    color:#5dffb0; background:#020e08; padding:1.6em; border-radius:10px;
    border:1px solid #1f5c3a; overflow-x:auto; font-size:1.3em; line-height:1.3;
    margin:0; display:inline-block; text-align:left;
    text-shadow:0 0 6px rgba(93,255,176,0.35);
  }}
  .art-wrap {{ display:flex; justify-content:center; }}

  /* Scenario cards: shared box used by every scam/lookalike/safe page */
  .card {{
    text-align:left; max-width:480px; margin:0 auto; padding:1.8em;
    border-radius:8px; background:#04140c; border:1px solid #1f5c3a;
  }}
  .card.warn {{ background:#160d05; border-color:#5c3a1f; }}
  .card.chrome {{ border-radius:0 0 8px 8px; }}
  .card .brand {{
    text-align:center; font-size:0.85em; margin-bottom:1em; letter-spacing:0.05em;
    color:#9dffc0;
  }}
  .card .brand .hl {{ color:#ffb05d; }}
  .card .field {{ color:#9dffc0; }}
  .card .field .v {{ color:#5dffb0; }}
  .card .field .v.warn {{ color:#ffb05d; }}
  .card .small {{ font-size:0.85em; color:#3a8a63; }}
  .card .small.warn {{ font-size:0.85em; color:#cf8a4a; }}
  .card .badge-row {{
    text-align:center; margin-top:1em; padding:0.6em; background:#1f3a0f;
    border-radius:6px; font-size:0.8em; color:#9dffc0;
  }}
  .card .alert-icon {{ text-align:center; color:#ff6a5d; font-size:2.2em; margin-bottom:0.3em; }}
  .card .alert-title {{ text-align:center; color:#ff6a5d; font-weight:bold; margin-top:0; }}
  .card .btn-fake {{
    display:inline-block; background:#3a1f0f; color:#ffb05d; padding:0.6em 1.4em;
    border-radius:6px; font-weight:bold;
  }}
  .card .pill {{
    display:inline-block; background:#1f3a2c; color:#5dffb0; padding:0.4em 1em;
    border-radius:6px; font-size:0.85em;
  }}
  .card p:first-child {{ margin-top:0; }}
  .card.plain {{ background:transparent; border:none; }}
  .lead-warn {{ color:#ffb05d; margin-top:0; }}
  .center {{ text-align:center; }}

  /* Browser chrome: fake address bar shown above scam/typosquat pages */
  .chromewrap {{ max-width:520px; margin:0 auto 1.2em auto; text-align:left; }}
  .addrbar {{
    display:flex; align-items:center; gap:0.6em; background:#0a1410;
    border:1px solid #1f3a2c; border-radius:8px 8px 0 0; padding:0.5em 0.8em;
  }}
  .addrbar .nav {{ color:#5c6b66; }}
  .addrbar .url {{
    flex:1; background:#000; border-radius:5px; padding:0.4em 0.7em;
    font-size:0.85em; overflow-x:auto; white-space:nowrap;
  }}
  .addrbar .url.unsafe {{ color:#ffb05d; }}
  .addrbar .url.safe {{ color:#5dffb0; }}
  .browser-warn {{
    background:#2a1505; border:1px solid #5c3a1f; border-top:none;
    padding:0.5em 0.9em; color:#ffb05d; font-size:0.8em;
  }}

  /* Flag/why-safe toggle */
  details.toggle {{ margin-top:1.4em; text-align:left; border-radius:8px; padding:0.9em 1.3em; }}
  details.toggle.bad {{ background:#160d05; border:1px solid #5c3a1f; }}
  details.toggle.good {{ background:#04140c; border:1px solid #1f5c3a; }}
  details.toggle summary {{ cursor:pointer; font-weight:bold; letter-spacing:0.03em; }}
  details.toggle.bad summary {{ color:#ff8a5d; }}
  details.toggle.good summary {{ color:#5dffb0; }}
  details.toggle ul {{ margin:0.9em 0 0.2em 0; padding-left:1.3em; color:#cfe8da; font-size:0.92em; line-height:1.5; }}
  details.toggle li {{ margin-bottom:0.6em; }}

  /* Webmail-style card used by /helpme */
  .mail {{ text-align:left; max-width:480px; margin:0 auto; border-radius:0 0 8px 8px;
           background:#0a1410; border:1px solid #1f3a2c; }}
  .mail .hdr {{ background:#0d1f17; padding:0.8em 1.2em; border-bottom:1px solid #1f3a2c; font-size:0.85em; color:#9dffc0; }}
  .mail .body {{ padding:1.4em; }}

  .lesson {{ text-align:left; max-width:560px; margin:0 auto; }}
  .lesson.small {{ font-size:0.9em; color:#3a8a63; }}
</style>
</head>
<body>
<div class="shell">
<p class="banner">&#x1F6E1;&#xFE0F; Loopback IT Security Awareness Station &mdash; Local Node</p>
<p><a class="home-btn" href="/">&#x1F3E0; Home</a></p>
<h1>{heading}</h1>
{body}
<hr style="border:none; border-top:1px dashed #1f5c3a; margin-top:2.5em;">
<p class="footer">Loopback Web Server &mdash; for security awareness training purposes only.</p>
</div>
</body>
</html>"""


def page(title, heading, body, max_width=1700):
    return PAGE_TEMPLATE.format(title=title, heading=heading, body=body, max_width=max_width)


def ascii_block(art):
    """Wrap ASCII art in a <pre> block so whitespace renders correctly.

    Uses textwrap.dedent to strip only the *common* leading whitespace
    across all lines (preserving each line's position relative to the
    others), so the art's internal shape stays intact. The block is then
    centered as a single rigid unit via a flex wrapper -- NOT via
    text-align:center on the <pre> itself, which would center each line
    independently and break vertical alignment between lines.
    """
    cleaned = textwrap.dedent(art).strip("\n")
    return f'<div class="art-wrap"><pre class="art">{cleaned}</pre></div>'


ASCII_LOOPBACK = r"""
   _____  .__              .__                ________         .__   __             ________
  /     \ |__| ______ _____|__| ____   ____   \______ \   ____ |  |_/  |______     /  _____/
 /  \ /  \|  |/  ___//  ___/  |/  _ \ /    \   |    |  \_/ __ \|  |\   __\__  \   /   __  \ 
/    Y    \  |\___ \ \___ \|  (  <_> )   |  \  |    `   \  ___/|  |_|  |  / __ \_ \  |__\  \
\____|__  /__/____  >____  >__|\____/|___|  / /_______  /\___  >____/__| (____  /  \_____  /
        \/        \/     \/               \/          \/     \/               \/         \/ 
"""

ASCII_LOCK = r"""
     ___________________
    |  ___  ACCESS      |
    | [ X ]  DENIED     |
    | [___]  [LOCKED]   |
    |___________________|
       |  |  |  |  |
       |__|__|__|__|
"""

ASCII_TIGER = r"""
   /\_/\
  ( o.o )
   > ^ <   ON PATROL
"""

ASCII_ROBOT = r"""
         ___
   _____/ o \____
  |   MONITOR    |
  |______  ______|
         \/
         ||
       __||__
      [______]
"""

ASCII_TROPHY = r"""      *
     /|\
    / | \
   *--+--*
  /   |   \
 *    |    *
  \   |   /
   \  |  /
    \ | /
     \|/
SECURITY AWARD
   EARNED"""


JOKES = {
    "qwerty": "The keyboard rolled over and this is what came out.",
    "starwars": "A long time ago, on a server far, far away... still no content.",
    "welcome": "Welcome! Make yourself at home. There isn't much furniture, though.",
    "tester": "Professional tester of empty pages, apparently.",
    "index": "You were looking for the index. This is just *an* index, of nothing.",
}


def browser_chrome(url, secure=False, warning=None):
    """Render a mock browser address bar above scenario content, so the
    page reads as 'a suspicious site you've landed on' rather than 'an
    email you received.' secure=True shows a padlock; secure=False shows
    a warning icon. An optional warning string renders as a thin
    browser-style warning strip just under the bar.
    """
    icon = "&#x1F512;" if secure else "&#x26A0;&#xFE0F;"
    url_class = "safe" if secure else "unsafe"
    html = (
        f'<div class="chromewrap"><div class="addrbar">'
        f'<span class="nav">&#x25C0;</span><span class="nav">&#x25B6;</span>'
        f'<span class="nav">&#x21BB;</span>'
        f'<div class="url {url_class}">{icon} {url}</div></div>'
    )
    if warning:
        html += f'<div class="browser-warn">{warning}</div>'
    html += "</div>"
    return html


def flag_toggle(items, label="Show red flags", good=False):
    """Render a collapsible <details> block listing red flags (or, when
    good=True, reasons a page is trustworthy). No JavaScript needed --
    <details>/<summary> handles the toggle natively.
    """
    cls = "good" if good else "bad"
    lines = "".join(f"<li>{item}</li>" for item in items)
    return f'<details class="toggle {cls}"><summary>{label}</summary><ul>{lines}</ul></details>'


def junk_body(slug):
    return f"<p>{JOKES.get(slug, 'Nothing much going on here.')}</p>"


def field(label, warn=False, kind="input"):
    """One label/value row inside a .card, e.g. 'Username: [input]'."""
    v_class = "v warn" if warn else "v"
    placeholder = "[file]" if kind == "file" else "[input]"
    return f'<p class="field">{label}: <span class="{v_class}">{placeholder}</span></p>'


def brand(name, highlight):
    return f'<div class="brand">{name} <span class="hl">{highlight}</span></div>'


def typo_lesson(fake_domain, real_domain, technique, explanation):
    """Mini-lesson page for a typosquatting example: fake browser chrome
    showing the lookalike domain, followed by a calm explanation of the
    specific technique used (no form, no red-flag toggle -- lighter touch
    than a full scam scenario, matching the .env/.git decoy style).
    """
    return (
        browser_chrome(fake_domain, secure=False)
        + f'<p class="lesson"><b style="color:#ffb05d;">Technique: {technique}</b><br>'
        f'This domain is designed to be mistaken for '
        f'<code style="color:#5dffb0;">{real_domain}</code>.</p>'
        f'<p class="lesson">{explanation}</p>'
        f'<p class="lesson small">This page doesn\'t connect anywhere &mdash; it\'s here '
        f'so you recognize the pattern, not to demonstrate the actual site.</p>'
    )


# ---------------------------------------------------------------------------
# Fake files served by the web server
# ---------------------------------------------------------------------------

FILES = {
    "/": (
        page(
            "Loopback IT Security Awareness Station",
            "&#x1F6E1;&#xFE0F; Loopback Station &mdash; Node Online",
            ascii_block(ASCII_LOOPBACK)
            + "<p>Congratulations on finding this node. This is a safe, isolated "
            "environment designed for learning about web security.</p>"
            "<p>Feel free to explore the various pages and see what you can find. "
            "The goal is to practice recognizing common patterns and red flags in "
            "URLs and page content, which can help you develop your skills in "
            "practicing safe browsing habits.</p>"
            "<div style='margin-top:1.8em; text-align:left; display:inline-block;'>"
            "<p style='color:#5dffb0; font-size:0.95em; letter-spacing:0.06em; "
            "text-transform:uppercase; margin-bottom:0.6em;'>Training Exercises</p>"
            "<ul style='color:#cfe8da; font-size:0.92em; line-height:1.7; padding-left:1.2em;'>"
            "<li><a href='/login' style='color:#9dffc0;'>/login</a> "
            "&mdash; a sample internal login page, plus a few lookalikes hidden elsewhere</li>"
            "<li><a href='/it-helpdesk' style='color:#9dffc0;'>/it-helpdesk</a> "
            "&mdash; a sample helpdesk contact page, plus a lookalike hidden elsewhere</li>"
            "<li><a href='/payroll' style='color:#9dffc0;'>/payroll</a> "
            "&mdash; a sample payroll page, plus a lookalike hidden elsewhere</li>"
            "<li><a href='/newsletter' style='color:#9dffc0;'>/newsletter</a> "
            "&mdash; a sample newsletter signup, plus a lookalike hidden elsewhere</li>"
            "<li>Plus several other pages scattered through the directory listing &mdash; "
            "some are harmless jokes, a few are worth a second look.</li>"
            "</ul>"
            "</div>",
        ),
        "text/html",
    ),

    "/tigers.html": (
        page(
            "Help Desk Mascot Roster",
            "&#x1F405; Help Desk Mascot Roster: TIGER Team",
            ascii_block(ASCII_TIGER)
            + "<ul>"
            "<li>TIGER-1 \"Bengal\" &mdash; team lead, the classic, the icon.</li>"
            "<li>TIGER-2 \"Siberian\" &mdash; keeps the biggest mug of coffee at the desk.</li>"
            "<li>TIGER-3 \"Sumatran\" &mdash; smallest mascot, biggest enthusiasm for password hygiene.</li>"
            "<li>TIGER-4 \"Malayan\" &mdash; the rare one you brag about working with.</li>"
            "</ul>",
        ),
        "text/html",
    ),

    "/robots.html": (
        page(
            "Directive: Monitoring Bots",
            "&#x1F916; Directive for Automated Monitoring Bots",
            ascii_block(ASCII_ROBOT)
            + "<p>User-agent: *<br>Disallow: /admin</p>"
            "<p>This file just politely asks automated visitors to stay "
            "out of certain folders. It's a courtesy request, not a lock "
            "&mdash; a good reminder that some protections need a real "
            "barrier behind them, not just a sign.</p>",
        ),
        "text/html",
    ),

    "/admin.html": (
        page(
            "Restricted Directory",
            "&#x1F6E1;&#xFE0F; Restricted Admin Panel",
            ascii_block(ASCII_LOCK)
            + "<p>Restricted Area &mdash; Authorized Staff Only</p>"
            "<p>(There's no actual login here. It's just a sign on an "
            "empty directory, like the 'employees only' door at a diner "
            "that just leads to a mop closet. Real admin panels should "
            "always sit behind proper authentication, not just a label.)</p>",
        ),
        "text/html",
    ),

    "/secret.html": (
        page(
            "Hidden Page",
            "&#x1F389; Hidden Page Located",
            ascii_block(ASCII_TROPHY)
            + "<p>You found the hidden page by exploring carefully &mdash; nice work.</p>"
            "<p>Here's your completion code &mdash; redeem it for a prize (Supply Pending)</p>"
            + ascii_block("CODE{loopback_hidden_page_found}")
            + "<p style='color:#3a8a63; font-size:0.85em;'>"
            "Congratulations! You've found the hidden page.</p>",
        ),
        "text/html",
    ),

    # --- Twin pair 1: internal login vs. fake "verify your account" ---

    "/login.html": (
        page(
            "Intranet Login",
            "&#x1F50F; Loopback Intranet &mdash; Sign In",
            "<div class='card'>"
            "<p >Sign in with your network username and password.</p>"
            + field("Username") + field("Password")
            + "<p class='small'>Forgot your password? Contact the help desk at "
            "extension 4100 or visit them in person.</p>"
            "</div>"
            + flag_toggle([
                "URL is a plain, predictable path on the same domain you'd expect (no copycat spelling).",
                "No urgency, countdowns, or threats &mdash; it just asks you to sign in.",
                "Password recovery points to a real internal channel (extension, in person), not a link or email reply.",
                "Doesn't ask you to 'confirm' or 're-verify' anything you didn't initiate.",
            ], label="Why this is safe", good=True),
        ),
        "text/html",
    ),

    "/account-verify.html": (
        page(
            "Account Verification Required",
            "&#x26A0;&#xFE0F; URGENT: Verify Your Account Now",
            browser_chrome(
                "loopback-secure-accounts.com/verify?session=88421",
                warning="&#x26A0;&#xFE0F; Not secure &mdash; this domain does not match your account provider",
            )
            + "<div class='card warn chrome'>"
            + brand("LOOPBACK", "ACCOUNTS")
            + "<p class='lead-warn'><b>Your account will be suspended in "
            "24 hours</b> unless you verify your identity immediately.</p>"
            "<p>Please confirm your username and current password below to keep your "
            "account active and avoid losing access to your files.</p>"
            + field("Username", warn=True) + field("Current Password", warn=True)
            + "<p class='small warn'>Failure to verify within 24 hours will result in "
            "permanent data loss. Act now!</p>"
            "</div>"
            + flag_toggle([
                "Address bar shows a domain ('loopback-secure-accounts.com') that just bolts trust-sounding words onto the real company name &mdash; not the actual account provider's domain.",
                "Browser flags the connection as not secure and notes the domain mismatch &mdash; both are signs to stop before entering anything.",
                "Artificial urgency and a countdown ('24 hours', 'act now') designed to short-circuit careful thinking.",
                "Asks you to type your *current password* into a page, which legitimate verification rarely requires.",
                "Threatens loss of access or data &mdash; fear-based pressure is a classic phishing tactic.",
                "No mention of a specific, verifiable contact method &mdash; just a form demanding credentials.",
            ]),
        ),
        "text/html",
    ),

    # --- Twin pair 2: real helpdesk contact vs. fake "urgent support" ---

    "/it-helpdesk.html": (
        page(
            "IT Help Desk",
            "&#x1F4DE; IT Help Desk &mdash; Contact Us",
            "<div class='card plain'>"
            "<p>Need help with a device, account, or software issue?</p>"
            "<ul style='line-height:1.7;'>"
            "<li>Call extension 4100 (internal) or 555-0142 (external)</li>"
            "<li>Submit a ticket through the internal ticketing portal</li>"
            "<li>Stop by the help desk counter, 2nd floor, 9am&ndash;5pm</li>"
            "</ul>"
            "<p class='small'>We will never ask for your password over the phone, "
            "by email, or through a web form.</p>"
            "</div>"
            + flag_toggle([
                "Gives specific, verifiable contact methods (extension, portal, physical location) instead of just a form.",
                "Explicitly states they will never ask for a password &mdash; a real policy statement, not a generic claim.",
                "No urgency, no scare language, no request for any information up front.",
                "Matches what you'd expect from a normal internal resource page.",
            ], label="Why this is safe", good=True),
        ),
        "text/html",
    ),

    "/it-support-urgent.html": (
        page(
            "IT Support Alert",
            "&#x1F6A8; Security Alert: Immediate Action Required",
            browser_chrome(
                "it-support-alert-center.net/security-notice?ref=44291",
                warning="&#x26A0;&#xFE0F; Dangerous site &mdash; this page has been reported for deceptive behavior",
            )
            + "<div class='card warn chrome'>"
            "<div class='alert-icon'>&#x1F6A8;</div>"
            "<p class='alert-title'>UNUSUAL ACTIVITY DETECTED</p>"
            "<p>Our systems have detected unusual activity on your account.</p>"
            "<p>To prevent unauthorized access, please call our IT Support hotline "
            "<b>right away</b> at the number below and provide your employee ID and "
            "current password for verification:</p>"
            "<p style='color:#ffb05d; font-size:1.2em; text-align:center;'>1-800-555-0199</p>"
            "<p class='small warn'>This alert was generated automatically. "
            "Do not ignore this message.</p>"
            "</div>"
            + flag_toggle([
                "Address bar shows a generic, unaffiliated domain ('it-support-alert-center.net') that has nothing to do with your actual employer or IT vendor.",
                "Browser itself has flagged the page as reported for deceptive behavior &mdash; a strong, independent signal to leave.",
                "Vague claim of 'unusual activity' with no specifics &mdash; designed to alarm rather than inform.",
                "Asks you to provide your password over the phone, which a legitimate help desk explicitly won't do.",
                "Generic 800-number instead of a known, internal extension you could cross-check.",
                "'Do not ignore this message' is pressure language meant to bypass your skepticism.",
            ]),
        ),
        "text/html",
    ),

    # --- Twin pair 3: real payroll page vs. fake "update direct deposit" ---

    "/payroll.html": (
        page(
            "Payroll Information",
            "&#x1F4B0; Payroll &mdash; General Information",
            "<div class='card plain'>"
            "<p>Paydays are the 1st and 15th of each month.</p>"
            "<p>To update direct deposit, tax withholding, or other payroll details, "
            "log in to the HR system directly using your normal credentials and "
            "navigate to <i>My Pay &rarr; Direct Deposit</i>.</p>"
            "<p class='small'>Payroll will never email or text you a link asking "
            "you to re-enter your banking details.</p>"
            "</div>"
            + flag_toggle([
                "Directs you to log in to the known HR system yourself, rather than clicking a link.",
                "No request for banking details on this page at all.",
                "States plainly that payroll will never ask you to re-enter details via a link &mdash; sets a clear expectation.",
                "Calm, informational tone with no urgency.",
            ], label="Why this is safe", good=True),
        ),
        "text/html",
    ),

    "/payroll-update.html": (
        page(
            "Payroll Update Needed",
            "&#x26A0;&#xFE0F; Action Needed: Direct Deposit Update",
            browser_chrome(
                "loopback-payroll-hr.net/update-deposit?emp=20144",
                warning="&#x26A0;&#xFE0F; This domain is not your company's payroll provider",
            )
            + "<div class='card warn chrome'>"
            + brand("LOOPBACK", "PAYROLL")
            + "<p class='lead-warn'>Your last direct deposit failed. "
            "To avoid a delay in your next paycheck, please re-enter your banking "
            "information below before end of day.</p>"
            + field("Bank Routing Number", warn=True) + field("Account Number", warn=True)
            + "<p class='small warn'>This must be completed today to avoid a delay "
            "in payment.</p>"
            "</div>"
            + flag_toggle([
                "Domain ('loopback-payroll-hr.net') mimics the company name but is a separate, unaffiliated site &mdash; not your actual HR/payroll system's domain.",
                "Browser explicitly notes this isn't your payroll provider's real domain.",
                "Directly requests sensitive banking details on the page itself, instead of pointing you to log in normally.",
                "Tight, same-day deadline designed to make you act before thinking it through.",
                "Pay disruption is a strong emotional hook &mdash; scammers know money lowers people's guard.",
                "No mention of any specific failed transaction details you could verify independently.",
            ]),
        ),
        "text/html",
    ),

    # --- Twin pair 4: real newsletter signup vs. fake "you've won" giveaway ---

    "/newsletter.html": (
        page(
            "Company Newsletter",
            "&#x1F4F0; Subscribe to the Company Newsletter",
            "<div class='card plain'>"
            "<p>Get monthly updates on company news, events, and announcements.</p>"
            + field("Email")
            + "<p class='small'>That's it &mdash; just your email. Unsubscribe "
            "anytime from the link in any issue.</p>"
            "</div>"
            + flag_toggle([
                "Asks for the minimum information needed (just an email) for what it's offering.",
                "No prize, no countdown, no pressure to act immediately.",
                "Clearly explains how to opt out later, which is a standard, trustworthy practice.",
            ], label="Why this is safe", good=True),
        ),
        "text/html",
    ),

    "/newsletter-winner.html": (
        page(
            "Congratulations Winner",
            "&#x1F389; You've Been Selected to Win!",
            browser_chrome(
                "monthly-giveaway-rewards.com/claim?winner=true",
                warning="&#x26A0;&#xFE0F; Not secure &mdash; avoid entering personal information",
            )
            + "<div class='card warn chrome'>"
            "<p class='lead-warn'>Congratulations! You've been "
            "randomly selected to receive a free gift card.</p>"
            "<p>To claim your prize, enter your full name, date of birth, email, "
            "and phone number below within the next 15 minutes:</p>"
            + field("Full Name", warn=True) + field("Date of Birth", warn=True)
            + field("Phone Number", warn=True)
            + "<p class='small warn'>Offer expires in 15:00 &mdash; don't miss out!</p>"
            "<div class='badge-row'>&#x2705; Verified Winner &middot; &#x2B50; "
            "5-Star Rated &middot; &#x1F512; 100% Secure</div>"
            "</div>"
            + flag_toggle([
                "Domain ('monthly-giveaway-rewards.com') isn't tied to any newsletter, store, or brand you actually signed up with.",
                "Browser flags the connection as not secure &mdash; a page collecting personal data should always be on HTTPS.",
                "You didn't enter any contest, yet you've supposedly 'won' &mdash; a classic unsolicited-prize red flag.",
                "Asks for far more personal data (DOB, phone) than a simple gift card would ever require.",
                "Self-applied badges like 'Verified Winner' or '100% Secure' aren't issued by any real authority &mdash; anyone can add that text to a page.",
                "Short countdown timer ('15:00') manufactures urgency to prevent careful thought.",
            ]),
        ),
        "text/html",
    ),

    # --- Standalone red-flag scenario pages ---

    "/winner.html": (
        page(
            "Prize Notification",
            "&#x1F3C6; You Have Won a Prize!",
            browser_chrome(
                "global-prize-rewards-center.com/winner?id=8842910",
                warning="&#x26A0;&#xFE0F; Not secure &mdash; this site's connection is not private",
            )
            + "<div class='card warn chrome'>"
            "<div style='text-align:center; font-size:0.75em; color:#ffb05d; "
            "letter-spacing:0.1em; text-transform:uppercase; margin-bottom:1em;'>"
            "&#x2728; Global Prize Rewards Center &#x2728;</div>"
            "<p class='lead-warn'>This is your final notice: you "
            "have won a brand new laptop! Enter your shipping details and a small "
            "processing fee payment below to claim it before midnight tonight.</p>"
            + field("Full Name / Address", warn=True)
            + field("Card Number (for $4.99 'processing fee')", warn=True)
            + "<div class='badge-row'>&#x2705; Verified Safe by 3 Trust Seals &mdash; "
            "SecurePay&#x2122; &middot; TrustGuard&#x2122; &middot; ShopSafe&#x2122;</div>"
            "</div>"
            + flag_toggle([
                "Address bar shows an unfamiliar, generic-sounding domain ('global-prize-rewards-center.com') with no connection to any site you actually visited.",
                "Browser flags the connection as not secure &mdash; legitimate payment pages always use HTTPS.",
                "'Final notice' for something you never entered is a strong unsolicited-prize tell.",
                "Made-up 'trust seal' badges (SecurePay&#x2122;, TrustGuard&#x2122;) are not real certifications &mdash; anyone can put a checkmark image on a page.",
                "Legitimate prizes don't require *you* to pay a fee to receive them.",
                "A hard deadline ('before midnight') pressures quick, unconsidered action.",
            ]),
        ),
        "text/html",
    ),

    "/success.html": (
        page(
            "Software Update Required",
            "&#x26A0;&#xFE0F; System Scan Complete &mdash; Threats Found",
            browser_chrome(
                "windows-defender-securitycheck.net/scan-results",
                warning="&#x26A0;&#xFE0F; Deceptive site ahead &mdash; attackers may be trying to trick you",
            )
            + "<div class='card warn chrome'>"
            "<div class='alert-icon'>&#x26A0;&#xFE0F;</div>"
            "<p class='alert-title'>3 THREATS DETECTED ON YOUR DEVICE</p>"
            "<p >Your scan finished. To remove the detected "
            "threats and finalize protection, please disable your current antivirus "
            "temporarily and run the attached verification tool below.</p>"
            "<div style='text-align:center; margin:1em 0;'>"
            "<span class='btn-fake'>&#x2B07;&#xFE0F; Download Fix Now</span></div>"
            "<p class='small warn'>Skipping this step may cause your system to "
            "become unstable.</p>"
            "</div>"
            + flag_toggle([
                "Address bar shows a domain mimicking Windows Defender, but it's not a microsoft.com domain &mdash; real Defender alerts never come from a website.",
                "Browser itself is flagging this as a deceptive site &mdash; a strong signal to leave immediately.",
                "Legitimate updates never ask you to disable your antivirus &mdash; that's a step designed to let something slip past your defenses.",
                "A 'Download Fix Now' button on an unexpected scan result is a classic way malware gets installed voluntarily.",
                "Vague threat of 'instability' if you don't comply is pressure without any real explanation.",
                "Real antivirus software runs as an installed program, not a popup served from a random website.",
            ]),
        ),
        "text/html",
    ),

    "/welcome.html": (
        page(
            "New Employee Portal Access",
            "&#x1F44B; Welcome! Complete Your Profile",
            browser_chrome(
                "loopback-hr-onboardlng.com/new-hire/profile",
                warning="&#x26A0;&#xFE0F; This domain was registered 6 days ago",
            )
            + "<div class='card warn chrome'>"
            + brand("LOOPBACK", "HR PORTAL")
            + "<p >Welcome to the team! To finish setting up "
            "your account, please enter your Social Security number, date of "
            "birth, and upload a copy of your driver's license below so we can "
            "complete onboarding today.</p>"
            + field("SSN", warn=True) + field("Date of Birth", warn=True)
            + field("Driver's License Upload", warn=True, kind="file")
            + "</div>"
            + flag_toggle([
                "Domain name is a near-miss lookalike of the real company name with a subtle misspelling ('onboardlng' instead of 'onboarding') &mdash; a classic typosquat.",
                "Browser shows the domain was registered very recently &mdash; scam sites are often thrown together days before use.",
                "Sensitive documents (SSN, license) should go through a secure, established HR system, never a freshly-registered look-alike domain.",
                "'Today' urgency on a brand-new employee is a common way to catch someone before they know the normal process.",
                "Real onboarding paperwork is typically handled in person or through a verified, long-standing company portal.",
            ]),
        ),
        "text/html",
    ),

    "/helpme.html": (
        page(
            "Webmail &mdash; 1 New Message",
            "&#x1F4E9; Webmail Preview",
            browser_chrome(
                "mail-loopback-corp.com/inbox/message?id=festured",
                warning="&#x26A0;&#xFE0F; This is not the company's verified mail domain",
            )
            + "<div class='mail'>"
            "<div class='hdr'><b>From:</b> J. Carter, VP Operations "
            "&lt;j.carter@mail-loopback-corp.com&gt;<br>"
            "<b>Subject:</b> Quick favor &mdash; need this ASAP</div>"
            "<div class='body'>"
            "<p >Hey, I'm stuck in back-to-back meetings and "
            "need you to buy some gift cards for a client and send me the codes. "
            "I'll pay you back. Please keep this between us for now &mdash; don't "
            "mention it to anyone else on the team yet.</p>"
            "</div></div>"
            + flag_toggle([
                "Sender's email domain ('mail-loopback-corp.com') resembles the company name but isn't the company's actual mail domain &mdash; a common spoofing tactic.",
                "Impersonation of a manager or executive ('CEO fraud') is one of the most common business email scams.",
                "Gift card requests are a near-universal scam pattern because the codes are instantly spendable and hard to trace.",
                "Asking you to keep it secret from coworkers removes the normal social check that would catch the scam.",
                "Vague urgency ('stuck in meetings', 'need this ASAP') discourages you from verifying through another channel.",
            ]),
        ),
        "text/html",
    ),

    "/access.html": (
        page(
            "Shared Drive Access Request",
            "&#x1F4C1; You've Been Granted Access &mdash; Sign In to View",
            browser_chrome(
                "drive-fileshare-secure.com/view?doc=4471&exp=600",
                warning="&#x26A0;&#xFE0F; This site is impersonating a file-sharing service",
            )
            + "<div class='mail' style='padding:1.8em;'>"
            "<div style='text-align:center; margin-bottom:1em;'>"
            "<span class='pill'>&#x1F4C4; Document Viewer</span></div>"
            "<p >A document has been shared with you. Sign "
            "in with your work email and password below to view it. This link "
            "will expire in 10 minutes.</p>"
            + field("Work Email", warn=True) + field("Password", warn=True)
            + "</div>"
            + flag_toggle([
                "Domain ('drive-fileshare-secure.com') isn't any real file-sharing provider's actual domain &mdash; it just borrows generic, trustworthy-sounding words.",
                "Browser explicitly flags this as an impersonation attempt.",
                "A short expiry window ('10 minutes') pressures you to act before checking whether the request is legitimate.",
                "Legitimate shared-document links from real platforms use single sign-on through the real provider's domain, not a generic password box on an unfamiliar page.",
                "No indication of who shared the document or why &mdash; a vague, unsolicited 'someone shared this with you' is a common credential-harvesting lure.",
                "If in doubt, navigate to the document platform directly rather than signing in through a link.",
            ]),
        ),
        "text/html",
    ),

    # --- Decoy "juicy" paths with short mini-lessons ---

    "/.env.html": (
        page(
            "Environment File",
            "&#x1F4DD; .env",
            "<p>Real <code>.env</code> files often hold database passwords, API "
            "keys, and other secrets that an application needs at runtime.</p>"
            "<p>If a web server accidentally serves this file to anyone who asks "
            "for it, an attacker can use those credentials directly &mdash; no "
            "further exploitation needed. That's why <code>.env</code> files "
            "should always be kept outside the web root and excluded from "
            "version control.</p>"
            "<p style='color:#3a8a63; font-size:0.9em;'>This particular file is "
            "empty by design &mdash; it's here so you recognize the pattern, not "
            "to demonstrate the actual risk.</p>",
        ),
        "text/html",
    ),

    "/wp-admin.html": (
        page(
            "WordPress Admin Path",
            "&#x1F4DD; /wp-admin",
            "<p>This is the default administrator login path for WordPress "
            "sites. Because so many sites run WordPress with default settings, "
            "automated scanners constantly probe this exact path looking for "
            "weak or reused passwords.</p>"
            "<p>Defensively: rate-limiting login attempts, enabling "
            "multi-factor authentication, and renaming or restricting access to "
            "admin paths all reduce the value of this path to an attacker.</p>",
        ),
        "text/html",
    ),

    "/config.html": (
        page(
            "Configuration File",
            "&#x1F4DD; config",
            "<p>Configuration files frequently contain database connection "
            "strings, internal hostnames, or service credentials. An exposed "
            "config file can hand an attacker a roadmap of your internal "
            "systems even if it doesn't contain a password directly.</p>"
            "<p>Defensively: configuration should be loaded from environment "
            "variables or a secrets manager rather than a file sitting in a "
            "web-accessible directory.</p>",
        ),
        "text/html",
    ),

    "/backup.zip.html": (
        page(
            "Backup Archive",
            "&#x1F4DD; backup.zip",
            "<p>Backup archives are a favorite target because they're often a "
            "complete snapshot of a system &mdash; source code, databases, and "
            "configuration all in one convenient, downloadable bundle.</p>"
            "<p>Defensively: backups should be stored outside the web root, "
            "access logged, and ideally encrypted, so a stray backup file "
            "can't become a one-stop breach.</p>",
        ),
        "text/html",
    ),

    "/.git.html": (
        page(
            "Git Repository Folder",
            "&#x1F4DD; .git",
            "<p>An exposed <code>.git</code> folder can let an attacker "
            "reconstruct an application's entire commit history &mdash; "
            "including old code, comments, and sometimes credentials that "
            "were committed and later removed but never actually "
            "invalidated.</p>"
            "<p>Defensively: version control folders should never be deployed "
            "to a public web root, and any secret that's ever been committed "
            "should be treated as compromised and rotated.</p>",
        ),
        "text/html",
    ),

    # --- Typosquatting examples: fake browser chrome + mini-lesson ---

    "/goggle.html": (
        page(
            "Typosquat Example",
            "&#x1F4DD; Typosquatting Example: Letter Repetition",
            typo_lesson(
                "goggle.com/search?q=loopback", "google.com", "Letter repetition",
                "Doubling a letter ('go<b>g</b>gle' instead of 'go<b>o</b>gle') is "
                "one of the oldest typosquatting tricks &mdash; it's a single "
                "keystroke away from the real spelling and easy to miss when "
                "typing quickly or glancing at a link.",
            ),
        ),
        "text/html",
    ),

    "/arnazon.html": (
        page(
            "Typosquat Example",
            "&#x1F4DD; Typosquatting Example: Look-Alike Characters",
            typo_lesson(
                "arnazon.com/orders", "amazon.com", "Look-alike characters",
                "Swapping 'm' for 'rn' (which renders almost identically in many "
                "fonts) is a classic visual trick. At a glance, especially on a "
                "small screen or low-res display, 'arnazon' can look just like "
                "'amazon.'",
            ),
        ),
        "text/html",
    ),

    "/paypa1.html": (
        page(
            "Typosquat Example",
            "&#x1F4DD; Typosquatting Example: Character Substitution",
            typo_lesson(
                "paypa1.com/signin", "paypal.com", "Character substitution",
                "Replacing a letter with a similar-looking number (the digit '1' "
                "instead of the letter 'l') is a common way to register a domain "
                "that looks right at a glance but is technically a completely "
                "different address.",
            ),
        ),
        "text/html",
    ),

    "/micros0ft.html": (
        page(
            "Typosquat Example",
            "&#x1F4DD; Typosquatting Example: Character Substitution",
            typo_lesson(
                "micros0ft-support.com/account", "microsoft.com",
                "Character substitution + extra words",
                "Swapping the letter 'o' for the digit '0' is another common "
                "substitution. Adding an extra word like '-support' is also "
                "typical &mdash; it makes the domain feel purposeful while still "
                "being a completely separate, unaffiliated site.",
            ),
        ),
        "text/html",
    ),

    "/facebok.html": (
        page(
            "Typosquat Example",
            "&#x1F4DD; Typosquatting Example: Missing Letter",
            typo_lesson(
                "facebok.com/login", "facebook.com", "Missing letter (omission)",
                "Dropping a single letter is one of the simplest typosquats to "
                "register and one of the easiest to type by accident yourself "
                "&mdash; which is exactly why scammers register these variants in "
                "bulk and wait for traffic.",
            ),
        ),
        "text/html",
    ),

    "/netflix-billing.html": (
        page(
            "Typosquat Example",
            "&#x1F4DD; Typosquatting Example: Subdomain Trick",
            typo_lesson(
                "netflix-billing.secure-update-center.com/payment", "netflix.com",
                "Subdomain / combosquatting trick",
                "Here the real brand name appears early in the URL "
                "('netflix-billing'), but it's actually part of a completely "
                "unrelated domain ('secure-update-center.com'). Browsers read "
                "domains right-to-left in terms of trust &mdash; what matters is "
                "the part right before the first single slash, not whatever "
                "appears first.",
            ),
        ),
        "text/html",
    ),
}

# Fill in the long tail of dictionary-word pages with a touch of personality.
for _slug in ("starwars", "qwerty", "letmein", "tester", "index"):
    FILES[f"/{_slug}.html"] = (
        page(_slug, f"{_slug}.html", junk_body(_slug)),
        "text/html",
    )


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(f"{self.client_address[0]} requested {self.path}")

        # Look up the exact path first (this also covers "/" and any path
        # that already ends in .html, like an old bookmark). If that
        # misses, try appending .html -- this lets visitors type clean
        # paths like /login or /.env without the .html suffix, while still
        # keeping the original *.html keys in FILES untouched.
        entry = FILES.get(self.path)
        if entry is None and not self.path.endswith(".html"):
            entry = FILES.get(self.path + ".html")

        if entry is not None:
            content, content_type = entry if isinstance(entry, tuple) else (entry, "text/html")
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")


def main():
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Listening on http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.server_close()


if __name__ == "__main__":
    main()