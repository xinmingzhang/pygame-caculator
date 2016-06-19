import pygame as pg
from math import e,pi,degrees,radians,exp,log,log10,factorial,sin,cos,tan,asin,acos,atan,sinh,cosh,tanh,\
    asinh,acosh,atanh,sqrt
import string

from .. import prepare,tools
from ..components.labels import Button,ButtonGroup,MultiLineLabel,Label

def ln(x):
    return log(x,e)

class CalculatorPro(tools._State):
    def __init__(self):
        super(CalculatorPro,self).__init__()
        self.mask = prepare.GFX['c2bg']
        self.bg_color = prepare.BG_COLOR[41]
        self.display = 'Please enter the expression'
        self.memory = '>>>'
        self.right_parenthesis = 0
        self.make_buttons()
        self.make_input_screen()
        self.make_result_screen()

        

    def startup(self, persist):
        self.persist = persist
        self.muted = self.persist['muted']

    def make_input_screen(self):
        self.memory_display = MultiLineLabel(prepare.FONTS['UbuntuMono-B'],30,self.memory,\
                                    'white',{'bottomleft':(15,200)},None,30,'left',0)
        
    def make_result_screen(self):
        self.lcd_screen = pg.sprite.Group()
        self.lcd_style ={
            'text_color':'white',
            'font_size':30,
            'font_path':prepare.FONTS['Ubuntu-L']}
        self.label = Label(self.display, {'bottomright':(467,230)}, **self.lcd_style)
        self.lcd_screen.add(self.label)

    def make_buttons(self):
        self.buttons = ButtonGroup()

        button_toplefts =[(10+x*58,243+y*49) for x in range(8) for y in range(8)]
        button_toplefts.remove((416, 586))
        button_toplefts.remove((416, 537))
        button_toplefts.remove((10, 243))
        button_toplefts.remove((68, 243))

        button_names = ['e','sin(','asin(','a','&','1','6','pi','sinh(','asinh(','b','|','2','7',\
                        'ce','log10(','cos(','acos(','c','^','3','8','.','ln(','cosh(','acosh(','d',
                        '~','4','9','%','10**','tan(','atan(','e','<<','5','0','//','e**','tanh(',
                        'atanh(','f','>>','+','-',"(",'**','sqrt(','degrees(','dec','0o','*','/',")",
                        'factorial(','**2','radians','0b','0x']

        button_sounds = [prepare.SFX['c2'],prepare.SFX['c2m'],prepare.SFX['d2'],prepare.SFX['d2m'],\
                         prepare.SFX['e2'],prepare.SFX['f2'],prepare.SFX['f2m'],prepare.SFX['g2'],\
                         prepare.SFX['g2m'],prepare.SFX['a2'],prepare.SFX['a2m'],prepare.SFX['b2'], \
                         prepare.SFX['c3'], prepare.SFX['c3m'], prepare.SFX['d3'], prepare.SFX['d3m'],\
                         prepare.SFX['e3'], prepare.SFX['f3'], prepare.SFX['f3m'], prepare.SFX['g3'],\
                         prepare.SFX['g3m'], prepare.SFX['a3'], prepare.SFX['a3m'], prepare.SFX['b3'],\
                         prepare.SFX['c4'],prepare.SFX['c4m'],prepare.SFX['d4'],prepare.SFX['d4m'],\
                         prepare.SFX['e4'],prepare.SFX['f4'],prepare.SFX['f4m'],prepare.SFX['g4'],\
                         prepare.SFX['g4m'],prepare.SFX['a4'],prepare.SFX['a4m'],prepare.SFX['b4'],\
                         prepare.SFX['c5'],prepare.SFX['c5m'],prepare.SFX['d5'],prepare.SFX['d5m'],\
                         prepare.SFX['e5'],prepare.SFX['f5'],prepare.SFX['f5m'],prepare.SFX['g5'],\
                         prepare.SFX['g5m'],prepare.SFX['a5'],prepare.SFX['a5m'],prepare.SFX['b5'], \
                         prepare.SFX['c6'], prepare.SFX['c6m'], prepare.SFX['d6'], prepare.SFX['d6m'],\
                         prepare.SFX['e6'], prepare.SFX['f6'], prepare.SFX['f6m'], prepare.SFX['g6'],\
                         prepare.SFX['g6m'], prepare.SFX['a6'], prepare.SFX['a6m'], prepare.SFX['b6']]

        for name,topleft,sound in zip(button_names,button_toplefts,button_sounds):
            buttons = Button(topleft,self.buttons,button_size =(54,45),idle_image = prepare.GFX['image2'], \
                             hover_fill_color='darkgoldenrod4',click_image = prepare.GFX['image3'],\
                             click_sound = sound,call=self.input,args = name)

        Button((416, 537),self.buttons,button_size =(54,94),idle_image = prepare.GFX['image4'], \
               hover_fill_color='chocolate4',click_image = prepare.GFX['image5'],call = self.compute,args = None)

        Button((10, 243), self.buttons, button_size=(54, 45), idle_image=prepare.GFX['image2'], \
               hover_fill_color='tomato4', click_image=prepare.GFX['image3'],call = self.input,args = 'S')

        Button((68, 243), self.buttons, button_size=(54, 45), idle_image=prepare.GFX['image2'], \
               hover_fill_color='darkorange4', click_image=prepare.GFX['image3'],call = self.input,args = 'ac')



    def input(self,name):
        if name == 'S':
            self.done = True
            self.next = 'STANDARD'
            self.persist['muted'] = self.muted
        elif name == 'ac':
            self.display = 'Please enter the expression'
            self.memory = '>>>'
            self.right_parenthesis = 0
        elif name == 'ce':
            if len(self.memory) == 3 and self.memory[:3] == '>>>':
                pass
            elif self.memory[-1]==')':
                self.right_parenthesis += 1
                self.display = 'NOTICE: '+str(self.right_parenthesis)+ ' ) needed'
                self.memory = self.memory[:-1]
            elif self.memory[-1]== '(':
                self.right_parenthesis -= 1
                if self.right_parenthesis == 0:
                    self.display = 'Please enter the expression'
                else:
                    self.display = 'NOTICE: '+str(self.right_parenthesis)+ ' ) needed'
                self.memory = self.memory[:-1]
            else:
                self.memory = self.memory[:-1]

        elif name == 'dec':
            pass
        elif len(self.memory + name) <= 180:
            self.memory += name
            if name in ('sin(','asin(','sinh(','asinh(','log10(','cos(','acos(','ln(','cosh(','acosh(',\
                        'tan(','atan(','tanh(','atanh(',"(",'sqrt(','degrees(','factorial('):
                self.right_parenthesis += 1
                self.display = 'NOTICE: '+str(self.right_parenthesis)+ ' ) needed'
            if name == ')':
                self.right_parenthesis -= 1
                if self.right_parenthesis == 0:
                    self.display = 'Please enter the expression'
                else:
                    self.display = 'NOTICE: '+str(self.right_parenthesis)+ ' ) needed'
        else:
            pass

    def compute(self,args):
        if len(self.memory)>3:
            try:
                result = str(eval(self.memory[3:]))
                self.display = '='+ result[:26]
            except Exception as result:
                self.display = 'Error'
        else:
            pass

    def get_event(self,event):
        mods = pg.key.get_mods()
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if mods&pg.KMOD_ALT:
                if event.key == pg.K_m:
                    self.muted = not self.muted
                if event.key == pg.K_s:
                    self.done = True
                    self.next = 'STANDARD'
                    self.persist['muted'] = self.muted
        self.buttons.get_event(event)            



    def draw_lattice(self,surface):
        pg.draw.rect(surface, 0xbfbfbf, (0, 0, 480, 10))
        pg.draw.rect(surface, 0xbfbfbf, (0, 0, 10, 640))
        pg.draw.rect(surface, 0xbfbfbf, (470, 0, 10, 640))
        pg.draw.rect(surface, 0xbfbfbf, (0, 630, 480, 10))
        pg.draw.rect(surface, 0xbfbfbf, (0, 233, 480, 10))


    def draw(self,surface):
        surface.fill(self.bg_color)
        self.draw_lattice(surface)
        self.buttons.draw(surface)
        surface.blit(self.mask, (0, 0))
        self.memory_display.draw(surface)
        self.lcd_screen.draw(surface)


    def update(self,dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        self.make_input_screen()
        self.lcd_screen.update(self.display)
        if self.muted:
            pg.mixer.stop()

