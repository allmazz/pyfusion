# pyfusion
Reversed RGB Fusion 2.0 protocol and library for using it
I have reversed the mobile application of the RGB Fusion, or rather, the protocol for communicating with a computer.

**Since I only have one device with support for the RGB Fusion, I can not fully test the library. I will be glad to improvements and reports of problems.**
# Install
Clone repository, install `requirements.txt` and put `pyfusion.py` in project directory.
# Using
`import pyfusion.py`
First you need to get a password and check the availability of the RGB Fusion server.
Default port is 9009(TCP)
```
client = pyfusion.RGBFusionClient("http://192.168.1.10:9009/")
client.auth()
```
It's all! Now you can change modes and colors
Colors must be as HEX without #. Example `ff0000`
Speed range is 0-5
Brightness range is 0-9
Color, speed, brightness must be strings. Very stranger protocol.

**All available methods**:

`client.color("ff0000", "9") # Color, brightness`

`client.pulse("ff0000", "5") # Color, speed`

`client.flash("ff0000", "5", "9") # Color, speed, brightness`

`client.double_flash("ff0000", "5", "9") # Color, speed, brightness`

`client.cycle("5") # Speed`

`client.music("ff0000") # Color. Put "020202" in color for random color`

`client.random("5", "9") # Speed, brightness`

`client.game()`

`client.turn_off()`

`client.get_info()`

Will be return led's state.

Example:

{'Pattern': '1', 'Profile': '1', 'Mode': '0', 'Othermode': '1', 'color': 'ff0000', 'S_Time': '09:00', 'E_Time': '01:00', 'Br': '0', 'Sp': '3', 'Support_Flag': '191', 'MCU_FW': '0'}

You can submit own request using

`client.submit(data)`

`data` must be dectionary with data.

Example:

`{"Pattern": "8", "Profile": "1", "Mode": "0", "Othermode": "1", "color": "4278190080", "S_Time": "09:00", "E_Time": "01:00", "Br": "2", "Sp": "2", "Support_Flag": "191", "Password_Str": "123"}`

More details can be found in the protocol description.

All methods return True if the request was sent successfully, or False upon error. True does not mean that all data is correct and the request is correct. This will indicate a successful shipment. Unfortunately, if the data is not correct, the server still returns a Positive result.

# RGB Fusion Protocol description
Server is working on 0.0.0.0:9009.
Working with the protocol looks like this: the client submits a Get request to /?Get_Type=0(I think 0 denotes the hardware on which the backlight changes, but I only have MB and I can’t verify this).
Response is XML of approximately this type:
```
<?xml version="1.0" encoding="utf-8"?><LED_info_Easy Pattern="2" Profile="1" Mode="0" Othermode="1" color="4278321666" S_Time="09:00" E_Time="01:00" Br="9" Sp="0" Support_Flag="191" Password_Str="123" MCU_FW="0" />
```
The operating mode is displayed in the Pattern. The funny thing is that the RGB Fusion program can set a password, which we see in this request. It turns out that the password is compared by the client application.
For change light state we must send POST request to /?Get_Type=0 with data equivalent to the response from the server, only with its own values.

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8

Content-Type: multipart/form-data;boundary=*****

Request example:
```
<xml><LED_info_Easy Br="9" E_Time="01:00" Mode="0" Othermode="1" Password_Str="123" Pattern="0" Profile="1" S_Time="09:00" Sp="0" Support_Flag="191" color="4294901786" /></xml>
```

If the request is received in response, you will receive a XML document with the text "Upload OK!" You will receive another only if your headings are incorrect. Even if there is an error in the data, the server will not say this.

## Request data desription:
**All keys must be strings**

Main object called LED_info_Easy must contain:
* Patern: light mode. 0: static color, 1: pulse, 4: flash, 11: double_flash, 9: cycle, 2: music, 5: random, 32: game, 8: turn off leds.
**If speed / brightness / color cannot be specified in the corresponding method, then this data cannot be specified for this mode.**
* Br: brightness, can be 0-9. If mode dont using brightness key must be with any value!
* Sp: spped, can be 0-5. If mode dont using speed key must be with any value!
* color: color in hexadecimal code. It's "FF" + HEX color(FF`ff0000`)
* Mode="0" I don't know what that means.
* Othermode="0" I don't know what that means.
* Profile="1" I don't know what that means.
* E_Time="01:00" I don't know what that means.
* S_Time="09:00" I don't know what that means.
* Support_Flag="191" I don't know what that means.
* Password_Str: password, which can be obtained in the Get request.

Perhaps the keys, the value of which I do not know, are somehow related to the choice of hardware, the backlight of which is controlled

You can study the source code of the library for a better understanding of the protocol.
