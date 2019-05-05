from tkinter import *
import tkinter as tk
from tkinter import ttk # treba nam za lepsi izgled, trenutno koristimo samo kod ***da bi dugmici uvek bili iste velicine pri promeni igraca(PLAVI ZUTI)
import os #**
import random
import time
from tkinter.font import Font
from pathlib import Path #treba nam za putanje za ucitavanje slika, kao i **
from tkinter import messagebox
from PIL import ImageTk,Image

#--KADA UDJEMO U 1vs1 i brzo kliknemo na 3 kartice--treba vrv uraditi neki disable dugmica
#Treba dodati da izabrane kartice stv budu kartice (a ne bele slike)
#8x8 i 16x16- nemamo dovoljno kartica
#dodati mozda u menubar nesto kao zapocni novu igru?


#globalne promenljive
comp_steps = 0
count=0
pom_i=-1
pom_j=-1
player = 1 #redni broj igraca 
points_b = 0 #poeni PLAVOG igraca
points_y = 0 #poeni ZUTOG igraca
nonmatched = [] #lista kartica koje nisu match-ovane ili osvojene
#sledeca dva para koristimo kod 1 vs rac
pair1 = (-1,-1) 
pair2 = (-1,-1)
done = 0
opened = [] #pamtimo sve kartice koje smo otvorili do nekog trenutka(treba nam za igranje racunara)

class MatrixOfButtons:
    #master je root
    def __init__(self,master,f_start,var1,var2,var3):
        #self=root a frame=f_one_player
        #valjda je master root?
        f_start.grid_forget()

        self.frame = Frame(master)
        self.frame.grid(row=1, column=1,sticky="nsew")
        self.n = var3.get()
        self.level = var2.get()
        #formiramo listu nonmatched:
        global nonmatched
        for i in range(0,self.n):
            for j in range(0,self.n):
                nonmatched.append((i,j)) 

        self.b=[[0 for x in range(0,self.n)] for x in range(0,self.n)] #matrica dugmica
        self.photo_matrix=[[0 for x in range(0,self.n)] for x in range(0,self.n)] #matrica slika

        photo_list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34] #broj slika
        list_pair=[] #lista parova=koordinate u matrici (i,j)
        
        for i in range(0,self.n):
            for j in range(0,self.n):
                list_pair.append((i,j))
                self.photo_matrix[i][j]=" " 

        while list_pair!=[]:
            broj_slike=random.choice(photo_list)
            photo_list.remove(broj_slike)
            
            pair=random.choice(list_pair)
            list_pair.remove(pair)
            pair1=random.choice(list_pair)
            list_pair.remove(pair1)

            #na poziciji (i,j) cuvamo naziv slike
            path = os.path.join(Path().absolute(),"slike3/"+str(broj_slike)+".gif")
            self.photo_matrix[pair[0]][pair[1]]=path
            self.photo_matrix[pair1[0]][pair1[1]]=path
                

            if self.n == 4:
                w = 800
                h = 600
            elif self.n == 6:
                w = 1000
                h = 800
            else:
                w = 1200
                h = 1000

            
            canvas = Canvas(self.frame,width= w,height =h,background = 'turquoise')
            
            canvas.grid(column =1,row=1)
            
            myFont = Font(family="Courier", size=14)
            myFontBtn = Font(family="Courier", size=12)
                
                
            x = 200
            y = 150
            for i in range(0,self.n):
                x = 200
                for j in range(0,self.n):
                
                    path = os.path.join(Path().absolute(),"slike3/blank.gif")
                    photo=PhotoImage(file=path)#slika kartica
                    self.b[i][j] = tk.Button(canvas,image=photo,bg='LightCyan2',fg='navy',command=lambda x1=i, y1=j,n=self.n,frame=self.frame,card_photo=photo,f_start=
                                          f_start,var1=var1,var2=var2,var3=var3: self.funkcija(x1,y1,n,frame,card_photo,f_start,var1,var2,var3)) #***
                    self.b[i][j].image=photo #*
                    canvas.create_window(x,y,
                                        window=self.b[i][j])
                    x += 100
                y+=100
            #stavljamo na frame labele koje smo gore definisali 
            self.lbl = tk.Label(canvas,text="\tIgra  ZUTI igrac",bg='LightCyan2',font=myFont) #prvi na potezu je ZUTI igrac
            canvas.create_window(50,y+25,
                                        window=self.lbl)
            self.points_yellow = tk.Label(canvas,text = "Zuti: 0",bg='LightCyan2',font=myFont) #labela za bodove ZUTOG igraca
            canvas.create_window(50,50,
                                        window=self.points_yellow)
            self.points_blue = tk.Label(canvas,text = "Plavi: 0",bg='LightCyan2',font=myFont) #labela za bodove PLAVOG igraca
            canvas.create_window(x+75,50,
                                        window=self.points_blue)

    def funkcija(self,i,j,n,frame,card_photo,f_start,var1,var2,var3):
                global pom_i,pom_j
                global player
                global points_b,points_y
                global nonmatched,opened
                global done
                pathf = os.path.join(Path().absolute(),"slike3/zuti.gif")
                paths = os.path.join(Path().absolute(),"slike3/plavi.gif")
                photo_first = PhotoImage(file=pathf)
                photo_second = PhotoImage(file=paths)

                def open_card(self,i,j): #prikazuje sta se nalazi na kartici

                    global opened
                    photo=PhotoImage(file=self.photo_matrix[i][j])
                    self.b[i][j].config(image=photo)
                    #moramo ponovo da postavimo sliku zbog sakupljaca otpadaka, jer ga on pokupi u suprotnom*
                    self.b[i][j].image=photo
                    if (i,j) not in opened:
                        opened.append((i,j)) # dodajemo u listu karticu koju smo otvorili, ako ona nije vec u njemu

                def open_random_cards(self): #prikazuje random izabrane kartice (2 kartice)
                    global nonmatched
                    global pair1,pair2
                    
                    #biramo 2 para iz liste neosvojenih(=nonmatched) kartica
                    pair1 = random.choice(nonmatched)
                    (i1,j1) = pair1
                    open_card(self,i1,j1)
                    nonmatched.remove(pair1) #sklonili smo ovaj pair1 da bi nam pair2 bio razliciti od pair1, posle cemo ga vratiti

                    pair2 = random.choice(nonmatched)
                    (i2,j2) = pair2
                    frame.after(500, lambda: open_card(self,i2,j2))
                    nonmatched.append(pair1) #vracamo pair1 u nonmatched listu
                
                def open_random_card(self): #prikazuje random izabranu karticu (1 kartica) i onda trazi njenu istu u opened
                    global opened,nonmatched
                    global pair1,pair2
                    
                    pair1 = random.choice(nonmatched)
                    (i1,j1) = pair1
                    open_card(self,i1,j1)
                    
                    opened.remove(pair1) #sklanjamo par pair1 iz opened da bismo videli da li postoji jos neki par sa istom slikom
                    if find_same(self,pair1):
                        (i2,j2) = pair2
                        frame.after(500, lambda: open_card(self,i2,j2))
                    else:
                        nonmatched.remove(pair1)
                        pair2 = random.choice(nonmatched)
                        (i2,j2) = pair2
                        frame.after(500, lambda: open_card(self,i2,j2))
                        nonmatched.append(pair1)
                    opened.append(pair1)

                def conditions():
                    if (self.level == 1 and self.n ==4 and comp_steps%4==0) or (self.level == 1 and self.n ==6 and comp_steps%6==0) or (self.level == 1 and self.n ==8 and comp_steps%8==0):
                        return True
                    elif (self.level == 2 and self.n ==4 and comp_steps%3==0) or (self.level == 2 and self.n ==6 and comp_steps%4==0) or (self.level == 2 and self.n ==8 and comp_steps%5==0):
                        return True
                    elif (self.level == 3 and self.n ==4) or (self.level == 3 and self.n ==6 and comp_steps%2==0) or (self.level == 3 and self.n ==8 and comp_steps%2==0):
                        return True
                    return False
                def find_same(self,pair):
                    global pair2
                    global opened

                    (i1,j1)=pair
                    for (i,j) in opened:
                        if self.photo_matrix[i1][j1] == self.photo_matrix[i][j]:
                            pair2 = (i,j)
                            return True
                    return False
            

                def open_same_cards_in_opened(self):
                    global opened
                    global pair1,pair2
                    
                
                    for pair in opened:
                        opened.remove(pair) #sklanjamo par pair iz opened da bismo videli da li postoji jos neki par sa istom slikom
                        if find_same(self,pair):
                            pair1 = pair
                            (i1,j1) = pair1
                            open_card(self,i1,j1)
                            (i2,j2) = pair2
                            frame.after(500, lambda: open_card(self,i2,j2))
                            return
                        opened.append(pair)
                    open_random_card(self) #ako nije nasao 2 iste u opened,onda otvara dalje po "randomu"

            
                def change(photo,i,j):
                    global pom_i,pom_j
                    self.b[i][j].config(image=photo)
                    self.b[i][j].image=photo
                    self.b[pom_i][pom_j].config(image=photo)
                    self.b[pom_i][pom_j].image=photo
                    pom_i = -1
                    pom_j = -1
                    # vracamo pom_i i pom_j na -1 da nam ne bi doslo do greske pri neparnim koracima
                def change_random_cards(photo,pair1,pair2) :
                    (i1,j1) = pair1
                    (i2,j2) = pair2
                    self.b[i1][j1].config(image=photo)
                    self.b[i1][j1].image=photo
                    self.b[i2][j2].config(image=photo)
                    self.b[i2][j2].image=photo
                def change_of_player(self,boja):
                    self.lbl.configure(text= "\tIgra " + boja + " igrac!")

                def computer_playing(self,frame,photo_second,card_photo):
                    global nonmatched,opened,comp_steps
                    global player
                    global points_b
                    global pair1,pair2
                    global done #sluzi nam da ne ispisemo 2x ko je pobednik na f_end
                    disable_buttons(self,n)
                    comp_steps += 1
                            
                    if len(nonmatched) is 0 : 
                        frame.after(1200,lambda : winner(points_b,points_y,frame))
                        done = 1
                        return False

                        
                    if conditions():
                        open_same_cards_in_opened(self)
                    else:
                        open_random_cards(self)
                    (i1,j1) = pair1
                    (i2,j2) = pair2
                    if self.photo_matrix[i1][j1]==self.photo_matrix[i2][j2]:
                        nonmatched.remove(pair1)
                        nonmatched.remove(pair2)
                        if pair1 in opened:
                            opened.remove(pair1)
                        if pair2 in opened:
                            opened.remove(pair2)
                        points_b += 1
                        self.points_blue.configure(text = 'Plavi: ' + str(points_b))
                        frame.after(800,lambda: change_random_cards(photo_second,pair1,pair2))
                        frame.after(1200,lambda: computer_playing(self,frame,photo_second,card_photo))
                    else:
                        player = 1
                        frame.after(950, lambda: enable_buttons(self,n))                 
                        frame.after(900, lambda: change_random_cards(card_photo,pair1,pair2))
                        frame.after(700, lambda: change_of_player(self,"ZUTI "))
                    

                def defaults(): #vracamo sve globalne promenljiive na njihov default
                    global count
                    global pom_i,pom_j
                    global player
                    global points_b,points_y
                    global nonmatched,opened,comp_steps
                    global pair1,pair2
                    global done
                    
                    f_start.rb1.deselect()
                    f_start.rb2.deselect()
                    f_start.rb3.deselect()
                    f_start.rb4.deselect()
                    f_start.rb5.deselect()
                    f_start.rb6.deselect()
                    f_start.rb7.deselect()
                    f_start.rb8.deselect()
                    
                    count=0
                    pom_i=-1
                    pom_j=-1
                    player = 1 #redni broj igraca 
                    points_b = 0 #poeni PLAVOG igraca
                    points_y = 0 #poeni ZUTOG igraca
                    nonmatched = [] #lista kartica koje nisu match-ovane ili osvojene
                    #sledeca dva para koristimo kod 1 vs rac
                    pair1 = (-1,-1) 
                    pair2 = (-1,-1)
                    done = 0
                    opened = []
                    comp_steps = 0
                    
                def disable_buttons(self,n):
                    for i in range(0,n):
                        for j in range(0,n):
                            self.b[i][j].configure(state=DISABLED)
                def enable_buttons(self,n):
                    for i in range(0,n):
                        for j in range(0,n):
                            self.b[i][j].configure(state=NORMAL)
                    
                def winner(points_b,points_y,frame):
                    def popup(text): #novi prozor u kom pitamo da li igrac zeli ponovo da igra ili da izadje iz igrice
                        msg=messagebox.askyesno("Qustion",text)
                        if msg==True:
                            frame.grid_forget()
                            defaults()
                            f_start.rb1.configure(variable=var1, value=1)
                            f_start.rb2.configure(variable=var1, value=2)
                            f_start.rb3.configure(variable=var2, value=1)
                            f_start.rb4.configure(variable=var2, value=2)
                            f_start.rb5.configure(variable=var2, value=3)
                            f_start.rb6.configure(variable=var3, value=4)
                            f_start.rb7.configure(variable=var3, value=6)
                            f_start.rb8.configure(variable=var3, value=8)
                            MainGUI(root,var1,var2,var3)
                        else:
                            exit()
                    if points_y > points_b:
                        popup("Pobedio je ZUTI Igrac!\nIgraj ponovo?")
                    elif points_y < points_b:
                        popup("Pobedio je PLAVI Igrac!\nIgraj ponovo?")
                    else:
                        popup("Nereseno\nIgraj ponovo?")

                # zapravo program, posle gomile fja :D
                if (pom_i!=i or pom_j!=j) and ((i,j) in nonmatched): #da ne bi nastao problem ako neko klikne dva puta na isto dugmei ne mozemo ponovo otvarati osvojene kartice

                    global count
                    count += 1
                
                    open_card(self,i,j)
                
                    if count % 2 == 0: #proveravamo da li su otvorene 2 kartice, ako jesu radimo sledece
                        if self.photo_matrix[i][j]==self.photo_matrix[pom_i][pom_j]: #ako su uparene
                            if player == 1: #ako je igrao zuti igrac
                                nonmatched.remove((i,j))
                                nonmatched.remove((pom_i,pom_j))
                                if (i,j) in opened:
                                    opened.remove((i,j))
                                if (pom_i,pom_j) in opened:
                                    opened.remove((pom_i,pom_j))
                                points_y += 1
                                self.points_yellow.configure(text ="Zuti: "+ str(points_y))
                                frame.after(700, lambda: change(photo_first,i,j)) #postavljamo na zute slicice jer su uparene
                            else:
                                #analogno za plavog
                                nonmatched.remove((i,j))
                                nonmatched.remove((pom_i,pom_j))
                                points_b += 1
                                self.points_blue.configure(text ="Plavi: "+ str(points_b))
                                frame.after(700, lambda: change(photo_second,i,j))
                        else:
                            frame.after(700, lambda: change(card_photo,i,j)) #vracamo na zatvorene slicice (jer nisu uparene dobro)
                            disable_buttons(self,n)   
                            if player == 1:
                                player = 2 #promenimo ko je na redu da igra
                                frame.after(700, lambda: change_of_player(self,"PLAVI"))

                                if var1.get() ==1: # u ovo ulazi samo ako smo uzeli opciju 1 vs rac (onda nam je racunar ustvari plavi igrac)
                                    frame.after(750, lambda: computer_playing(self,frame,photo_second,card_photo))
                                frame.after(700, lambda: enable_buttons(self,n))                 
                            else:
                                player = 1
                                frame.after(500, lambda: change_of_player(self,"ZUTI "))
                                frame.after(700, lambda: enable_buttons(self,n))
                                
                    # ako nisu, to znaci da imamo jednu otvorenu i zelimo da zapamtimo njenu poziciju
                    else:
                        pom_i=i
                        pom_j=j  
                
                if points_b + points_y == n*n/2 and done==0: #ako je done=1 onda smo presli na f_end u fji computer_playing
                    frame.after(1200,lambda : winner(points_b,points_y,frame))
        
                   
    
        
        
def raise_frame(frame):
    frame.tkraise()

def sel(f_start):    
    if var1.get()==1:
        print("1 vs rac")
        m = MatrixOfButtons(root,f_start,var1,var2,var3)
    else:
        print (var1.get())
        print("1 vs 1")
        m = MatrixOfButtons(root,f_start,var1,var2,var3)

class MainGUI:
    def __init__(self,master,var1,var2,var3):
        self.f_start = Frame(master)
        self.f_start.grid(column =1,row = 1)
        
        class CanvasButton:
            def __init__(self,f_start,canvas,var1,var2,var3):
                self.canvas = canvas
        
                myFont = Font(family="Courier", size=14)
                myFontBtn = Font(family="Courier", size=12)
                
            
                f_start.rb1 = tk.Radiobutton(self.canvas, text="1 vs rac", variable=var1, value=1,indicatoron=0,bg='LightCyan2',fg='navy',font=myFontBtn)
                canvas.create_window(370, 50,width=100, height=30,
                                            window=f_start.rb1)
                f_start.rb2 = tk.Radiobutton(self.canvas, text="1 vs 1", variable=var1, value=2,indicatoron=0,bg='LightCyan2',fg='navy',font=myFontBtn)
                canvas.create_window(480, 50,width=100, height=30,
                                            window=f_start.rb2)

                label = tk.Label(self.canvas,text='Izaberite tezinu:', font=myFont)   
                canvas.create_window(426, 100,
                                            window=label)
                f_start.rb3 = tk.Radiobutton(self.canvas,text="najlaksi nivo",variable=var2, value=1,bg='LightCyan2',fg='navy',font=myFontBtn,indicatoron = 0)
                canvas.create_window(426, 130,width=150, height=30,
                                            window=f_start.rb3)
                f_start.rb4 = tk.Radiobutton(self.canvas,text="srednji nivo",variable=var2, value=2,bg='LightCyan2',fg='navy',font=myFontBtn,indicatoron = 0)
                canvas.create_window(426, 165,width=150, height=30,
                                            window=f_start.rb4)
                f_start.rb5 = tk.Radiobutton(self.canvas,text="najtezi nivo",variable=var2, value=3,bg='LightCyan2',fg='navy',font=myFontBtn,indicatoron = 0)
                canvas.create_window(426, 200,width=150, height=30,
                                            window=f_start.rb5)
                
                
                label1 = tk.Label(self.canvas,text='Izaberite velicinu tabele:', font=myFont)   
                canvas.create_window(426, 245,
                                            window=label1)
                f_start.rb6 = tk.Radiobutton(self.canvas,text="4 x 4",variable=var3, value=4,bg='LightCyan2',fg='navy',font=myFontBtn,indicatoron = 0,command=lambda frame=f_start: sel(frame))
                canvas.create_window(426, 275,width=60, height=30,
                                            window=f_start.rb6)
                f_start.rb7 = tk.Radiobutton(self.canvas,text="6 x 6",variable=var3, value=6,bg='LightCyan2',fg='navy',font=myFontBtn,indicatoron = 0,command=lambda frame=f_start: sel(frame))
                canvas.create_window(426, 310,width=60, height=30,
                                            window=f_start.rb7)
                f_start.rb8 = tk.Radiobutton(self.canvas,text="8 x 8",variable=var3, value=8,bg='LightCyan2',fg='navy',font=myFontBtn,indicatoron = 0,command=lambda frame=f_start: sel(frame))
                canvas.create_window(426, 345,width=60, height=30,
                                            window=f_start.rb8)
    
        
        imgpath = 'poz1.gif'
        img = Image.open(imgpath)
        self.photo_background = ImageTk.PhotoImage(img)
        canvas = Canvas(self.f_start,width= 852,height =480)
        canvas.create_image(426,240,image = self.photo_background)
        canvas.image = self.photo_background
        canvas.grid(column =1,row=1)
    
        CanvasButton(self.f_start,canvas,var1,var2,var3)


        raise_frame(self.f_start)


root = Tk()
root.title('Memory game')
#root.configure(background='LightSteelBlue2',cursor='rtl_logo')

#root.geometry('800x500') # Size 800,500

#MENUBAR
menubar = Menu(root)
root.config(menu=menubar)
fileMenu = Menu(menubar)
helpMenu=Menu(menubar)

def ispisi():
    text="Ova igrica na na na"
    msg=messagebox.showinfo("O igrici",text)    

helpMenu.add_command(label="Pravila igre",command=ispisi)
fileMenu.add_command(label="Izadji",command=exit)
menubar.add_cascade(label="File", menu=fileMenu)
menubar.add_cascade(label="Help", menu=helpMenu)

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()

MainGUI(root,var1,var2,var3)

root.mainloop()

