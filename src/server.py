#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse;
import re
import json

from Physics import *;

class billiardsHandler( BaseHTTPRequestHandler ):

    def do_GET(self):

        parsed = urlparse(self.path);

        if (parsed.path in ['/']):
            fp = open('./index.html')
            content = fp.read()
            fp.close()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))

        elif (parsed.path in ['/script.js']):

            fp = open('.'+self.path)
            content = fp.read()
            fp.close()
            
            # generate the header
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.send_header("Content-length", len(content))
            self.end_headers()
            
            self.wfile.write(bytes(content, "utf-8"))

        elif (parsed.path in ['/Physics.py']):
            fp = open('.'+self.path)
            content = fp.read()
            fp.close

            self.send_response(200)
            self.send_header("Content-type", "text/python")
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))

        elif (parsed.path in ['/https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js']):

            fp = open('.'+self.path)
            content = fp.read()
            fp.close()
            
            # generate the header
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            self.send_header("Content-length", len(content))
            self.end_headers()
            
            self.wfile.write(bytes(content, "utf-8"))     
            
        else:
            # generate 404 response
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

    def do_POST(self):

        parsed = urlparse(self.path)

        if parsed.path in ['/new_game']:
            data_length = int(self.headers['Content-Length'])
            raw_data = self.rfile.read(data_length)
            try:
                data = json.loads(raw_data.decode('utf-8'))
                db = Database(True)
                db.createDB()

                game = Game(None, data['game_name'], data['player1'], data['player2'])
                table = Table()

                table.init_table()
                table_id = db.writeTable(table)
                db.close()
                game_id = game.gameID
                svg = table.svg()
                res_dict = {
                    "table_id": table_id,
                    "game_id": game_id,
                    "svg": svg
                }
                results = json.dumps(res_dict)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-length", len(results))
                self.end_headers()

                self.wfile.write(bytes(results, "utf-8"))

            except json.JSONDecodeError:
                self.send_response(404)
                self.end_headers()

        elif parsed.path in ['/make_shot']:
            data_length = int(self.headers['Content-Length'])
            raw_data = self.rfile.read(data_length)
            try:
                data = json.loads(raw_data.decode('utf-8'))
                db = Database()
                table = db.readTable(data['table_id'])
                game = Game(data['game_id'], None, None, None)
                shotID = game.shoot(game.gameName, data['player'], table, float(data['x']), float(data['y']))
                shot_time = db.get_shot_time(shotID)
                db.close()
                res = {
                    "shot_id": shotID,
                    "shot_time": shot_time
                }

                results = json.dumps(res)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-length", len(results))
                self.end_headers()

                self.wfile.write(bytes(results, "utf-8"))

            except json.JSONDecodeError:
                self.send_response(404)
                self.end_headers()

        elif parsed.path in ['/run_animation']:
            data_length = int(self.headers['Content-Length'])
            raw_data = self.rfile.read(data_length)
            try:
                data = json.loads(raw_data.decode('utf-8'))
                shot_id = data['shot_id']
                current_time = data['current_time']
                db = Database()
                read_out = db.readTable_time(shot_id, current_time)
                db.close()
                if read_out == None:
                    self.send_response(400)
                    self.end_headers()
                    return
                (table, table_id) = read_out
                svg = table.svg()
                res = {
                    "table_id": table_id,
                    "svg": svg
                }

                results = json.dumps(res)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-length", len(results))
                self.end_headers()

                self.wfile.write(bytes(results, "utf-8"))

            except json.JSONDecodeError:
                self.send_response(404)
                self.end_headers()

        elif parsed.path in ['/new_cue']:
            data_length = int(self.headers['Content-Length'])
            raw_data = self.rfile.read(data_length)
            try:
                data = json.loads(raw_data.decode('utf-8'))
                table_id = data['table']
                db = Database()
                table = db.readTable(table_id)
                if table == None:
                    self.send_response(400)
                    self.end_headers()
                    return
                table.newCueBall()
                svg = table.svg()
                new_id = db.writeTable(table)
                db.close()
                res = {
                    "table_id": new_id,
                    "svg": svg
                }

                results = json.dumps(res)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-length", len(results))
                self.end_headers()

                self.wfile.write(bytes(results, "utf-8"))

            except json.JSONDecodeError:
                self.send_response(404)
                self.end_headers()
        
        else:
            # generate 404 response
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"))

if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 12345), billiardsHandler)
    try:
        httpd.serve_forever()
    except RuntimeError:
        httpd.shutdown()
