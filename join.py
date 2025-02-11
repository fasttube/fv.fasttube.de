#!/usr/bin/env python

import os, csv, datetime

import http.server as server
from urllib.parse import parse_qs

CSVFILE = "applicants.csv"

COLS = [
    "einsendung",
    "start",
    "vornamen",
    "nachnamen",
    "adresse1",
    "adresse2",
    "email",
    "satzung",
    "datenschutz",
    "lastschrift",
    "bank",
    "bic",
    "iban",
    "inhaber"
]

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):

    def do_POST(self):

        content_len = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_len)
        data = parse_qs(body.decode('utf-8'))

        print(data)

        # create csv if not exists
        if not os.path.exists(CSVFILE):
            print("Creating", CSVFILE, "...")
            with open(CSVFILE, 'w+') as f:
                writer = csv.writer(f)
                writer.writerow(COLS)

        now_iso = datetime.datetime.now().isoformat()

        with open(CSVFILE, 'a+') as f:
            writer = csv.writer(f)
            writer.writerow([data.get(c, [now_iso])[0] for c in COLS])

        self.send_response(201, 'Created')
        self.end_headers()
        self.wfile.write("""<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
                    <meta http-equiv="refresh" content="5;url=https://fv.fasttube.de/" />
                    <title>FTFV: Beitrittsantrag eingereicht</title>
                </head>
                <body>
                    <h1>Beitrittsantrag eingereicht</h1>
                    <p>Antrag gespeichert.</p>
                    <p>Danke! Toll, dass Du dabei bist. Wir melden uns möglichst bald.</p>
                    <p>&nbsp;&nbsp;&nbsp;~ Dein Fördervereinsvorstand</p>
                    <p>Du wirst in 5 Sekunden auf die Hauptseite weitergeleitet...</p>
                </body>
            </html>""".encode('utf-8'))


if __name__ == '__main__':
    server = server.ThreadingHTTPServer(("127.0.0.1", 3131), HTTPRequestHandler)
    print("listening on 127.0.0.1:3131")
    server.serve_forever()
