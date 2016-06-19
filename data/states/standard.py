import pygame as pg
import string

from .. import prepare,tools
from ..components.labels import Button,ButtonGroup,Label



class CalculatorStd(tools._State):
    def __init__(self):
        super(CalculatorStd,self).__init__()
        self.mask = prepare.GFX['c1bg']
        self.init()
        self.make_buttons()
        self.make_screen()
        self.muted = False
        self.bg_color = prepare.BG_COLOR[11]

    def startup(self, persistent):
        self.persist = persistent
        self.muted = self.persist['muted']

    def init(self):
        self.display = '0'
        self.memory_number = '0'
        self.memory_operator = '+'
        self.pre_display = '0'
        self.pre_operator ='+'
        self.last_input = '0'
        self.operator = '+'

    def make_screen(self):
        self.lcd_screen = pg.sprite.Group()
        self.lcd_style ={
            'text_color':'white',
            'font_size':115,
            'font_path':prepare.FONTS['digital-7']}
        self.label = Label(self.display, {'bottomright':(470,120)}, **self.lcd_style)
        self.lcd_screen.add(self.label)

    def make_buttons(self):
        self.buttons = ButtonGroup()

        button_names = ['S', 'AC', '', '+',\
                        '1',  '2',  '3', '-',\
                        '4',  '5',  '6', '*',\
                        '7',  '8',  '9', '/',\
                        '0',  '.',  '-+', '=']

        button_bindings = [(),(),(pg.K_BACKSPACE,),(pg.K_KP_PLUS,pg.K_EQUALS),\
                           (pg.K_1,pg.K_KP1),(pg.K_2,pg.K_KP2),(pg.K_3,pg.K_KP3),(pg.K_MINUS,pg.K_KP_MINUS),\
                           (pg.K_4,pg.K_KP4),(pg.K_5,pg.K_KP5),(pg.K_6,pg.K_KP6),(pg.K_KP_MULTIPLY,pg.K_8),\
                           (pg.K_7,pg.K_KP7),(pg.K_8,pg.K_KP8),(pg.K_9,pg.K_KP9),(pg.K_SLASH,pg.K_KP_DIVIDE),\
                           (pg.K_0,pg.K_KP0),(pg.K_PERIOD,pg.K_KP_PERIOD),(),(pg.K_EQUALS,)]

        button_toplefts = [(10,140),(127,140),(245,140),(362,140),\
                           (10,240),(127,240),(245,240),(362,240),\
                           (10,340),(127,340),(245,340),(362,340),\
                           (10,440),(127,440),(245,440),(362,440),\
                           (10,540),(127,540),(245,540),(362,540)]

        button_sounds = [prepare.SFX['di'],prepare.SFX['di'],prepare.SFX['di'],prepare.SFX['add'],\
                         prepare.SFX['1'],prepare.SFX['2'],prepare.SFX['3'],prepare.SFX['sub'],\
                         prepare.SFX['4'],prepare.SFX['5'],prepare.SFX['6'],prepare.SFX['mul'],\
                         prepare.SFX['7'],prepare.SFX['8'],prepare.SFX['9'],prepare.SFX['div'],\
                         prepare.SFX['0'],prepare.SFX['point'],prepare.SFX['di'],prepare.SFX['equ']]

        for name,topleft,sound,shotcut_key in zip(button_names,button_toplefts,button_sounds,button_bindings):
            buttons = Button(topleft,self.buttons,button_size =(108,90),idle_image = prepare.GFX['image0'], \
                             hover_fill_color='gray20',click_image = prepare.GFX['image1'],click_sound = sound,\
                             bindings =shotcut_key, call=self.compute,args = name)

    def digit_input_operate(self,name):
        self.pre_operator = self.operator
        if self.display == 'Error':
            pass
        elif self.last_input in '+-*/':
            self.display = name
        elif self.last_input in string.digits:
            if self.display == '0' or self.display == '-0':
                self.display = self.display[:-1] + name
            elif len(self.display) == 8:
                pass
            else:
                self.display += name
        self.last_input = name

    def plus_minus_operate(self,name):
        self.operator = name
        if self.display == 'Error':
            pass
        elif self.last_input in string.digits:
            if self.pre_operator in '+-*/':
                try:
                    result = str(eval(self.memory_number+self.memory_operator+\
                                      self.pre_display + self.pre_operator + self.display))
                    if float(result) > 99999999 or float(result) < -9999999:
                        result = 'Error'
                    else:
                        result = result.rstrip('0') if ('.' in result and result.endswith('0')) else result
                        result = result[:8]
                        result = result[:-1] if result.endswith('.') else result
                except ZeroDivisionError:
                    result = 'Error'
                finally:
                    self.memory_number = '0'
                    self.memory_operator = '+'
                self.display = result
            self.pre_display = self.display
        self.last_input = name

    def multiply_divide_operate(self,name):
        self.operator = name
        if self.display == 'Error':
            pass
        elif self.last_input in string.digits:
            if self.pre_operator in '+-':
                self.memory_number = self.pre_display
                self.memory_operator = self.pre_operator

            elif self.pre_operator in '*/':
                try:
                    result = str(eval(self.pre_display + self.pre_operator + self.display))
                    if float(result) > 99999999 or float(result) < -9999999:
                        result = 'Error'
                    else:
                        result = result.rstrip('0') if ('.' in result and result.endswith('0')) else result
                        result = result[:8]
                        result = result[:-1] if result.endswith('.') else result
                except ZeroDivisionError:
                    result = 'Error'
                self.display = result
            self.pre_display = self.display
        self.last_input = name

    def negtive_operate(self,name):
        if self.display == 'Error':
            pass

        elif self.last_input in string.digits:
            if self.display.startswith('-'):
                self.display = self.display[1:]
            else:
                self.display = ('-'+ self.display)[:8]
        elif self.last_input in '+-*/':
            self.display = '-0'
        self.last_input = '0'

    def equal_operate(self,name):
        if self.display == 'Error':
            pass
        else:
            try:
                
                result = str(eval(self.memory_number + self.memory_operator + \
                                  self.pre_display + self.pre_operator + self.display))

                if float(result) > 99999999 or float(result) < -9999999:
                    result = 'Error'
                else:
                    result = result.rstrip('0') if ('.' in result and result.endswith('0')) else result
                    result = result[:8]
                    result = result[:-1] if result.endswith('.') else result
            except ZeroDivisionError:
                result = 'Error'
            finally:
                self.memory_number = '0'
                self.memory_operator = '+'
            self.init()
            self.display = result
        

    def compute(self,name):
        if name == 'S':
            self.done = True
            self.next = 'PROGRAMMER'
            self.persist['muted'] = self.muted

        elif name == 'AC':
            self.init()

        elif name == '':
            if self.display == 'Error':
                pass
            elif len(self.display)== 1:
                self.display = '0'
            elif len(self.display)>1:
                self.display = self.display[:-1]

        elif name in string.digits:
            self.digit_input_operate(name)

        elif name in '+-':
            self.plus_minus_operate(name)

        elif name in '*/':
            self.multiply_divide_operate(name)

        elif name in '-+':
            self.negtive_operate(name)

        elif name in '.':
            self.last_input = '0'
            if self.display == 'Error':
                pass
            elif '.' in self.display:
                pass
            elif '.' not in self.display:
                if len(self.display) == 8:
                    pass
                else:
                    self.display += '.'

        elif name == '=':
            self.equal_operate(name)


    def get_event(self,event):
        mods = pg.key.get_mods()
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key in (pg.K_RETURN,pg.K_KP_ENTER):
                self.compute('=')
            elif event.key == pg.K_DELETE:
                self.compute('AC')
            if mods&pg.KMOD_ALT:
                if event.key == pg.K_m:
                    self.muted = not self.muted
                if event.key == pg.K_s:
                    self.done = True
                    self.next = 'PROGRAMMER'
                    self.persist['muted'] = self.muted
                    
        elif event.type == pg.MOUSEBUTTONDOWN:
            pass




        self.buttons.get_event(event)



    def update(self,dt):
        mouse_pos = pg.mouse.get_pos()
        self.buttons.update(mouse_pos)
        self.display = self.display if len(self.display) <= 8 else 'Error'
        self.lcd_screen.update(self.display)
        if self.muted:
            pg.mixer.stop()


    def draw_lattice(self,surface):
        pg.draw.rect(surface, 0xbfbfbf, (0, 0, 480, 10))
        pg.draw.rect(surface, 0xbfbfbf, (0, 0, 10, 640))
        pg.draw.rect(surface, 0xbfbfbf, (470, 0, 10, 640))
        for i in range(6):
            pg.draw.rect(surface,0xbfbfbf,(0,630-i*100,480,10))
        pg.draw.rect(surface, 0xbfbfbf, (118, 130, 9, 500))
        pg.draw.rect(surface, 0xbfbfbf, (235, 130, 10,500))
        pg.draw.rect(surface, 0xbfbfbf, (353, 130, 9, 500))


    def draw(self,surface):
        surface.fill(self.bg_color)
        self.lcd_screen.draw(surface)
        self.draw_lattice(surface)

        self.buttons.draw(surface)
        surface.blit(self.mask,(0,0))


