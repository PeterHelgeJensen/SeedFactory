import ephem
import math
import urllib3


url = 'http://celestrak.com/NORAD/elements/other-comm.txt'
#resp = urllib3.urlopen('https://www.celestrak.com/NORAD/elements/cubesat.txt')
http = urllib3.PoolManager()

resp = http.request('GET', url)
content = resp.data

tles = content.splitlines()

satlist = {}
for i in range(0,len(tles),3):
    sat = ephem.readtle(tles[i].decode(), tles[i+1].decode(), tles[i+2].decode())
    satlist[sat.name] = sat

t = ephem.now()

s1 = satlist["DIAMOND RED"]
s1.compute(t)
s2 = satlist["DIAMOND GREEN"]
s2.compute(t)
s3 = satlist["DIAMOND BLUE"]
s3.compute(t)
#s4 = satlist["GOMX-4A"]
#s4.compute(t)
#s5 = satlist["GOMX-4B"]
#s5.compute(t)


print ("Distance RED<->GREEN")
print ("Arc:   {:.1f}km".format(ephem.separation(s1, s2) * (s2.elevation + ephem.earth_radius) / 1000))
print ("Chord: {:.1f}km".format(math.sin(ephem.separation(s1, s2)/2)*2*(s2.elevation + ephem.earth_radius) / 1000))
print ("")
print ("Distance GREEN<->BLUE")
print ("Arc:   {:.1f}km".format(ephem.separation(s2, s3) * (s2.elevation + ephem.earth_radius) / 1000))
print ("Chord: {:.1f}km".format(math.sin(ephem.separation(s2, s3)/2)*2*(s2.elevation + ephem.earth_radius) / 1000))
print ("")
print ("Distance RED<->BLUE")
print ("Arc:   {:.1f}km".format(ephem.separation(s1, s3) * (s1.elevation + ephem.earth_radius) / 1000))
print ("Chord: {:.1f}km".format(math.sin(ephem.separation(s1, s3)/2)*2*(s1.elevation + ephem.earth_radius) / 1000))

antenna = ephem.Observer()
antenna.lat = '56.769043'
antenna.lon = '9.856832'
antenna.elevation = 72

next_pass = antenna.next_pass(s1)
print ("")
print ("time:    ", next_pass[0])
print ("azimuth: ", next_pass[1])
print (next_pass[2])
print (next_pass[3])
print (next_pass[4])
print (next_pass[5])
