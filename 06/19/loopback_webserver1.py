#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import textwrap

HOST = "127.0.0.1"
PORT = 8080

PAGE_TEMPLATE = """<html>
<head><title>{title}</title></head>
<body style="
    font-family: 'Courier New', monospace;
    font-size:22px;
    line-height:1.65;
    background-color:#02040a;
    background-image:
        radial-gradient(white 1px, transparent 1px),
        radial-gradient(white 1px, transparent 1px),
        radial-gradient(#9fd6ff 1px, transparent 1px),
        linear-gradient(180deg, #050a18 0%, #02040a 60%, #000000 100%);
    background-size: 140px 140px, 220px 220px, 300px 300px, cover;
    background-position: 0 0, 60px 90px, 150px 40px, 0 0;
    background-attachment: fixed;
    color:#cdeaff;
    padding:6em 1.5em;
    margin:0;
    min-height:100vh;
">
<div style="
    max-width:{max_width}px;
    margin:0 auto;
    background:rgba(6,14,30,0.82);
    border:1px solid #1f4068;
    border-radius:16px;
    box-shadow:0 0 40px rgba(60,160,255,0.18), inset 0 0 64px rgba(0,40,90,0.25);
    padding:2.8em 3.2em;
    text-align: center;
">
<p style="
    color:#5fdfff;
    font-size:1.05em;
    letter-spacing:0.18em;
    text-transform:uppercase;
    margin:0 0 0.5em 0;
    border-bottom:1px dashed #1f4068;
    padding-bottom:0.8em;
">&#x1F6F0;&#xFE0F; United States Space Force &mdash; Loopback Tracking Station</p>
<h1 style="color:#7fd3ff; text-shadow:0 0 14px rgba(127,211,255,0.5); margin-top:0.9em; font-size:2.9em;">{heading}</h1>
{body}
<hr style="border:none; border-top:1px dashed #1f4068; margin-top:2.5em;">
<p style="color:#4d7fa8; font-size:0.95em;">SEMPER SUPRA &middot; Loopback Web Server &mdash; for training purposes only.</p>
</div>
</body>
</html>"""


def page(title, heading, body, max_width=1700):
    return PAGE_TEMPLATE.format(title=title, heading=heading, body=body, max_width=max_width)


def ascii_block(art):
    """Wrap ASCII art in a <pre> block so whitespace renders correctly.

    Uses textwrap.dedent to strip only the *common* leading whitespace
    across all lines (preserving each line's position relative to the
    others), so the art's internal shape stays intact. The block is
    then centered as a single rigid unit via a flex wrapper -- NOT via
    text-align:center on the <pre> itself, which would center each line
    independently and break vertical alignment between lines (e.g. a
    box's left/right walls drifting out of register with its top/bottom).
    """
    cleaned = textwrap.dedent(art).strip("\n")
    pre = (
        f'<pre style="color:#7fd3ff; background:#01070f; padding:1.6em; '
        f'border-radius:10px; border:1px solid #1f4068; overflow-x:auto; '
        f'font-size:1.3em; line-height:1.3; margin:0; display:inline-block; '
        f'text-align:left; '
        f'text-shadow:0 0 6px rgba(127,211,255,0.35);">'
        f'{cleaned}</pre>'
    )
    return f'<div style="display:flex; justify-content:center;">{pre}</div>'


ASCII_SEMPER_SUPRA = r"""
   _____  .__              .__                ________         .__   __             ________
  /     \ |__| ______ _____|__| ____   ____   \______ \   ____ |  |_/  |______     /  _____/
 /  \ /  \|  |/  ___//  ___/  |/  _ \ /    \   |    |  \_/ __ \|  |\   __\__  \   /   __  \ 
/    Y    \  |\___ \ \___ \|  (  <_> )   |  \  |    `   \  ___/|  |_|  |  / __ \_ \  |__\  \
\____|__  /__/____  >____  >__|\____/|___|  / /_______  /\___  >____/__| (____  /  \_____  /
        \/        \/     \/               \/          \/     \/               \/         \/ 
"""

ASCII_HOUSE = r"""
   .  *  .   .   *
    *   ___    .   *
        /-+-\
  .  --|  o  |--   .
        \---/        *
   *      ||
          ||      .
.  ___  __||__  ___   *
   [___]        [___]
"""

ASCII_LOCK = r"""
     ___________________
    |  ___    ACCESS    |
    | / o \   DENIED    |
    | \___/   [LOCKED]  |
    |___________________|
       |  |  |  |  |
       |__|__|__|__|
"""

ASCII_TIGER = r"""
   /\_/\
  ( o.o )
   > ^ <   RAWR
"""

ASCII_ROBOT = r"""
         ___
   _____/ o \____
  |              |
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
DISTINGUISHED
 ORBIT MEDAL"""


# A little flavor-text generator for the "junk drawer" of dictionary-word
# pages, so they're not all just a bare <h1> but nobody mistakes them for
# anything resembling a real secret.
JOKES = {
    "dragon": "Breathes fire. Hoards gold. Does not breathe fire on this server.",
    "qwerty": "The keyboard rolled over and this is what came out.",
    "letmein": "Knock knock. Who's there? Not a password, that's for sure.",
    "baseball": "Three strikes, you're out. This page strikes out too &mdash; nothing here.",
    "master": "Of none, apparently. This endpoint has no skills to speak of.",
    "football": "Wide left. So is the content on this page.",
    "shadow": "Lurks in corners. Found hiding in your URL bar instead.",
    "monkey": "&#x1F412; Ooh ooh ah ah. That's monkey for 'nothing to see here'.",
    "hunter": "Searching for loot. Found a 404-adjacent dead end.",
    "test": "1, 2, 3... is this thing on? Yes. It serves nothing.",
    "batman": "I am the night. I am also an empty HTTP response.",
    "trustno1": "Wise policy. Doubly wise here, since there's nothing to trust or distrust.",
    "tigger": "Bouncy, trouncy, flouncy, pouncy... empty.",
    "access": "Access granted! To absolutely nothing.",
    "soccer": "Goooooaaaal! Into the back of the net of empty pages.",
    "hockey": "Slapshot. Missed the net. Also missed having any content.",
    "killer": "App? Feature? Joke? This page is none of the above.",
    "superman": "Faster than a speeding bullet, slower than actual content arriving here.",
    "pepper": "A little spicy, mostly empty.",
    "golfer": "Fore! (That's a warning, not content.)",
    "summer": "Endless sunny days. Endlessly empty page.",
    "hammer": "MC says stop. This page already has.",
    "thunder": "Loud name, quiet page.",
    "cowboy": "Yeehaw. Rides off into a sunset of blank HTML.",
    "silver": "Worth less than gold, more than this page's content.",
    "orange": "Not the new black. Also not very full of data.",
    "merlin": "A wizard did this. Then forgot to add content.",
    "corvette": "Zero to sixty in 3 seconds. Zero content in 0 seconds.",
    "bigdog": "Woof. That's all it has to say.",
    "cheese": "Say cheese! &#x1F9C0; (There isn't any, though.)",
    "freedom": "Free! As in, free of content.",
    "sparky": "&#x26A1; A little jolt of nothing.",
    "yellow": "Mellow yellow. Hollow page.",
    "camaro": "Vroom vroom. Empty room.",
    "falcon": "&#x1F985; Soars high above any actual data.",
    "hello": "Hello there! Goodbye, any expectation of content.",
    "scooter": "Putters along at low speed, low substance.",
    "please": "Pretty please? Still nothing here.",
    "porsche": "Luxury German engineering. Bargain-bin HTML.",
    "guitar": "&#x1F3B8; Plays one note: silence.",
    "diamond": "Forged under pressure. This page wasn't even trying.",
    "computer": "Beep boop. Computer says: no data.",
    "wizard": "Pay no attention to the page behind the curtain.",
    "money": "Money can't buy you content for this page.",
    "phoenix": "Rises from the ashes. Of what, exactly? There was nothing here to burn.",
    "knight": "In shining armor. Defending an empty castle.",
    "iceman": "Cool under pressure. Cold, empty page.",
    "purple": "Rain optional. Content not included.",
    "player": "Player one has entered. Player one found nothing.",
    "sunshine": "&#x2600;&#xFE0F; Bright outside, blank in here.",
    "starwars": "A long time ago, in a server far, far away... still no content.",
    "coffee": "&#x2615; Brewed strong, served empty.",
    "bulldog": "Stubborn little guy. Stubbornly empty page.",
    "rabbit": "Down the hole you go. Wonderland's not here either.",
    "gandalf": "You shall not... find any content past this point.",
    "winter": "Is coming. Content is not.",
    "tennis": "Serve's up! Nothing's returned.",
    "ferrari": "Prancing horse. Galloping void.",
    "cookie": "&#x1F36A; This server does not track you with cookies. It just has no content.",
    "maverick": "Top of the leaderboard for 'pages with nothing on them'.",
    "diablo": "Stay a while and listen... to the sound of an empty response body.",
    "welcome": "Welcome! Make yourself at home. There isn't much furniture, though.",
    "fishing": "Gone fishing. Caught nothing but a 200 OK.",
    "captain": "My captain! This ship has no cargo.",
    "viking": "Pillaged far and wide. Found no content here either.",
    "snoopy": "&#x1F436; Even Snoopy's doghouse has more in it than this page.",
    "blue": "Feeling blue? This page certainly is &mdash; and empty.",
    "winner": "Winner winner, chicken dinner. No data, though.",
    "house": "Lights on, nobody home.",
    "firebird": "Mythical bird. Equally mythical content.",
    "butter": "Smooth and... that's about it.",
    "turtle": "Slow and steady. Steadily empty.",
    "steelers": "Here we go! Nowhere, that is.",
    "golf": "A good walk spoiled. A good page, also spoiled (it's empty).",
    "bear": "&#x1F43B; Grr. Translation: 'no content.'",
    "tiger": "Hear it roar. Hear the silence of an empty page.",
    "doctor": "The doctor is in. The content is out.",
    "gateway": "A gateway to... another empty page, unfortunately.",
    "angel": "Watching over you. Not watching over any content, since there is none.",
    "spider": "&#x1F577;&#xFE0F; Spins a web of nothingness.",
    "matrix": "There is no spoon. There is also no content.",
    "scooby": "Ruh-roh. Mystery solved: this page is empty.",
    "princess": "In another castle. This one's just an empty page.",
    "mercedes": "The best or nothing. This is the 'nothing' option.",
    "gunner": "Locked, loaded, and aimed at... an empty response.",
    "voyager": "Boldly going where no content has gone before.",
    "rangers": "Lead the way. Straight to an empty page.",
    "topgun": "I feel the need... the need for actual content. Doesn't get it though.",
    "green": "It's not easy being green, or having any data on this page.",
    "magic": "&#x2728; Now you see it, now it's still nothing.",
    "slayer": "Vanquished all the content on this page.",
    "video": "Killed the radio star. Also, there's no video here.",
    "monster": "Under the bed. Not under this empty page, though.",
    "rocket": "&#x1F680; 3, 2, 1... still no content.",
    "beach": "&#x1F3D6;&#xFE0F; Sun, sand, and absolutely nothing else.",
    "testing": "Testing, testing, 1, 2, 3. Still just testing.",
    "eagle1": "The eagle has landed. On an empty page.",
    "raiders": "Of the Lost Content (spoiler: still lost).",
    "forever": "This page will be empty forever and ever.",
    "buddy": "Hey buddy. Got any content? No? Same.",
    "whatever": "Whatever. This page certainly doesn't care either.",
    "helpme": "Help is not on the way. Neither is content.",
    "midnight": "The witching hour. Nothing happens here either.",
    "startrek": "To boldly go where no content has gone before.",
    "happy": "&#x1F600; Happy to have visited. Sad about the empty page.",
    "giants": "Standing on the shoulders of... an empty response body.",
    "golden": "All that glitters is not content.",
    "fire": "&#x1F525; Lit. (The page is not, in fact, lit with content.)",
    "packers": "Cheese optional. Content not included.",
    "einstein": "E=mc&sup2;. Still couldn't calculate any content for this page.",
    "warrior": "Fights bravely. Loses to the boss named 'Empty Page'.",
    "power": "Unlimited power! Limited to zero content, though.",
    "toyota": "Oh what a feeling! Of finding nothing here.",
    "rock": "&#x1F3B8; Solid as a rock. Also as empty as one.",
    "wolf": "&#x1F43A; Howls at the moon. Howls about the lack of content.",
    "iloveyou": "&#x2764;&#xFE0F; Aw, shucks. This page loves you back, but has nothing to give.",
    "legend": "Legend has it this page used to have content. (It didn't.)",
    "success": "Mission accomplished: you found another empty page.",
    "jaguar": "&#x1F406; Fast and sleek. Equally fast to load, since it's empty.",
    "cool": "As a cucumber. As empty as one too.",
    "mountain": "&#x26F0;&#xFE0F; Climbed it. Found no content at the summit.",
    "phantom": "Of the opera. Haunting this very empty page.",
    "tester": "Professional tester of empty pages, apparently.",
    "index": "You were looking for the index. This is just *an* index, of nothing.",
}


def junk_body(slug):
    joke = JOKES.get(slug, "Nothing much going on here.")
    return f"<p>{joke}</p>"


# Fake files served by the web server

FILES = {
    "/": (
        page(
            "Loopback Tracking Station",
            "&#x1F6F0;&#xFE0F; Loopback Tracking Station Online",
            ascii_block(ASCII_SEMPER_SUPRA)
            + "<p>This is a simulated ground station, for training purposes only.</p>"
            "<p>All systems nominal. No live satellites are actually being "
            "tracked here &mdash; but feel free to explore the comms array "
            "and see what other channels are broadcasting.</p>"
            "<p>Proudly flying the colors for Freedom 250, marking 250 years "
            "of American independence.</p>",
        ),
        "text/html",
    ),

    "/tigers.html": (
        page(
            "Callsign Roster",
            "&#x1F405; Squadron Callsign Roster: TIGER Flight",
            ascii_block(ASCII_TIGER)
            + "<ul>"
            "<li>TIGER-1 \"Bengal\" &mdash; flight lead, the classic, the icon.</li>"
            "<li>TIGER-2 \"Siberian\" &mdash; biggest wingspan in the squadron.</li>"
            "<li>TIGER-3 \"Sumatran\" &mdash; smallest airframe, still terrifying on intercept.</li>"
            "<li>TIGER-4 \"Malayan\" &mdash; the rare one you brag about flying with.</li>"
            "</ul>",
        ),
        "text/html",
    ),

    "/robots.html": (
        page(
            "Directive: Autonomous Units",
            "&#x1F916; Directive for Autonomous Probe Units",
            ascii_block(ASCII_ROBOT)
            + "<p>User-agent: *<br>Disallow: /admin</p>"
            "<p>Yes, we know putting it in robots.txt just tells every "
            "probe unit (and every curious human) exactly where the "
            "restricted bay is. That's sort of the joke.</p>",
        ),
        "text/html",
    ),

    "/admin.html": (
        page(
            "Restricted Bay",
            "&#x1F512; Restricted Launch Bay",
            ascii_block(ASCII_LOCK)
            + "<p>Restricted Area &mdash; Authorized Guardians Only</p>"
            "<p>(There's no actual login here. It's just a blast door "
            "sign on an empty bay, like the 'employees only' door at a "
            "diner that just leads to a mop closet.)</p>",
        ),
        "text/html",
    ),

    "/secret.html": (
        page(
            "Classified Commendation",
            "&#x1F389; Guardian Commendation Located",
            ascii_block(ASCII_TROPHY)
            + "<p>You found the hidden transmission.</p>"
            "<p>Here's your flag &mdash; redeem it for a prize "
            "(however your particular redemption system works):</p>"
            + ascii_block("FLAG{loopback_secret_page_found}")
            + "<p style=\"color:#4d7fa8; font-size:0.85em;\">"
            "Congratulations! You've found the secret page."
            "</p>",
        ),
        "text/html",
    ),
}

# Fill in the long tail of dictionary-word pages with a touch of personality.
for _slug in [
    "dragon", "qwerty", "letmein", "baseball", "master", "football", "shadow",
    "monkey", "hunter", "test", "batman", "trustno1", "tigger", "access",
    "soccer", "hockey", "killer", "superman", "pepper", "golfer", "summer",
    "hammer", "thunder", "cowboy", "silver", "orange", "merlin", "corvette",
    "bigdog", "cheese", "freedom", "sparky", "yellow", "camaro", "falcon",
    "hello", "scooter", "please", "porsche", "guitar", "diamond", "computer",
    "wizard", "money", "phoenix", "knight", "iceman", "purple", "player",
    "sunshine", "starwars", "coffee", "bulldog", "rabbit", "gandalf",
    "winter", "tennis", "ferrari", "cookie", "maverick", "diablo", "welcome",
    "fishing", "captain", "viking", "snoopy", "blue", "winner", "house",
    "firebird", "butter", "turtle", "steelers", "golf", "bear", "tiger",
    "doctor", "gateway", "angel", "spider", "matrix", "scooby", "princess",
    "mercedes", "gunner", "voyager", "rangers", "topgun", "green", "magic",
    "slayer", "video", "monster", "rocket", "beach", "testing", "eagle1",
    "raiders", "forever", "buddy", "whatever", "helpme", "midnight",
    "startrek", "happy", "giants", "golden", "fire", "packers", "einstein",
    "warrior", "power", "toyota", "rock", "wolf", "iloveyou", "legend",
    "success", "jaguar", "cool", "mountain", "phantom", "tester", "index",
]:
    FILES[f"/{_slug}.html"] = (
        page(_slug, f"{_slug}.html", junk_body(_slug)),
        "text/html",
    )


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        print(f"{self.client_address[0]} requested {self.path}")

        if self.path in FILES:
            entry = FILES[self.path]

            if isinstance(entry, tuple):
                content, content_type = entry
            else:
                content = entry
                content_type = "text/html"

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