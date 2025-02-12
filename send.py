#!/opt/homebrew/bin/python3
import base64, requests, sys
import random
import json
#print ('argument list', sys.argv)

try:
    with open("variables.txt", mode="r", encoding="utf-8") as read_file:
      vars_file = json.load(read_file)
     
    print(vars_file["RUNS"])
 
except:
    print("Something unexpected occurred!")


try:
    authorization = base64.b64encode(bytes(vars_file["myclient"] + ":" + vars_file["client_secret"], "ISO-8859-1")).decode("ascii")
    headers = {
        "Authorization": f"Basic {authorization}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {
        "grant_type": "client_credentials"
    }
    response = requests.post("https://auth.pingone.com/{}/as/token".format(vars_file["ENVID"]),data=body, headers=headers)
    mytoken_dict = json.load(response.text)
    TOKEN = mytoken_dict["access_token"]
except:
    print("No token present")
# 
#myclient=`grep myclient variables | awk -F\" '{print $2}'`
#client_secret=`grep client_secret variables | awk -F\" '{print $2}'`
#RISKPOLICYID=`grep RISKPOLICYID variables | awk -F\" '{print $2}'`
#ENVID=`grep ENVID variables | awk -F\" '{print $2}'`
#RUNS=`grep RUNS variables | awk -F\= '{print $2}'`
#BADACTORS=`grep BADACTORS variables | awk -F\" '{print $2}'`
#DEBUG=`grep DEBUG variables | awk -F\" '{print $2}'`

#TOKEN=`./gettoken.py $myclient $client_secret $ENVID | grep access_token | awk -F\" '{print $4}'`

# Set MAXTIMES to how many instances to load - suggestion is not over 100 at once
#numbertoload=`jot -r 1 1 $RUNS`

i=0
#Count how many lines in source files
with open(r"ips", 'r') as fp:
    IPCOUNT = sum(1 for line in fp)
with open(r"names", 'r') as fp:
    NAMECOUNT = sum(1 for line in fp)
with open(r"Agents", 'r') as fp:
    AGENTCOUNT = sum(1 for line in fp)
with open(r"Platforms", 'r') as fp:
    PLATFORMCOUNT = sum(1 for line in fp)
with open(r"MailDomains", 'r') as fp:
    MAILCOUNT = sum(1 for line in fp)
with open(r"AppsUsed", 'r') as fp:
    APPSCOUNT = sum(1 for line in fp)
with open(r"badips", 'r') as fp:
    BADIPCOUNT = sum(1 for line in fp)

#if [[ $DEBUG == "YES" ]] ;
# then
#  export CURLCMD="curl --location"
# else 
#  export CURLCMD="curl -s -o --location"
#fi

# FUNCTION TO SEND REQUESTS
def THROWTHEPIE () :
#Assign the userinformation from the files here
#using gawk number of lines NR we select the exact line of the source file to be returned in the assigned variable

  print("Name is $NAME and source app is $APP domain is $MAILDOMAIN")
  print("Emails is $MAIL and Client browser: $AGENT and their ip is $IP")
  print( "--")
   $CURLCMD --location 'https://api.pingone.com/v1/environments/'"$ENVID"'/riskEvaluations' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer '"$TOKEN"'' \
  --data-raw '{
  	"event": {
  		"completionStatus": "IN_PROGRESS",
  		"targetResource": {
  			"id": "15fa85c0742a8be144a703f6b14b2888",
  			"name": "RiskMFAScoring"
  		},
  		"ip": "'"$IP"'",
  		"flow": {
  			"type": "AUTHENTICATION"
  		},
  		"session": {
  			"id": "002b1094-9676-42c3-9f4f-56ef112c6918"
  		},
  		"user": {
  			"id": "'"$MAIL"'",
  			"name": "'"$NAME"'",
  			"type": "EXTERNAL",
  			"groups": [
  				{
  					"name": "seasonal"
  				},
  				{
  					"name": "yellow"
  				}
  			]
  		},
  		"sharingType": "SHARED",
  		"browser": {
  			"userAgent": "'"$AGENT"'",
  			"language": "en",
  			"colorDepth": 24,
  			"deviceMemory": 8,
  			"hardwareConcurrency": 8,
  			"screenResolution": [
  				900,
  				1440
  			],
  			"availableScreenResolution": [
  				877,
  				1380
  			],
  			"timezoneOffset": -5.0,
  			"timezone": "New York/US",
  			"sessionStorage": true,
  			"localStorage": true,
  			"indexedDb": true,
  			"addBehaviour": null,
  			"openDatabase": true,
  			"cpuClass": "not available",
  			"platform": "'"$PLATFORM"'",
  			"plugins": [
  				[
  					"Chrome PDF Plugin",
  					"Portable Document Format",
  					[
  						"application x-google-chrome-pdf",
  						"pfg"
  					]
  				],
  				[
  					"Chrome PDF Viewer",
  					[
  						"application x-google-chrome-pdf",
  						"pdf"
  					]
  				]
  			],
  			"webglVendorAndRenderer": "Intel Inc.~Intel Iris Pro OpenGL Engine",
  			"webgl": [
  				"webgl aliased line width range:[1, 1]",
  				"webgl alpha bits:8",
  				"webgl antialiasing:yes",
  				"webgl blue bits:8",
  				"webgl depth bits:24",
  				"webgl green bits:8",
  				"webgl max anisotropy:16"
  			],
  			"adBlock": false,
  			"hasLiedLanguages": false,
  			"hasLiedResolution": false,
  			"hasLiedOs": false,
  			"hasLiedBrowser": false,
  			"touchSupport": [
  				"0",
  				"false",
  				"false"
  			],
  			"fonts": [
  				"Arial",
  				"Comic Sans MS",
  				"Courier",
  				"Courier New",
  				"Helvetica"
  			],
  			"audio": "124.04345808873768"
  		},
  		"origin": "'"$APP"'"
  	},
      "riskPolicySet": {
        "id": "'"$RISKID"'",
        "name": "Default Risk Policy"
      }
  }'
 
}

#
#while [ $i -ne $numbertoload ]
#do
## jot is used to get a random line value
## jot syntax is asking jot to make 1 random number between 1 and the total lines of the file
#  CHOOSEIP =`jot -r 1 1 "$IPCOUNT"`
#  CHOOSENAME =`jot -r 1 1 "$NAMECOUNT"`
#  CHOOSEMAILDOMAIN =`jot -r 1 1 "$MAILCOUNT"`
#  CHOOSEPLATFORM =`jot -r 1 1 "$PLATFORMCOUNT"`
#  CHOOSEAGENT =`jot -r 1 1 "$AGENTCOUNT"`
#  CHOOSEAPP =`jot -r 1 1 "$APPSCOUNT"`
#
#  CHOOSEBADIP=`jot -r 1 1 "$BADIPCOUND"`
#  CHOOSEBADNAME=`jot -r 1 1 "$NAMECOUNT"`
#  CHOOSEBADMAILDOMAIN=`jot -r 1 1 "$MAILCOUNT"`
#  CHOOSEBADPLATFORM=`jot -r 1 1 "$PLATFORMCOUNT"`
#  CHOOSEBADAGENT=`jot -r 1 1 "$AGENTCOUNT"`
#  CHOOSEBADAPP=`jot -r 1 1 "$APPSCOUNT"`
## increase the counter
#  i=$(($i+1))
#
#  # Show run counter
#  echo "We are loading number $i"
#  
#  NAME=`gawk "NR==$CHOOSENAME" names`
#  MAILDOMAIN=`gawk "NR==$CHOOSEMAILDOMAIN" MailDomains`
#  AGENT=`gawk "NR==$CHOOSEAGENT" Agents`
#  PLATFORM=`gawk "NR==$CHOOSEPLATFORM" Platforms`
#  MAIL=`echo $NAME | sed 's/ /./' | sed 's/$/@'"$MAILDOMAIN"'/' ` 
#  APP=`gawk "NR==$CHOOSEAPP" AppsUsed`
#  # Send request then send badactors if enabled
#  IP=`gawk "NR=="$CHOOSEIP"" ips`
#  THROWTHEPIE 
#
#if [[ "$BADACTORS" == "YES" ]] ;
# then
#  NAME=`gawk "NR==$CHOOSEBADNAME" names`
#  MAILDOMAIN=`gawk "NR==$CHOOSEBADMAILDOMAIN" MailDomains`
#  AGENT=`gawk "NR==$CHOOSEBADAGENT" Agents`
#  PLATFORM=`gawk "NR==$CHOOSEBADPLATFORM" Platforms`
#  MAIL=`echo $NAME | sed 's/ /./' | sed 's/$/@'"$MAILDOMAIN"'/' ` 
#  APP=`gawk "NR==$CHOOSEBADAPP" AppsUsed`
#  IP=`gawk "NR=="$CHOOSEBADIP"" badips`
#  THROWTHEPIE
#fi
#
#done
#
#
#
