#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 8080

# Fake files served by the web server

FILES = {
    "/": (
        "<html><body>"
        "<h1>Welcome to the Loopback Web Server! This is for training purposes only.</h1>"
        "<p>Nothing interesting here...</p>"
        "</body></html>",
        "text/html"
    ),

    "/passwords.html": (
        "admin:Spring2026!\n"
        "guest:password123\n"
        "test:qwerty\n",
        "text/plain"
    ),

    "/tigers.html": (
        "Bengal Tiger\n"
        "Siberian Tiger\n"
        "Sumatran Tiger\n"
        "Malayan Tiger\n",
        "text/plain"
    ),

    "/robots.html": (
        "<h1>Welcome to the Loopback Web Server! This is for training purposes only.</h1>"
        "User-agent: *\n"
        "Disallow: /admin\n",
        "text/plain"
    ),

    "/admin.html": (
        "<html><body>"
        "<h1>Welcome to the Loopback Web Server! This is for training purposes only.</h1>"
        "<h2>Admin Portal</h2>"
        "<p>Restricted Area</p>"
        "</body></html>",
        "text/html"
    ),

    "/secret.html": (
        "<html><body>"
        "<h1>Congratulations!</h1>"
        "<p>You found the hidden page.</p>"
        "</body></html>",
        "text/html"
    ),

    "/dragon.html": "<h1>dragon.html</h1>",
    "/qwerty.html": "<h1>qwerty.html</h1>",
    "/letmein.html": "<h1>letmein.html</h1>",
    "/baseball.html": "<h1>baseball.html</h1>",
    "/master.html": "<h1>master.html</h1>",
    "/football.html": "<h1>football.html</h1>",
    "/shadow.html": "<h1>shadow.html</h1>",
    "/monkey.html": "<h1>monkey.html</h1>",
    "/hunter.html": "<h1>hunter.html</h1>",
    "/test.html": "<h1>test.html</h1>",
    "/batman.html": "<h1>batman.html</h1>",
    "/trustno1.html": "<h1>trustno1.html</h1>",
    "/tigger.html": "<h1>tigger.html</h1>",
    "/access.html": "<h1>access.html</h1>",
    "/soccer.html": "<h1>soccer.html</h1>",
    "/hockey.html": "<h1>hockey.html</h1>",
    "/killer.html": "<h1>killer.html</h1>",
    "/superman.html": "<h1>superman.html</h1>",
    "/pepper.html": "<h1>pepper.html</h1>",
    "/golfer.html": "<h1>golfer.html</h1>",
    "/summer.html": "<h1>summer.html</h1>",
    "/hammer.html": "<h1>hammer.html</h1>",
    "/thunder.html": "<h1>thunder.html</h1>",
    "/cowboy.html": "<h1>cowboy.html</h1>",
    "/silver.html": "<h1>silver.html</h1>",
    "/orange.html": "<h1>orange.html</h1>",
    "/merlin.html": "<h1>merlin.html</h1>",
    "/corvette.html": "<h1>corvette.html</h1>",
    "/bigdog.html": "<h1>bigdog.html</h1>",
    "/cheese.html": "<h1>cheese.html</h1>",
    "/freedom.html": "<h1>freedom.html</h1>",
    "/sparky.html": "<h1>sparky.html</h1>",
    "/yellow.html": "<h1>yellow.html</h1>",
    "/camaro.html": "<h1>camaro.html</h1>",
    "/falcon.html": "<h1>falcon.html</h1>",
    "/hello.html": "<h1>hello.html</h1>",
    "/scooter.html": "<h1>scooter.html</h1>",
    "/please.html": "<h1>please.html</h1>",
    "/porsche.html": "<h1>porsche.html</h1>",
    "/guitar.html": "<h1>guitar.html</h1>",
    "/diamond.html": "<h1>diamond.html</h1>",
    "/computer.html": "<h1>computer.html</h1>",
    "/wizard.html": "<h1>wizard.html</h1>",
    "/money.html": "<h1>money.html</h1>",
    "/phoenix.html": "<h1>phoenix.html</h1>",
    "/knight.html": "<h1>knight.html</h1>",
    "/iceman.html": "<h1>iceman.html</h1>",
    "/purple.html": "<h1>purple.html</h1>",
    "/player.html": "<h1>player.html</h1>",
    "/sunshine.html": "<h1>sunshine.html</h1>",
    "/starwars.html": "<h1>starwars.html</h1>",
    "/coffee.html": "<h1>coffee.html</h1>",
    "/bulldog.html": "<h1>bulldog.html</h1>",
    "/rabbit.html": "<h1>rabbit.html</h1>",
    "/gandalf.html": "<h1>gandalf.html</h1>",
    "/winter.html": "<h1>winter.html</h1>",
    "/tennis.html": "<h1>tennis.html</h1>",
    "/ferrari.html": "<h1>ferrari.html</h1>",
    "/cookie.html": "<h1>cookie.html</h1>",
    "/maverick.html": "<h1>maverick.html</h1>",
    "/diablo.html": "<h1>diablo.html</h1>",
    "/welcome.html": "<h1>welcome.html</h1>",
    "/fishing.html": "<h1>fishing.html</h1>",
    "/captain.html": "<h1>captain.html</h1>",
    "/viking.html": "<h1>viking.html</h1>",
    "/snoopy.html": "<h1>snoopy.html</h1>",
    "/blue.html": "<h1>blue.html</h1>",
    "/winner.html": "<h1>winner.html</h1>",
    "/house.html": "<h1>house.html</h1>",
    "/firebird.html": "<h1>firebird.html</h1>",
    "/butter.html": "<h1>butter.html</h1>",
    "/turtle.html": "<h1>turtle.html</h1>",
    "/steelers.html": "<h1>steelers.html</h1>",
    "/golf.html": "<h1>golf.html</h1>",
    "/bear.html": "<h1>bear.html</h1>",
    "/tiger.html": "<h1>tiger.html</h1>",
    "/doctor.html": "<h1>doctor.html</h1>",
    "/gateway.html": "<h1>gateway.html</h1>",
    "/angel.html": "<h1>angel.html</h1>",
    "/spider.html": "<h1>spider.html</h1>",
    "/matrix.html": "<h1>matrix.html</h1>",
    "/scooby.html": "<h1>scooby.html</h1>",
    "/princess.html": "<h1>princess.html</h1>",
    "/mercedes.html": "<h1>mercedes.html</h1>",
    "/gunner.html": "<h1>gunner.html</h1>",
    "/voyager.html": "<h1>voyager.html</h1>",
    "/rangers.html": "<h1>rangers.html</h1>",
    "/topgun.html": "<h1>topgun.html</h1>",
    "/green.html": "<h1>green.html</h1>",
    "/magic.html": "<h1>magic.html</h1>",
    "/slayer.html": "<h1>slayer.html</h1>",
    "/video.html": "<h1>video.html</h1>",
    "/monster.html": "<h1>monster.html</h1>",
    "/rocket.html": "<h1>rocket.html</h1>",
    "/beach.html": "<h1>beach.html</h1>",
    "/testing.html": "<h1>testing.html</h1>",
    "/eagle1.html": "<h1>eagle1.html</h1>",
    "/raiders.html": "<h1>raiders.html</h1>",
    "/forever.html": "<h1>forever.html</h1>",
    "/buddy.html": "<h1>buddy.html</h1>",
    "/whatever.html": "<h1>whatever.html</h1>",
    "/helpme.html": "<h1>helpme.html</h1>",
    "/midnight.html": "<h1>midnight.html</h1>",
    "/startrek.html": "<h1>startrek.html</h1>",
    "/happy.html": "<h1>happy.html</h1>",
    "/giants.html": "<h1>giants.html</h1>",
    "/golden.html": "<h1>golden.html</h1>",
    "/fire.html": "<h1>fire.html</h1>",
    "/packers.html": "<h1>packers.html</h1>",
    "/einstein.html": "<h1>einstein.html</h1>",
    "/warrior.html": "<h1>warrior.html</h1>",
    "/power.html": "<h1>power.html</h1>",
    "/toyota.html": "<h1>toyota.html</h1>",
    "/rock.html": "<h1>rock.html</h1>",
    "/wolf.html": "<h1>wolf.html</h1>",
    "/iloveyou.html": "<h1>iloveyou.html</h1>",
    "/legend.html": "<h1>legend.html</h1>",
    "/success.html": "<h1>success.html</h1>",
    "/jaguar.html": "<h1>jaguar.html</h1>",
    "/cool.html": "<h1>cool.html</h1>",
    "/mountain.html": "<h1>mountain.html</h1>",
    "/phantom.html": "<h1>phantom.html</h1>",
    "/tester.html": "<h1>tester.html</h1>",
    "/index.html": "<h1>index.html</h1>",
}


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