from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from time import time

class BJ_API(BaseHTTPRequestHandler):
    payloads = []
    Run = True
    TotalCount = 0
    TotalCards = []
    PastCount = []
    CurrentGameCount = 0
    CardsOnTable = []
    LastCall = time()
    def __init__(self, request, client_address, server):
        return super().__init__(request, client_address, server)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'https://babylonstk.evo-games.com')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        payload = json.loads(post_data)["payloadData"]

        if type(payload) is not dict or not ("name" in payload.keys() or "dealer" in payload.keys()):
            self._set_response()
            return
        
        if (time() - BJ_API.LastCall >= 50):
            print("New Deck")
            print(time() - BJ_API.LastCall)

        if "name" in payload.keys():
            print("PHASE : " + payload["name"] + "-----------------")
            if payload["name"] == "BetweenGames":
                BJ_API.TotalCards += BJ_API.CardsOnTable
                BJ_API.TotalCount = self.countCards(BJ_API.TotalCards)
                BJ_API.PastCount.append(self.countCards(BJ_API.CardsOnTable))
                BJ_API.CardsOnTable = []
        elif "dealer" in payload.keys():
            print("GAME------------------")                
            BJ_API.CardsOnTable = []
            print("Dealer: ", end="")
            for card in payload["dealer"]["cards"]:
                if card["value"] != "**":
                    BJ_API.CardsOnTable.append(card["value"])
                    print(card["value"], end=" ")
            print("")
            for player in payload["seats"].items():
                print("P: ", end="")
                for card in player[1]["first"]["cards"]:
                    BJ_API.CardsOnTable.append(card["value"])
                    print(card["value"], end=" ")
                print("")
        else:
            assert("Error not handled payload.")

        print("Card Count: " + str(self.countCards(BJ_API.CardsOnTable)))
        print("Total Count: " + str(BJ_API.TotalCount + self.countCards(BJ_API.CardsOnTable)))
        print("Past Count:" + str(BJ_API.PastCount))
        print("LastCall: " + str(time() - BJ_API.LastCall))
        BJ_API.LastCall = time()
        BJ_API.payloads.append(payload)
        print("")
        self._set_response()

    def log_message(self, format, *args):
        return

    def countCards(self, cards):
        count = 0
        for card in cards:
            if card[0] in "AKQJT":
                count -= 1
            elif card[0] in "23456":
                count += 1
        return count


def run():
    server_address = ('', 2121)
    httpd = HTTPServer(server_address, BJ_API)
    while (BJ_API.Run):
        httpd.handle_request()

if __name__ == '__main__':
    run()

# BetweenGames
# BetsOpen
# BetsClosed
# InitialDealing
# PlayerDealing
# DealerDealing
# GameResult
