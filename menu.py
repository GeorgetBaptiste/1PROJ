import PIL.Image, PIL.ImageTk
from tkinter import Tk, Button, Canvas, Label, NORMAL, DISABLED
from game import Game
from themes import Themes
import os
from playsound import playsound
import AppKit
import threading
import time

class Menu: 
    
    def __init__(self):
        
        #--------------------------------------------------------------------------------------------------------------------#
        # Fenêtre Tkinter #
        if os.name == "posix": # Macos, Linux
            self.__screen = (round(AppKit.NSScreen.screens()[0].frame().size.width), round(AppKit.NSScreen.screens()[0].frame().size.height))
        else: # Inconnu
            self.__screen = (1920, 1080)
        self.__root = Tk(className = " Kamon")
        self.__root.attributes('-fullscreen', True)
        self.__root.geometry(str(self.__screen[0])+"x"+str(self.__screen[1]))
        self.__root.resizable(False, False)
        self.__loop = threading.Thread(target=self.loop, daemon=True)
        self.__loop.start()
        #--------------------------------------------------------------------------------------------------------------------#
        # Thèmes
        self.__theme_astro = Themes().get_themes()[0]
        self.__theme_imaginary = Themes().get_themes()[1]
        self.__theme_classique = Themes().get_themes()[2]
        self.__theme_actuel = self.__theme_classique
        #--------------------------------------------------------------------------------------------------------------------#
        # L'objet représentant une partie
        self.__game = None
        self.__mode = None
        #--------------------------------------------------------------------------------------------------------------------#
        # Paramètrage des widget et du board
        self.__hlt_widget = 0
        self.__hlb_widget = "black"
        self.__hlc_widget = "white"
        self.__fg_widget = "black"
        self.__bg_widget = "white"
        self.__board_color_outline = "black"
        self.__board_color = "#555"
        self.__board_hlc = "yellow"
        self.__board_border = round(5*self.__screen[0]/self.__screen[0])
        self.__font_helvetica_24_bold = ("Helvetica", 24, "bold")
        self.__font_courier_120_bold = ("Courier", 120, "bold")
        self.__font_courier_70_bold = ("Courier", 70, "bold")
        self.__width_50_px = round(50*self.__screen[0]/self.__screen[0])
        self.__height_50_px = round(50*self.__screen[0]/self.__screen[0])
        self.__height_2 = round(2*self.__screen[0]/self.__screen[0])
        self.__width_20 = round(20*self.__screen[0]/self.__screen[0])
        self.__anchor = "center"
        self.__win_screen_outline_color = "yellow"
        self.__win_screen_color = "black"
        self.__win_screen_text_color = "white"
        self.__mult_rayon = self.__screen[0]/self.__screen[0]
        #--------------------------------------------------------------------------------------------------------------------#
        # Les emplacements des widgets
        self.__canvas_p = [self.__screen[0]*50/100, self.__screen[1]*50/100]
        self.__item_logo_p = [self.__screen[0]*50/100, self.__screen[1]*20/100]
        self.__button_player_vs_player_p = [self.__screen[0]*50/100, self.__screen[1]*50/100]
        self.__button_player_vs_ordi_p = [self.__screen[0]*50/100, self.__screen[1]*60/100]
        self.__button_quit_kamon_p = [self.__screen[0]*50/100, self.__screen[1]*70/100]
        self.__button_settings_p = [self.__screen[0]*90/100, self.__screen[1]*10/100]
        self.__button_back_p = [self.__screen[0]*10/100, self.__screen[1]*10/100]
        self.__button_break_p = [self.__screen[0]*90/100, self.__screen[1]*10/100]
        self.__button_resume_p = [self.__screen[0]*50/100, self.__screen[1]*50/100]
        self.__button_restart_p = [self.__screen[0]*50/100, self.__screen[1]*60/100]
        self.__button_quit_game_p = [self.__screen[0]*50/100, self.__screen[1]*70/100]
        self.__button_small_board_p = [self.__screen[0]*50/100, self.__screen[1]*50/100]
        self.__button_medium_board_p = [self.__screen[0]*50/100, self.__screen[1]*60/100]
        self.__button_large_board_p = [self.__screen[0]*50/100, self.__screen[1]*70/100]
        self.__button_theme_astro_p = [self.__screen[0]*50/100, self.__screen[1]*50/100]
        self.__button_theme_imaginary_p = [self.__screen[0]*50/100, self.__screen[1]*60/100]
        self.__button_theme_classique_p = [self.__screen[0]*50/100, self.__screen[1]*70/100]
        self.__item_title_break_p = [self.__screen[0]*50/100, self.__screen[1]*20/100]
        self.__item_title_settings_p = [self.__screen[0]*50/100, self.__screen[1]*20/100]
        self.__item_title_board_size_p = [self.__screen[0]*50/100, self.__screen[1]*20/100]
        #--------------------------------------------------------------------------------------------------------------------#
        # Les widgets
        self.__canvas = Canvas(self.__root, width=self.__screen[0], height=self.__screen[1], highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_player_vs_player = Button(self.__root, text='Play', command=lambda: [self.change_display(self.__page_board_size), self.set_mode("player")], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_player_vs_ordi = Button(self.__root, text='Play IA', command=lambda: [self.change_display(self.__page_board_size), self.set_mode("ordi")], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_quit_kamon = Button(self.__root, text='Quit Kamon', command=lambda: [self.__root.destroy()], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_settings = Button(self.__root, bitmap=Themes().get_logo()[1], command=lambda: self.change_display(self.__page_settings), font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_50_px, width=self.__width_50_px, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_back = Button(self.__root, bitmap=Themes().get_logo()[3], command=lambda: self.change_display(self.__page_back), font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_50_px, width=self.__width_50_px, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_break = Button(self.__root, bitmap=Themes().get_logo()[2], command=lambda: [self.change_display(self.__page_break), self.__game.set_pause(True)], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_50_px, width=self.__width_50_px, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_resume = Button(self.__root, text='Resume', command=lambda: [self.change_display(self.__page_game), self.__game.set_pause(False), self.__game.display_board()], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_restart = Button(self.__root, text='Restart', command=lambda: [self.change_display(self.__page_game), self.start_game(self.__game.get_board_size(), self.__game.get_rayon(), self.__board_border, self.__mode), self.change_state(NORMAL)], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_quit_game = Button(self.__root, text='Quit', command=lambda: [self.change_display(self.__page_accueil), self.change_state(NORMAL)], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_small_board = Button(self.__root, text='Small', command=lambda: [self.change_display(self.__page_game), self.start_game(37, self.__mult_rayon*65, 5, self.__mode)], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_medium_board = Button(self.__root, text='Medium', command=lambda: [self.change_display(self.__page_game), self.start_game(61, self.__mult_rayon*50, 4, self.__mode)], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_large_board = Button(self.__root, text='Large', command=lambda: [self.change_display(self.__page_game), self.start_game(91, self.__mult_rayon*40, 3, self.__mode)], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_theme_astro = Button(self.__root, text='Astro theme', command=lambda: [self.change_theme(self.__theme_astro)], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_theme_imaginary = Button(self.__root, text='Imaginary theme', command=lambda: [self.change_theme(self.__theme_imaginary)], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__button_theme_classique = Button(self.__root, text='Default theme', command=lambda: [self.change_theme(self.__theme_classique)], font=self.__font_helvetica_24_bold, fg=self.__fg_widget, bg=self.__bg_widget, height=self.__height_2, width=self.__width_20, highlightthickness=self.__hlt_widget, highlightbackground=self.__hlb_widget, highlightcolor=self.__hlc_widget)
        self.__canvas.place(x=self.__canvas_p[0], y=self.__canvas_p[1], anchor=self.__anchor)
        #--------------------------------------------------------------------------------------------------------------------#
        # Les items
        self.__item_logo = None
        self.__item_title_board_size = None
        self.__item_title_break = None
        self.__item_title_settings = None
        self.__item_bg = self.__canvas.create_image(self.__canvas_p[0], self.__canvas_p[1], image = self.image(self.__theme_actuel["bg"], self.__screen[0], self.__screen[1]), anchor= self.__anchor)
        #--------------------------------------------------------------------------------------------------------------------#
        # Les pages
        self.__page_accueil = [[self.__button_player_vs_player, self.__button_player_vs_ordi, self.__button_settings, self.__button_quit_kamon], [self.__button_player_vs_player_p, self.__button_player_vs_ordi_p, self.__button_settings_p, self.__button_quit_kamon_p]]
        self.__page_settings = [[self.__button_back, self.__button_theme_astro, self.__button_theme_classique, self.__button_theme_imaginary], [self.__button_back_p, self.__button_theme_astro_p, self.__button_theme_classique_p, self.__button_theme_imaginary_p]]
        self.__page_board_size = [[self.__button_back, self.__button_small_board, self.__button_medium_board, self.__button_large_board], [self.__button_back_p, self.__button_small_board_p, self.__button_medium_board_p, self.__button_large_board_p]]
        self.__page_game = [[self.__button_break], [self.__button_break_p]]
        self.__page_break = [[self.__button_restart, self.__button_quit_game, self.__button_resume], [self.__button_restart_p, self.__button_quit_game_p, self.__button_resume_p]]
        self.__page_actuel = None
        self.__page_back = None
        #--------------------------------------------------------------------------------------------------------------------#
        # Fonction de lancement
        self.change_display(self.__page_accueil)
        self.__root.mainloop()
        #--------------------------------------------------------------------------------------------------------------------#

    def image(self, image, width, height):
        image = PIL.Image.open(image)
        image = image.resize((width, height), PIL.Image.ANTIALIAS)
        image = PIL.ImageTk.PhotoImage(image)
        label = Label(self.__root, image=image)
        label.img=image
        return image
    
    def set_mode(self, mode):
        self.__mode = mode
    
    def change_display(self, page):
        if self.__page_actuel != None:
            for i in range(len(self.__page_actuel[0])):
                self.__page_actuel[0][i].place_forget()
        for i in range(len(page[0])):
            page[0][i].place(x=page[1][i][0], y=page[1][i][1], anchor=self.__anchor)
        if page == self.__page_accueil:
            self.__item_logo = self.__canvas.create_image(self.__item_logo_p[0], self.__item_logo_p[1], anchor=self.__anchor, image=self.image(Themes().get_logo()[0], round(700*self.__screen[0]/self.__screen[0]), round(180*self.__screen[0]/self.__screen[0])))
        if page != self.__page_accueil:
            self.__canvas.delete(self.__item_logo)
        if page == self.__page_break:
            self.__item_title_break = self.__canvas.create_text(self.__item_title_break_p[0], self.__item_title_break_p[1], text="Break", font=self.__font_courier_120_bold, fill=self.__fg_widget)
        if page != self.__page_break:
            self.__canvas.delete(self.__item_title_break)
        if page == self.__page_settings:
            self.__item_title_settings = self.__canvas.create_text(self.__item_title_settings_p[0], self.__item_title_settings_p[1], text="Settings", font=self.__font_courier_120_bold, fill=self.__fg_widget)
        if page != self.__page_settings:
            self.__canvas.delete(self.__item_title_settings)
        if page == self.__page_board_size:
            self.__item_title_board_size = self.__canvas.create_text(self.__item_title_board_size_p[0], self.__item_title_board_size_p[1], text="Boards", font=self.__font_courier_120_bold, fill=self.__fg_widget)
        if page != self.__page_board_size:
            self.__canvas.delete(self.__item_title_board_size)
        if page != self.__page_game and self.__game != None:
            for value in self.__game.get_dic_item().values():
                self.__canvas.delete(value)
        self.__page_back = self.__page_actuel
        self.__page_actuel = page
        self.__root.update()
                 
    def start_game(self, board_size, rayon, board_border, mode):
        self.__board_border = board_border
        self.__game = Game(self.__theme_actuel, self.image, self.__canvas, self.__canvas_p, board_size, rayon, self.__board_color_outline, self.__board_color, self.__board_border, self.__board_hlc, self.__screen, self.__win_screen_outline_color, self.__win_screen_color, self.__win_screen_text_color, self.__font_courier_70_bold, mode, self.change_state)
    
    def change_theme(self, theme):
        if theme == self.__theme_astro:
            self.__fg_widget = "white"
        else:
            self.__fg_widget = "black"
        self.__canvas.delete(self.__item_bg, self.__item_title_settings)
        self.__item_bg = self.__canvas.create_image(self.__canvas_p[0], self.__canvas_p[1], image = self.image(theme["bg"], self.__screen[0], self.__screen[1]), anchor= self.__anchor)
        self.__item_title_settings = self.__canvas.create_text(self.__item_title_settings_p[0], self.__item_title_settings_p[1], text="Settings", font=self.__font_courier_120_bold, fill=self.__fg_widget)
        self.__theme_actuel = theme
        
    def change_state(self, state):
            self.__page_break[0][2]["state"] = state
            
    def start_music(self):
        self.__thread = threading.Thread(target=playsound, args=["assets/music/anime_music.mp3"], daemon=True)
        self.__thread.start()
        
    def loop(self):
        self.start_music()
        while True:
            if self.__thread.is_alive() == False:
                self.start_music()
            time.sleep(2)
        
Menu()