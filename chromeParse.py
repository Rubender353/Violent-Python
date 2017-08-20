#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import optparse
import os
import sqlite3


def printDownloads(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    c.execute("SELECT target_path, referrer, datetime((start_time/1000000)-11644473600, \
             'unixepoch', 'localtime'), datetime((end_time/1000000)-11644473600, \
             'unixepoch', 'localtime') FROM downloads;")
    print '\n[*] --- Files Downloaded --- '
    for row in c:
        print '[+] File: ' + str(row[0]) + ' from source: ' \
            + str(row[1]) + ' Start: ' + str(row[2]) + ' End: ' + str(row[3])


def printCookies(cookiesDB):
    try:
        conn = sqlite3.connect(cookiesDB)
        c = conn.cursor()
        c.execute('SELECT host_key, name, value FROM cookies;')

        print '\n[*] -- Found Cookies --'
        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            print '[+] Host: ' + host + ', Cookie: ' + name \
                + ', Value: ' + value
    except Exception, e:
        if 'encrypted' in str(e):
            print '\n[*] Error reading your cookies database.'
            print '[*] Upgrade your Python-Sqlite3 Library'


def printHistory(placesDB):
    try:
        conn = sqlite3.connect(placesDB)
        c = conn.cursor()
        c.execute("select url, datetime((last_visit_time/1000000)-11644473600, \
                  'unixepoch', 'localtime') from urls;")
        
        print '\n[*] -- Found History --'
        for row in c:
            url = str(row[0])
            date = str(row[1])
            print '[+] ' + date + ' - Visited: ' + url
    except Exception, e:
        if 'encrypted' in str(e):
            print '\n[*] Error reading your places database.'
            print '[*] Upgrade your Python-Sqlite3 Library'
            exit(0)


def printGoogle(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()    
    c.execute("select url, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') \
        from urls,keyword_search_terms where visit_count > 0 \
        and keyword_search_terms.url_id==urls.id;")

    print '\n[*] -- Found Google --'
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'google' in url.lower():
            r = re.findall(r'q=.*\&', url)
            if r:
                search=r[0].split('&')[0]
                search=search.replace('q=', '').replace('+', ' ')
                print '[+] '+date+' - Searched For: ' + search


def main():
    parser = optparse.OptionParser("usage %prog "+\
      "-p <firefox profile path> "
                              )
    parser.add_option('-p', dest='pathName', type='string',\
      help='specify chrome profile path')

    (options, args) = parser.parse_args()
    pathName = options.pathName
    if pathName == None:
        print parser.usage
        exit(0)
    elif os.path.isdir(pathName) == False:
        print '[!] Path Does Not Exist: ' + pathName
        exit(0)
    else:

        cookiesDB = os.path.join(pathName, 'Cookies')
        if os.path.isfile(cookiesDB):
            pass
            printCookies(cookiesDB)
        else:
            print '[!] Cookies Db does not exist:' + cookiesDB

        placesDB = os.path.join(pathName, 'History')
        if os.path.isfile(placesDB):
            printHistory(placesDB)
            printGoogle(placesDB)
            printDownloads(placesDB)
        else:
            print '[!] History Db does not exist: ' + placesDB


if __name__ == '__main__':
    main()

