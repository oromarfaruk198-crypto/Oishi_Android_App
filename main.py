import os
import random
import math
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, Line

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
FONT = os.path.join(BASE_DIR, "fonts", "NotoSansBengali-Regular.ttf")
FONT_BOLD = os.path.join(BASE_DIR, "fonts", "NotoSansBengali-Bold.ttf")

SPECIAL = [
    "Oishi, তুমি আমার কাছে সত্যিই খুব special ♥",
    "তোমার একটা smile আমার পুরো দিনটা সুন্দর করে দিতে পারে ♥",
    "তুমি পাশে থাকলে ordinary মুহূর্তও special হয়ে যায় ♥",
    "তোমাকে পেয়ে আমি সত্যিই lucky ♥",
]
LOVE = [
    "I love you Oishi ♥",
    "তুমি আমার heart-এর সবচেয়ে সুন্দর জায়গাটায় আছো ♥",
    "তোমাকে ভালোবাসার কোনো special reason লাগে না ♥",
    "Every day, I choose you again and again ♥",
]
CUTE = [
    "তুমি রাগ করলে আরও cute লাগে ♥",
    "তোমার হাসিটা আমার favourite thing ♥",
    "Oishi = Cute + Beautiful + Special ♥",
    "তুমি একটু বেশি-ই সুন্দর ♥",
]
SORRY = [
    "Oishi, যদি কখনো তোমাকে কষ্ট দিয়ে থাকি, I'm really sorry ♥",
    "আমার ভুল হলে আমাকে ক্ষমা করে দিও ♥",
    "I never want to hurt you. Sorry Oishi ♥",
    "তোমার মুখে হাসি দেখতে চাই, রাগ নয় ♥",
]
SURPRISE = [
    "SURPRISE! তুমি আমার সবচেয়ে special person ♥",
    "এই surprise শুধু তোমার জন্য Oishi ♥",
    "You are my favourite notification ♥",
    "তোমার জন্য আমার ভালোবাসা সবসময় থাকবে ♥",
]

class RoundedButton(Button):
    bg_color = ListProperty([1, 0.36, 0.57, 1])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_name = FONT_BOLD if os.path.exists(FONT_BOLD) else FONT
        self.font_size = sp(14)
        self.bold = True
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
        self.bind(pos=self._update, size=self._update, bg_color=self._update_color)
    def _update(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size
    def _update_color(self, *_):
        self.canvas.before.children[-2].rgba = self.bg_color

class Card(FloatLayout):
    def __init__(self, dark=False, **kwargs):
        super().__init__(**kwargs)
        self.bg = [0.22,0.13,0.17,1] if dark else [1,1,1,1]
        with self.canvas.before:
            Color(*self.bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(22)])
            Color(0.95,0.45,0.62,1)
            self.line = Line(rounded_rectangle=(self.x,self.y,self.width,self.height,dp(22)), width=1.1)
        self.bind(pos=self._update, size=self._update)
    def _update(self, *_):
        self.rect.pos = self.pos; self.rect.size = self.size
        self.line.rounded_rectangle = (self.x,self.y,self.width,self.height,dp(22))

class ClickableImage(Image):
    def __init__(self, on_click=None, **kwargs):
        super().__init__(**kwargs)
        self.on_click = on_click
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.on_click:
            self.on_click(); return True
        return super().on_touch_down(touch)

class OishiApp(App):
    def build(self):
        self.title = "Oishi ♥"
        self.dark = False
        self.music_on = False
        self.sound = None
        self.last_message = None
        self.gallery_files = []
        self.gallery_index = 0
        self.sm = ScreenManager(transition=SlideTransition(duration=.22))
        self.opening()
        Window.bind(on_keyboard=self.on_keyboard)
        return self.sm

    def bg(self): return [0.996,0.95,0.972,1] if not self.dark else [0.14,0.08,0.11,1]
    def text(self): return [0.35,0.19,0.27,1] if not self.dark else [1,0.91,0.95,1]
    def card(self): return [1,1,1,1] if not self.dark else [0.22,0.13,0.17,1]
    def button(self): return [1,0.30,0.53,1] if not self.dark else [0.85,0.25,0.49,1]

    def base(self, name):
        if self.sm.has_screen(name): self.sm.remove_widget(self.sm.get_screen(name))
        s = Screen(name=name)
        root = FloatLayout()
        root.canvas.before.clear()
        with root.canvas.before:
            Color(*self.bg()); root.rect = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *_: setattr(root.rect,'pos',root.pos), size=lambda *_: setattr(root.rect,'size',root.size))
        s.add_widget(root); self.sm.add_widget(s)
        self.hearts(root, 7)
        return s, root

    def hearts(self, root, count=8):
        for _ in range(count):
            h = Label(text=random.choice(["♥","♡","♥","♡"]), font_name=FONT, font_size=sp(random.randint(18,28)),
                      color=(1,.42,.62,random.uniform(.25,.65)), size_hint=(None,None), size=(dp(35),dp(35)),
                      pos=(random.uniform(0, max(1,Window.width-dp(35))), -dp(40)))
            root.add_widget(h)
            dur=random.uniform(5,9); x=random.uniform(0,max(1,Window.width-dp(35)))
            anim=Animation(y=Window.height+dp(50), x=x+random.uniform(-dp(35),dp(35)), opacity=.05, duration=dur)
            anim.bind(on_complete=lambda a,w: root.remove_widget(w) if w.parent else None)
            Clock.schedule_once(lambda dt,a=anim,w=h:a.start(w), random.uniform(0,2.5))

    def title_label(self, text, size=sp(30)):
        return Label(text=text, font_name=FONT_BOLD if os.path.exists(FONT_BOLD) else FONT, font_size=size,
                     color=(1,.30,.53,1), bold=True, halign='center', valign='middle', size_hint_y=None, height=dp(55))

    def button(self, text, callback, height=dp(48)):
        b=RoundedButton(text=text, bg_color=self.button(), size_hint_y=None, height=height)
        b.bind(on_release=callback)
        return b

    def stack(self, root, padding=dp(16), spacing=dp(8)):
        box=BoxLayout(orientation='vertical', padding=padding, spacing=spacing, size_hint=(.86,None), height=dp(590), pos_hint={'center_x':.5,'center_y':.5})
        root.add_widget(box); return box

    def opening(self):
        s,root=self.base('opening')
        box=BoxLayout(orientation='vertical', spacing=dp(12), size_hint=(.9,None), height=dp(310), pos_hint={'center_x':.5,'center_y':.5}, padding=dp(12))
        root.add_widget(box)
        box.add_widget(self.title_label('Oishi ♥', sp(44)))
        sub=Label(text='A little surprise made just for you...', font_name=FONT, font_size=sp(16), color=self.text(), halign='center')
        box.add_widget(sub)
        box.add_widget(self.button('Enter ♥', lambda *_: self.home(), dp(54)))
        foot=Label(text='Made with ♥ by Omar', font_name=FONT, font_size=sp(12), color=[.55,.38,.45,1], size_hint_y=None, height=dp(35))
        box.add_widget(foot)
        self.sm.current='opening'

    def home(self):
        s,root=self.base('home')
        box=self.stack(root, dp(14), dp(7))
        box.add_widget(self.title_label('Welcome Oishi ♥', sp(29)))
        box.add_widget(Label(text='Choose something special...', font_name=FONT, font_size=sp(14), color=self.text(), size_hint_y=None, height=dp(32)))
        items=[
            ('♥ Special Message', lambda *_: self.message('Special Message',SPECIAL)),
            ('♥ Love Letter', lambda *_: self.love_letter()),
            ('♥ Cute Zone', lambda *_: self.message('Cute Zone',CUTE)),
            ('♥ Sorry', lambda *_: self.message('Sorry',SORRY)),
            ('♥ Surprise', lambda *_: self.surprise()),
            ('♥ Just Oishi', lambda *_: self.oishi()),
            ('♥ Photo Gallery', lambda *_: self.gallery()),
            ('♥ Music: ON' if self.music_on else '♥ Music: OFF', lambda *_: self.toggle_music()),
            ('☾ Dark Mode' if not self.dark else '☀ Light Mode', lambda *_: self.toggle_theme()),
        ]
        for t,c in items: box.add_widget(self.button(t,c,dp(43)))
        self.sm.current='home'

    def message(self,title,messages):
        s,root=self.base('message')
        box=BoxLayout(orientation='vertical', spacing=dp(12), size_hint=(.9,None), height=dp(520), pos_hint={'center_x':.5,'center_y':.5}, padding=dp(10))
        root.add_widget(box); box.add_widget(self.title_label(title,sp(29)))
        card=Card(self.dark, size_hint_y=None, height=dp(190)); box.add_widget(card)
        lab=Label(text='', font_name=FONT_BOLD if os.path.exists(FONT_BOLD) else FONT, font_size=sp(19), color=self.text(), halign='center', valign='middle', text_size=(dp(290),None), size_hint=(.9,.9), pos_hint={'center_x':.5,'center_y':.5})
        card.add_widget(lab); self.typewriter(lab,self.pick(messages))
        box.add_widget(self.button('♥ Another Message', lambda *_: self.message(title,messages), dp(50)))
        box.add_widget(self.button('← Back', lambda *_: self.home(), dp(48)))
        self.sm.current='message'

    def pick(self, messages):
        choices=[m for m in messages if m != self.last_message] or messages
        self.last_message=random.choice(choices); return self.last_message
    def typewriter(self, label, text, i=0):
        if not label.parent: return
        label.text=text[:i]
        if i < len(text): Clock.schedule_once(lambda dt:self.typewriter(label,text,i+1), .025)

    def love_letter(self):
        s,root=self.base('letter')
        box=self.stack(root,dp(16),dp(10)); box.height=dp(560)
        box.add_widget(self.title_label('♥ A Letter For Oishi',sp(28)))
        card=Card(self.dark); card.size_hint_y=1; box.add_widget(card)
        letter=("Dear Oishi ♥\n\nতুমি আমার জীবনের এমন একজন মানুষ,\nযাকে হারানোর কথা আমি কখনো ভাবতে চাই না।\n\nতোমার হাসি, তোমার কথা,\nতোমার ছোট ছোট অভিমান—সবকিছুই আমার কাছে special।\n\nMaybe I'm not perfect,\nbut my feelings for you are real. ♥\n\nAlways stay happy, Oishi. ♥\n\nWith Love,\nOmar ♥")
        card.add_widget(Label(text=letter,font_name=FONT,font_size=sp(15),color=self.text(),halign='center',valign='middle',text_size=(dp(320),None),pos_hint={'center_x':.5,'center_y':.5},size_hint=(.92,.9)))
        box.add_widget(self.button('← Back',lambda *_:self.home(),dp(48))); self.sm.current='letter'

    def surprise(self):
        s,root=self.base('surprise'); box=self.stack(root); box.height=dp(460)
        box.add_widget(self.title_label('♥ Surprise',sp(34)))
        lab=Label(text='Click the button to reveal your surprise...',font_name=FONT_BOLD if os.path.exists(FONT_BOLD) else FONT,font_size=sp(17),color=self.text(),halign='center',valign='middle',text_size=(dp(320),None),size_hint_y=1)
        box.add_widget(lab)
        def reveal(*_):
            lab.text=self.pick(SURPRISE); self.explode(root,Window.width/2,Window.height/2,28); self.hearts(root,12)
        box.add_widget(self.button('✦ Reveal Surprise',reveal,dp(54))); box.add_widget(self.button('← Back',lambda *_:self.home(),dp(48)))
        self.sm.current='surprise'

    def oishi(self):
        s,root=self.base('oishi'); box=self.stack(root); box.height=dp(500)
        box.add_widget(self.title_label('♥ Just Oishi ♥',sp(34)))
        msg='There is only one Oishi...\n\nand she is very special to me. ♥\n\nYou are beautiful.\nYou are cute.\nYou are important.\n\nNever forget that. ♥'
        box.add_widget(Label(text=msg,font_name=FONT_BOLD if os.path.exists(FONT_BOLD) else FONT,font_size=sp(19),color=self.text(),halign='center',valign='middle',text_size=(dp(330),None)))
        box.add_widget(self.button('← Back',lambda *_:self.home(),dp(48))); self.sm.current='oishi'

    def get_images(self):
        if not os.path.isdir(IMAGE_DIR): os.makedirs(IMAGE_DIR,exist_ok=True)
        exts=('.png','.jpg','.jpeg','.gif','.ppm','.pgm')
        return sorted([f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(exts) and os.path.isfile(os.path.join(IMAGE_DIR,f))], key=str.lower)
    def photo_name(self,f):
        n=f.lower()
        if n=='omar.png': return 'Omar ♥'
        if n in ('oishi.png','pakhi.png'): return 'Oishi ♥'
        return os.path.splitext(f)[0].replace('_',' ').replace('-',' ').title()+' ♥'

    def gallery(self):
        s,root=self.base('gallery'); self.gallery_files=self.get_images(); self.gallery_index=0
        box=BoxLayout(orientation='vertical', spacing=dp(6), size_hint=(.94,.94), pos_hint={'center_x':.5,'center_y':.49}, padding=dp(5)); root.add_widget(box)
        box.add_widget(self.title_label('♥ Our Photo Gallery',sp(27)))
        box.add_widget(Label(text='Every picture has a little memory... ♥',font_name=FONT,font_size=sp(12),color=self.text(),size_hint_y=None,height=dp(25)))
        self.gallery_holder=FloatLayout(size_hint_y=1); box.add_widget(self.gallery_holder)
        nav=BoxLayout(size_hint_y=None,height=dp(45),spacing=dp(8))
        nav.add_widget(self.button('⟵ Previous',lambda *_:self.prev_photo(),dp(45)))
        nav.add_widget(self.button('Next ⟶',lambda *_:self.next_photo(),dp(45)))
        box.add_widget(nav)
        box.add_widget(self.button('↻ Refresh Gallery',lambda *_:self.gallery(),dp(43)))
        box.add_widget(self.button('← Back',lambda *_:self.home(),dp(43)))
        self.sm.current='gallery'; self.render_gallery()

    def render_gallery(self):
        if not hasattr(self,'gallery_holder'): return
        self.gallery_holder.clear_widgets()
        if not self.gallery_files:
            self.gallery_holder.add_widget(Label(text='No photos found ♥\n\nAdd JPG/PNG photos to the images folder.',font_name=FONT,font_size=sp(16),color=self.text(),halign='center',valign='middle',text_size=(dp(300),None),pos_hint={'center_x':.5,'center_y':.5}))
            return
        f=self.gallery_files[self.gallery_index]; path=os.path.join(IMAGE_DIR,f)
        img=ClickableImage(source=path, allow_stretch=True, keep_ratio=True, size_hint=(.92,.78), pos_hint={'center_x':.5,'center_y':.56}, on_click=self.enlarge)
        self.gallery_holder.add_widget(img)
        self.gallery_holder.add_widget(Label(text=self.photo_name(f)+f'   ({self.gallery_index+1}/{len(self.gallery_files)})',font_name=FONT_BOLD if os.path.exists(FONT_BOLD) else FONT,font_size=sp(16),color=self.text(),size_hint=(1,None),height=dp(35),pos_hint={'center_x':.5,'y':.02}))

    def prev_photo(self):
        if self.gallery_files:
            self.gallery_index=(self.gallery_index-1)%len(self.gallery_files); self.render_gallery(); self.explode(self.gallery_holder,dp(70),dp(150),10)
    def next_photo(self):
        if self.gallery_files:
            self.gallery_index=(self.gallery_index+1)%len(self.gallery_files); self.render_gallery(); self.explode(self.gallery_holder,Window.width-dp(70),dp(150),10)
    def enlarge(self):
        if not self.gallery_files: return
        f=self.gallery_files[self.gallery_index]; path=os.path.join(IMAGE_DIR,f)
        box=FloatLayout(); img=Image(source=path,allow_stretch=True,keep_ratio=True,size_hint=(.96,.82),pos_hint={'center_x':.5,'center_y':.55}); box.add_widget(img)
        box.add_widget(Label(text=self.photo_name(f),font_name=FONT_BOLD if os.path.exists(FONT_BOLD) else FONT,font_size=sp(18),color=(1,.3,.53,1),size_hint=(1,None),height=dp(40),pos_hint={'x':0,'y':0.02}))
        p=Popup(title='',content=box,size_hint=(.94,.88),separator_color=(1,.3,.53,1),background_color=(.08,.05,.07,1)); p.open()

    def explode(self,root,x,y,amount=20):
        for _ in range(amount):
            h=Label(text=random.choice(['♥','♡']),font_name=FONT,font_size=sp(random.randint(18,28)),color=(1,.25,.52,1),size_hint=(None,None),size=(dp(30),dp(30)),pos=(x,y))
            root.add_widget(h); ang=random.uniform(0,math.pi*2); dist=random.uniform(dp(50),dp(150))
            a=Animation(x=x+math.cos(ang)*dist,y=y+math.sin(ang)*dist,opacity=0,duration=.65)
            a.bind(on_complete=lambda anim,w: root.remove_widget(w) if w.parent else None); a.start(h)

    def toggle_theme(self): self.dark=not self.dark; self.home()
    def toggle_music(self):
        path=os.path.join(MUSIC_DIR,'love.wav')
        if self.music_on:
            if self.sound: self.sound.stop()
            self.music_on=False
        elif os.path.exists(path):
            self.sound=SoundLoader.load(path)
            if self.sound:
                self.sound.loop=True; self.sound.play(); self.music_on=True
        self.home()
    def on_keyboard(self,window,key,*args):
        if key==27:
            if self.sm.current != 'opening': self.home(); return True
        return False

if __name__ == '__main__':
    OishiApp().run()
