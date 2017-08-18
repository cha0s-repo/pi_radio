#!/usr/bin/env python
# -*- coding: utf-8 -*-

import SimpleHTTPServer
import SocketServer
import re
import subprocess as sp

def htc(m):
    return chr(int(m.group(1),16))

def urldecode(url):
    rex=re.compile('%([0-9a-hA-H][0-9a-hA-H])',re.M)
    return rex.sub(htc,url)

class SETHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def createHTML(self):
	pl = sp.check_output(["mpc", "playlist"]).split('\n')
	cu = sp.check_output(["mpc", "current"])
        html = file("/home/pi/mine/index.html", "r")
        for line in html:
            self.wfile.write(line)
	self.wfile.write("play list:<br>")
	for cont in pl:
		self.wfile.write(cont)
		self.wfile.write('<br>')
	self.wfile.write("current playing:<br>")
	self.wfile.write(cu)
	self.wfile.write("</body>")
	self.wfile.write("</html>")

            
    def do_GET(self):
	if "reloadlist" in self.path:
		sp.call(["mpc", "stop"])
		sp.call(["mpc", "clear"])
		sp.call(["mpc", "load", "all"])
		sp.call(["mpc", "play", "-q"])
	if "playnext" in self.path:
		sp.call(["mpc", "next"])
	if "playprev" in self.path:
		sp.call(["mpc", "prev", "-q"])

        self.createHTML()
        
    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        qs = self.rfile.read(length)
        url=urldecode(qs)
        plist = url.split('=')
	if plist[1] and plist[0] == 'newlist':
		with open('/home/pi/.mpd/playlists/all.m3u', 'a') as fd:
			fd.write(plist[1]+'\n')
        self.createHTML()
        
if __name__=='__main__':
	Handler = SETHandler
	PORT = 80
	httpd = SocketServer.TCPServer(("", PORT), Handler)
	httpd.serve_forever()

