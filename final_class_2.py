from customtkinter import *
from PIL import Image as Img
import geocoder
from geopy.geocoders import Nominatim
import requests

api_key = "418c82f22eb5581a48dd631a74d5788c"  

def get_device_location_city():
    # Use 'ipinfo' provider to get the location based on IP address
    location = geocoder.ipinfo("me")
    if location.ok:
        latitude, longitude = (
            location.latlng
        )  # Returns latitude and longitude as a tuple
        geolocator = Nominatim(user_agent="device_location")
        address = geolocator.reverse((latitude, longitude))
        return address[0].split(", ")[3]
    else:
        print("Failed to retrieve device location.")
        return None

class EntryFrame(CTkFrame):
    def __init__(self, parent, height):
        super().__init__(parent)
        self.height = height
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.bottom_frame=BottomFrame(parent,1,0)
        self.create_widgets()
        self.place(x=0, y=0, relwidth=1, relheight=self.height)
        self.city = get_device_location_city()

    def animate_locate(self):
        bot=self.bottom_frame
        bot.pos=1
        bot.place(relx=bot.pos,rely=0.5,relwidth=1,relheight=0.5)
        bot.create_widgets(bot.get_weather(self.city))
        bot.animate()
    def animate(self):
        newcity=self.city_var.get()
        if newcity:
            bot=self.bottom_frame
            bot.pos=1
            bot.place(relx=bot.pos,rely=0.5,relwidth=1,relheight=0.5)
            bot.create_widgets(bot.get_weather(newcity))
            bot.animate()

    def create_widgets(self):
        sub_top_frame1 = CTkFrame(self, fg_color="transparent")
        sub_top_frame2 = CTkFrame(self, fg_color="transparent")
        sub_top_frame3 = CTkFrame(self, fg_color="transparent")
        label1 = CTkLabel(
            sub_top_frame1,
            text="Enter your city name here",
            font=("Century Gothic", 20, "bold"),
        )
        label2 = CTkLabel(
            sub_top_frame2, text="OR", font=("Century Gothic", 53, "bold")
        )
        label3 = CTkLabel(
            sub_top_frame3,
            text="Don't know where you are!!",
            font=("Century Gothic", 20, "bold"),
        )
        label4 = CTkLabel(
            sub_top_frame3,
            text="Find your current city's weather\nHERE",
            font=("Century Gothic", 20, "bold"),
        )
        self.city_var = StringVar()
        city_entry = CTkEntry(sub_top_frame1, textvariable=self.city_var)
        city_enter_button = CTkButton(sub_top_frame1, text="Get Weather",command=self.animate)
        get_city_button = CTkButton(
            sub_top_frame3, text="Get Weather", command=self.animate_locate
        )
        sub_top_frame1.grid(row=0, column=0, sticky="nsew", columnspan=3)
        sub_top_frame2.grid(row=0, column=3, sticky="ew")
        sub_top_frame3.grid(row=0, column=4, sticky="nsew", columnspan=3)
        label1.place(relx=0.5, rely=0.25, anchor="center")
        label2.place(relx=0.5, rely=0.5, anchor="center")
        city_entry.place(relx=0.5, rely=0.5, anchor="center")
        city_enter_button.place(relx=0.5, rely=0.75, anchor="center")
        label3.place(relx=0.5, rely=0.25, anchor="center")
        label4.place(relx=0.5, rely=0.5, anchor="center")
        get_city_button.place(relx=0.5, rely=0.75, anchor="center")


class BottomFrame(CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(parent)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.pos=start_pos
        self.city_var = StringVar()
        self.place(
            relx=self.pos,
            rely=0.5,
            relwidth=1,
            relheight=0.5
        )

    def create_widgets(self, weather_info):
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2), weight=1, uniform="a")
        self.location_logo = CTkImage(Img.open("location.png"))
        self.temperature_logo = CTkImage(Img.open("temperature.png"))
        self.weather_logo = CTkImage(Img.open("weather.png"))
        self.pressure_logo = CTkImage(Img.open("pressure.png"))
        self.humidity_logo = CTkImage(Img.open("humidity.png"))
        self.wind_speed_logo = CTkImage(Img.open("wind_speed.png"))
        CTkLabel(
            self,
            text=f"   City: {weather_info["name"]}",
            font=("Century Gothic", 20, "bold"),
            image=self.location_logo,
            compound="left",
        ).grid(row=0, column=0, sticky="nsew"),
        CTkLabel(
            self,
            text=f"   Weather: {weather_info["weather"]}",
            font=("Century Gothic", 20, "bold"),
            image=self.weather_logo,
            compound="left",
        ).grid(row=0, column=1, sticky="nsew")
        CTkLabel(
            self,
            text=f"   Temperature: {weather_info["temp_c"]} ⁰C",
            font=("Century Gothic", 20, "bold"),
            image=self.temperature_logo,
            compound="left",
        ).grid(row=1, column=0, sticky="nsew")
        CTkLabel(
            self,
            text=f"   Pressure: {weather_info["pressure"]} Pa",
            font=("Century Gothic", 20, "bold"),
            image=self.pressure_logo,
            compound="left",
        ).grid(row=1, column=1, sticky="nsew")
        CTkLabel(
            self,
            text=f"   Humidity: {weather_info["humidity"]} %",
            font=("Century Gothic", 20, "bold"),
            image=self.humidity_logo,
            compound="left",
        ).grid(row=2, column=0, sticky="nsew")
        CTkLabel(
            self,
            text=f"   Wind Speed: {weather_info["wind_speed"]} m/s",
            font=("Century Gothic", 20, "bold"),
            image=self.wind_speed_logo,
            compound="left",
        ).grid(row=2, column=1, sticky="nsew")
        self.button=CTkButton(self,text="Get Temperature in K",command=self.change_temp_unit)
        self.button.place(relx=0.5,rely=0.9,anchor="center")
    def change_temp_unit(self):
        if self.button._text[-1]=="K":
            CTkLabel(
            self,
            text=f"   Temperature: {self.weather_info["temp_k"]} K",
            font=("Century Gothic", 20, "bold"),
            image=self.temperature_logo,
            compound="left",).grid(row=1, column=0, sticky="nsew")
            self.button.configure(text="Get temperature in ⁰F")
        elif self.button._text[-1]=="F":
            CTkLabel(
            self,
            text=f"   Temperature: {round(self.weather_info["temp_f"],2)} ⁰F",
            font=("Century Gothic", 20, "bold"),
            image=self.temperature_logo,
            compound="left",).grid(row=1, column=0, sticky="nsew")
            self.button.configure(text="Get Temperature in ⁰C")
        elif self.button._text[-1]=="C":
            CTkLabel(
            self,
            text=f"   Temperature: {self.weather_info["temp_c"]} ⁰C",
            font=("Century Gothic", 20, "bold"),
            image=self.temperature_logo,
            compound="left",).grid(row=1, column=0, sticky="nsew")
            self.button.configure(text="Get Temperature in K")        
    def get_weather(self,city):
        weather_data = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}"
        ).json()
        name = weather_data["name"]
        weather = weather_data["weather"][0]["main"]
        temp_k = weather_data["main"]["temp"]
        temp_c = round(temp_k - 273.15, 2)
        temp_f = temp_c * (9 / 5) + 32
        pressure = weather_data["main"]["pressure"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        self.weather_info={"name":name,"weather":weather,"temp_k":temp_k,"temp_c":temp_c,"temp_f":temp_f,"pressure":pressure,"humidity":humidity,"wind_speed":wind_speed}
        return self.weather_info
    def animate(self):
        if self.pos<=0:
            self.animate_right()
        elif self.pos>=1:
            self.animate_left()
    def animate_right(self):
        if self.pos<1:
            self.pos+=0.025
            self.place(relx=self.pos,
            rely=0.5,
            relwidth=1,
            relheight=0.5)
            self.after(10,self.animate_right)
    def animate_left(self):
        if self.pos>=0:
            self.pos-=0.025
            self.place(relx=self.pos,
            rely=0.5,
            relwidth=1,
            relheight=0.5)
            self.after(10,self.animate_left)
window = CTk()
window.title("Weathery")
window.geometry("800x600")
entryframe = EntryFrame(window, 0.5)
# bottom_frame=BottomFrame(window,0,1)
window.mainloop()
