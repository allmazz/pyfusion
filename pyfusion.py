from requests import get, post
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring


class RGBFusionClient:
    def __init__(self, url):
        self.url = url  # Saving URL

    def auth(self):
        r = get(url=self.url, params={"Get_Type": 0})
        tree = fromstring(r.text)  # Parsing answer
        if 'Password_Str' in tree.attrib:
            self.password = tree.attrib['Password_Str']  # Saving password
            return True
        else:
            return False

    def submit(self, data):
        top = Element('xml')  # Creating XML document
        ezled = SubElement(top, 'LED_info_Easy')
        ezled.attrib = data
        submit_data = tostring(top)
        # Headers from original android app
        headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows 2000)",
                   "Content-Type": "multipart/form-data;boundary=*****",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Encoding": "gzip"}
        r = post(url=self.url, params={"Get_Type": 0}, headers=headers, data=submit_data)
        if "Upload OK!" in r.text:
            return True
        else:
            return False

    def calculate_color(self, color):
        return str(int("FF" + color, 16))  # Converting color code to hexadecimal

    def color(self, color: str, brightness: str):  # Speed: 0-5 Brightness: 0-9
        data = {"Pattern": "0", "Profile": "1", "Mode": "0", "Othermode": "1", "color": self.calculate_color(color),
                "S_Time": "09:00",
                "E_Time": "01:00", "Br": brightness, "Sp": "0", "Support_Flag": "191", "Password_Str": self.password}
        return self.submit(data)

    def pulse(self, color: str, speed: str):
        data = {"Pattern": "1", "Profile": "1", "Mode": "0", "Othermode": "1", "color": self.calculate_color(color),
                "S_Time": "09:00",
                "E_Time": "01:00", "Br": "0", "Sp": speed, "Support_Flag": "191", "Password_Str": self.password}
        return self.submit(data)

    def flash(self, color: str, speed: str, brightness: str):
        data = {"Pattern": "4", "Profile": "1", "Mode": "0", "Othermode": "1", "color": self.calculate_color(color),
                "S_Time": "09:00",
                "E_Time": "01:00", "Br": brightness, "Sp": speed, "Support_Flag": "191", "Password_Str": self.password}
        return self.submit(data)

    def double_flash(self, color: str, speed: str, brightness: str):
        data = {"Pattern": "11", "Profile": "1", "Mode": "0", "Othermode": "1", "color": self.calculate_color(color),
                "S_Time": "09:00",
                "E_Time": "01:00", "Br": brightness, "Sp": speed, "Support_Flag": "191", "Password_Str": self.password}
        return self.submit(data)

    def cycle(self, speed: str):
        data = {"Pattern": "9", "Profile": "1", "Mode": "0", "Othermode": "1", "color": "", "S_Time": "09:00",
                "E_Time": "01:00", "Br": "0", "Sp": speed, "Support_Flag": "191", "Password_Str": self.password}
        return self.submit(data)

    def music(self, color: str):  # Put 020202 in color to random color
        data = {"Pattern": "2", "Profile": "1", "Mode": "0", "Othermode": "1", "color": self.calculate_color(color),
                "S_Time": "09:00",
                "E_Time": "01:00", "Br": "9", "Sp": "0", "Support_Flag": "191", "Password_Str": self.password}
        return self.submit(data)

    def random(self, speed: str, brightness: str):
        data = {"Pattern": "5", "Profile": "1", "Mode": "0", "Othermode": "1", "color": "0", "S_Time": "09:00",
                "E_Time": "01:00", "Br": brightness, "Sp": speed, "Support_Flag": "191", "Password_Str": self.password}
        return self.submit(data)

    def game(self):
        data = {"Pattern": "32", "Profile": "1", "Mode": "0", "Othermode": "1", "color": "0", "S_Time": "09:00",
                "E_Time": "01:00", "Br": "2", "Sp": "2", "Support_Flag": "191", "Password_Str": self.password}
        return self.submit(data)

    def turn_off(self):
        data = {"Pattern": "8", "Profile": "1", "Mode": "0", "Othermode": "1", "color": "4278190080", "S_Time": "09:00",
                "E_Time": "01:00", "Br": "2", "Sp": "2", "Support_Flag": "191", "Password_Str": self.password}
        return self.submit(data)

    def get_info(self):
        r = get(url=self.url, params={"Get_Type": 0})
        tree = fromstring(r.text)  # Parsing XML
        tree.attrib['color'] = hex(int(tree.attrib['color']))[4:]  # Converting color string to hex, and delete first 4 symobls to get color code
        del tree.attrib["Password_Str"]
        return tree.attrib
