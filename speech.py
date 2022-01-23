import speech_recognition as sr
from tkinter import *
import cv2
import numpy as np
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.core.text import Label as CoreLabel
import pyscreenshot as ImageGrab
from kivy.config import Config

from gtts import gTTS
import os
mytext = 'Hey welcome what do you want to color'
myaudiotext = 'Speak correctly please !!!'
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj2 = gTTS(text=myaudiotext, lang=language, slow=False)

myobj.save("welcome.mp3")
myobj2.save("error.mp3")

ListOfObjects = {'Apple':'red','Fish':'blue','Leaf':'green'}

Config.set('graphics', 'width', 2880)
Config.set('graphics','height', 1800)

class MyBackground(Widget):
    def __init__(self, **kwargs):
        super(MyBackground, self).__init__(**kwargs)
        with self.canvas:
            Window.clearcolor = (1, 1, 1, 1)
            object = r.recognize_google(audio);
            #random.randInt(1,10)
            file = object + ".png"
            print(file)
            image = cv2.imread(file)
            img = cv2.imread(file,0)
            ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

            cv2.imshow("original image", img)
            cv2.imshow("rgb image", image)

            image = np.rot90(np.swapaxes(image, 0, 1))

            cv2.imshow("Binary Image", bw_img)
            cv2.imwrite(object + "_gray.png",img)
            cv2.imwrite(object + "_bin.png",bw_img)

            img = cv2.imread(object + "_gray.png")
            bw_img = cv2.imread(object + "_bin.png")
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            #self.bg = Rectangle(source=object+'e'+'.gif', size=(400, 400), pos=(100, 800))
            video_texture_3D = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='rgb')
            video_texture_3D.blit_buffer(image.tostring(), colorfmt='bgr', bufferfmt='ubyte')
            self.bg = Rectangle(texture=video_texture_3D, size=(400, 400), pos=(100, 800))
            self.bind(pos=self.update_bg_3D)
            self.bind(size=self.update_bg_3D)
            img = np.rot90(np.swapaxes(img, 0, 1))

            video_texture_2D = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='rgb')

            video_texture_2D.blit_buffer(img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
            #self.bg = Rectangle(source=object+'Sample'+'.gif', size=(400, 400), pos=(800, 800))
            self.bg = Rectangle(texture=video_texture_2D, size=(400, 400), pos=(800, 800))
            self.bind(pos=self.update_bg_2D)
            self.bind(size=self.update_bg_2D)
            #self.bg = Rectangle(source=object+'.gif', size=(600, 600), pos=(300, 500))
            #self.bg = Rectangle(source='moon.png', size=(600, 600), pos=(300, 500))
            bw_img = np.rot90(np.swapaxes(bw_img, 0, 1))
            video_texture_1D = Texture.create(size=(bw_img.shape[1], bw_img.shape[0]), colorfmt='rgb')
            video_texture_1D.blit_buffer(bw_img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
            self.bg = Rectangle(texture=video_texture_1D, size=(600, 600), pos=(300, 500))
            self.bind(pos=self.update_bg_1D)
            self.bind(size=self.update_bg_1D)


    def update_bg_3D(self, *args):
        self.bg.pos = (100., 800.)
        self.bg.size = (400., 400.)


    def update_bg_2D(self, *args):
        self.bg.pos = (500., 800.)
        self.bg.size = (400., 400.)

    def update_bg_1D(self, *args):
        self.bg.pos = (300., 0.)
        self.bg.size = (600., 600.)

class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        with self.canvas:

            Color(*color, mode='hsv')
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=5)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]




os.system("mpg321 welcome.mp3")
# Record Audio
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# Speech recognition using Google Speech Recognition
try:
    print("You said: " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
    os.system("mpg321 error.mp3")
    exit()
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

class MyPaintApp(App):

    def build(self):

        parent = MyBackground()
        self.painter = MyPaintWidget()
        clearbtn = Button(text='Clear')
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        savebtn = Button(text='Save',pos=(1000, 0))
        savebtn.bind(on_release=self.save)
        parent.add_widget(savebtn)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()

    def save(self, *args):
        im = ImageGrab.grab()
        im.save('screenshot.png')



if __name__ == '__main__':
    MyPaintApp().run()