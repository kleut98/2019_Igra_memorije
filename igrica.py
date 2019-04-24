from tkinter import *
import tkinter as tk
import os
import random
import time
from tkinter.font import Font

#!!! ne radi nam ako neko klikne na isto dugme vise putaa
#1) staviti sliku kao pozadinu na frejmu f_one_player
#2) dodati labele za rezultate
#3) napraviti kada se otkriju dve slike da se proveri da li su iste ili razlicite....
#4) kada nema vise slika-dugme za igrati ponovo/glavni meni??
#5) 

brojac=0
pom_i=-1
pom_j=-1

class MatrixOfButtons:
    #master je root
    def __init__(self,master,frame,n,photo_num):
        #self=root a frame=f_one_player
        self.b=[[0 for x in range(0,n)] for x in range(0,n)] #matrica dugmica

        #??????ne znamo da li nam treba da svako dugme stavimo u poseban frejm???????
        #mozda je bolje da bismo mogli da podesimo velicinu slike itd
        #self.frames=[[0 for x in range(0,n)] for x in range(0,n)] #matrica frejmova za dugmice
        photo_matrix=[[0 for x in range(0,n)] for x in range(0,n)] #matrica slika

        photo_list=[1,2,3,4,5,6,7,8,9,10,11,1,2,3,4,5,6,7,8,9,10,11,1,2,3,4,5,6,7,8,9,10] #broj slika (sada ih ima 11, promeniti!)
        list_pair=[] #lista parova=koordinate u matrici (i,j)
        
        for i in range(0,n):
            for j in range(0,n):
                list_pair.append((i,j))
                photo_matrix[i][j]=" " 

        while list_pair!=[]:
            broj_slike=random.choice(photo_list)
            photo_list.remove(broj_slike)
            
            pair=random.choice(list_pair)
            list_pair.remove(pair)
            pair1=random.choice(list_pair)
            list_pair.remove(pair1)

            #na poziciji (i,j) cuvamo naziv slike
            photo_matrix[pair[0]][pair[1]]="slike1\\"+str(broj_slike)+".gif"
            photo_matrix[pair1[0]][pair1[1]]="slike1\\"+str(broj_slike)+".gif"
            
        for i in range(0,n):
            for j in range(0,n):
                #path=os.path.join(photo_matrix[i][j])
                #path=os.path.join("slike1\\nesto.png")
                photo=PhotoImage(file="slike1\\"+str(photo_num)+".gif")#slika kartica
                photo1=PhotoImage(file=photo_matrix[0][0])
                #???????????????????
                #da li stavljati u ove nove frejmove??
                #self.frames[i][j]=Frame(frame)
                #self.b[i][j].pack(fill='both',anchor='center',expand=True)

                self.b[i][j] = Button(frame,image=photo,text = str(i)+''+str(j),command=lambda x1=i, y1=j,matrica=photo_matrix,frame=frame,card_photo=photo: self.funkcija(x1,y1,matrica,frame,card_photo))
                self.b[i][j].image=photo #*
                self.b[i][j].grid(row = i,column = j,sticky='nsew')
                
        rezultat=Label(frame, text='labela').grid(column = n+5,row =0)    
        
                       
    def funkcija(self,i,j,photo_matrix,frame,card_photo):
        #print (str(i))
        global pom_i,pom_j
        
        if pom_i!=i or pom_j!=j: #da ne bi nastao problem ako neko klikne dva puta na isto dugme
        
            global brojac
            brojac=brojac+1
        
            photo=PhotoImage(file=photo_matrix[i][j])
            self.b[i][j].config(image=photo)

            #moramo ponovo da postavimo sliku zbog sakupljaca otpadaka, jer ga on pokupi u suprotnom*
            self.b[i][j].image=photo
        
            if brojac%2==0:
                if photo_matrix[i][j]==photo_matrix[pom_i][pom_j]:
                    print ("nakns")#"sklanjaju se"
                else:
                    frame.after(700, lambda: promeni(self,card_photo))
                    #self.b[i][j].config(image=photo1)
            else:
                pom_i=i
                pom_j=j   
       # self.b[i][j].destroy()
    
            def promeni(self,photo):
                self.b[i][j].config(image=photo)
                self.b[i][j].image=photo
                self.b[pom_i][pom_j].config(image=card_photo)
                self.b[pom_i][pom_j].image=card_photo

def raise_frame(frame):
    frame.tkraise()

def sel(f_start):

    if var1.get()==1:
        print("1 vs rac")
        f_start.destroy()
        raise_frame(f_one_player)
        m = MatrixOfButtons(root,f_one_player,var3.get(),var2.get())
    else:
        print("1 vs 1")
        raise_frame(f_two_players)
        m = MatrixOfButtons(root,f_two_players,var3.get())

class MainGUI:

    def __init__(self, master,photo1,photo2,photo3,var1,var2,var3):
        self.f_start = Frame(master)
        self.f_start.grid(column=1, row=1)
        #cemu ovo sluzi??
        #self.f_start.columnconfigure(1, weight=1)
        #self.f_start.rowconfigure(1, weight=1)
        myFont = Font(family="Segoe Print", size=14)
        label=Label(self.f_start, text='Izaberite opciju:', font=myFont).grid(column = 1,row =1)    
        rb1=tk.Radiobutton(self.f_start, text="1 vs rac", variable=var1, value=1,indicatoron=0).grid(column = 1,row =2)
        rb2=tk.Radiobutton(self.f_start, text="1 vs 1", variable=var1, value=2,indicatoron=0).grid(column =2,row =2)
        
        Label(self.f_start, text='Izaberite kartice:',font=myFont).grid(column = 1,row =3)
        tk.Radiobutton(self.f_start,image = photo, text="opcija 1", variable=var2, value=1,indicatoron = 0).grid(column =1,row =4)
        tk.Radiobutton(self.f_start,image = photo2, text="opcija 2", variable=var2, value=2,indicatoron = 0).grid(column =2,row =4)
        tk.Radiobutton(self.f_start,image = photo3 ,text="opcija 3", variable=var2, value=3,indicatoron = 0).grid(column =3,row =4)

        Label(self.f_start, text='Koliko kartica zelite?',font=myFont).grid(column = 1,row =5)
        #prosledjujemo pocetni frejm (f_start)
        tk.Radiobutton(self.f_start, text="4x4", variable=var3, value=4,command=lambda frame=self.f_start: sel(frame),indicatoron = 0).grid(column =1,row =6)
        tk.Radiobutton(self.f_start, text="8x8", variable=var3, value=8,command=lambda frame=self.f_start: sel(frame),indicatoron = 0).grid(column =2,row =6)
        tk.Radiobutton(self.f_start, text="16x16", variable=var3, value=16,command=lambda frame=self.f_start: sel(frame),indicatoron = 0).grid(column =3,row =6)
        
        raise_frame(self.f_start)


root = Tk()
root.title('Memory game')
root.geometry('800x600') # Size 200, 200

f_one_player = Frame(root)
f_two_players = Frame(root)

f_one_player.grid(row=1, column=1,sticky="nsew",padx=20,pady=20)
f_two_players.grid(row=1, column=1,sticky="nsew",padx=20,pady=20)
photo=PhotoImage(file='slike1/1.gif')
photo2 = PhotoImage(file ='slike1/2.gif')
photo3 = PhotoImage(file = 'slike1/3.gif')
var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
MainGUI(root,photo,photo2,photo3,var1,var2,var3)
root.mainloop()
