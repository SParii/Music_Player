import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
import os
import pickle
from mutagen.mp3 import MP3
import pygame
from math import ceil
from time import sleep


pygame.mixer.init()

class music(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(bg="black")
        self.pack()

        #adding event listeners

        root.bind('<space>', self.pause_song)

        #previous song
        root.bind('<Left>', self.prev_song)

        #next song
        root.bind('<Right>', self.next_song)
        
        #playall
        root.bind('<Up>', self.playall)

        #for repeat
        root.bind('<Down>', self.repeat)

        # check songs.pickle
        if os.path.exists('C:/Users/saipa/OneDrive/Desktop/Music/songs.pickle'):
            with open('C:/Users/saipa/OneDrive/Desktop/Music/songs.pickle','rb') as f:
                self.playlist=pickle.load(f)
        else:
            self.playlist=[]

        #making some defaults
        self.current=0
        self.pause=True
        self.played=False
        self.confirm2=False
        self.loop2=False
        self.shuffled=False
        self.confirm=False


        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()
        self.marqee()
    
    def marqee(self):
    
        def shift():
            x1, y1, x2, y2 = self.canvas2.bbox("marquee")
            if (x2 < 0 or y1 < 0):  # reset the coordinates
                x1 = self.canvas2.winfo_width()
                y1 = 20
                self.canvas2.coords("marquee", x1, y1)
            else:
                self.canvas2.move("marquee", -20, 0)
            self.canvas2.after(1000 // self.fps, shift)
            ############# Main program ###############

        self.canvas2 = tk.Canvas(root, bg='#F6A9A9')
        self.canvas2.pack(fill="both", expand=1)
        
        self.text5 = "Where words fail, music speaks!"
        self.text3 = self.canvas2.create_text(0, -2000, text=self.text5, font=('consolas', 15, 'bold','italic'),
                                              fill='#00008b', tags=("marquee"), anchor='w')
        x1, y1, x2, y2 = self.canvas2.bbox("marquee")
        width = 620
        height = 1
        self.canvas2['width'] = width
        self.canvas2['height'] = height
        self.fps = 2  # Change the fps to make the animation faster/slower
        shift()

    def create_frames(self):
        # main wondow
        self.track= tk.LabelFrame(self,text="Main window",font=("times new roman",15,"italic","bold"),bd=4,fg='#00008b',bg="#F6A9A9",relief=tk.GROOVE)
        self.track.config(height=360,width=500)
        self.track.grid(row=0,column=0,padx=10,pady=(0,20))
        #track list
        self.tracklist= tk.LabelFrame(self,text="Song Nos",font=("times new roman",15,"italic","bold"),bd=4,fg='#00008b',bg="#F6A9A9",relief=tk.GROOVE)
        self.tracklist.config(height=420,width=190)
        self.tracklist.grid(row=0,column=2,padx=10,rowspan=2,pady=(0,0))
        #control bar
        self.control= tk.LabelFrame(self,font=("times new roman",25,"italic"),bd=2,fg='#00008b',bg="#F6A9A9",relief=tk.GROOVE)
        self.control.config(height=80,width=580)
        self.control.grid(row=1,column=0,padx=10,pady=(0,10))
        #volume bar
        self.volume= tk.DoubleVar()
        self.slider=ttk.Scale(self,from_=10,to=0, cursor='hand2',orient=tk.VERTICAL,length=490, variable=self.volume,command=self.change_volume)
        self.slider.set(8)
        self.slider.grid(row=0, column=1, rowspan=2, pady=10)
    
    def track_widgets(self):
        self.canvas=tk.Label(self.track, bg="#F6A9A9", image=img)
        self.canvas.configure(width=520, height=350)
        self.canvas.grid(row=0,column=0, columnspan=2)

        # A bar     
        self.songtrack = tk.Label(self.track, font=('times new roman',15,'italic','bold'),bg="#F6A9A9",fg='#00008b',text="Enjoy your music!") 
        self.songtrack.config(width=45,height=1)
        self.songtrack.grid(row=1, column=0)
    
    def control_widgets(self):
        self.loadSongs = tk.Button(self.control, bg='#F6A9A9',fg='#00008b',font=('consolas',17,'italic','bold'),text="Load-song", command=self.retreive_songs)
        self.loadSongs.config(height=1)
        self.loadSongs.grid(row=0, column=0, padx=5)

        #button
        self.loop=tk.Button(self.control,bd=1,bg='black',image=loop,cursor='hand2',activebackground='black',command=self.repeat)
        self.loop.config(height=45,width=48)
        self.loop.grid(row=0,column=1,pady=2,padx=2)

        #previous button
        self.previous=tk.Button(self.control,bd=1,bg='black',image=prev,cursor='hand2',activebackground='black', command=self.prev_song)
        self.previous.config(height=45,width=48)
        self.previous.grid(row=0,column=2,pady=2,padx=2)

        #Song Button
        self.play=tk.Button(self.control,bd=1,bg='black',image=play,cursor='hand2',activebackground='black', command=self.pause_song)
        self.play.config(height=45,width=48)
        self.play.grid(row=0,column=3,pady=2,padx=2)

        #Next Button
        self.next_=tk.Button(self.control,bd=1,bg='black',image=next_,cursor='hand2',activebackground='black',command=self.next_song)
        self.next_.config(height=45,width=48)
        self.next_.grid(row=0,column=4,pady=2,padx=1)
        
        # playall button
        self.shuffle=tk.Button(self.control,bd=1,bg='black',image=shuffle,cursor='hand2',activebackground='black',command=self.playall)
        self.shuffle.config(height=45,width=120)
        self.shuffle.grid(row=0,column=5,pady=2,padx=2)

        # progress bar
        self.progress_bar=ttk.Progressbar(self.control, mode='determinate', orient='horizontal',length=530)
        self.progress_bar.grid(row=1,columnspan=7)
       
    # tracklist widgets
    def tracklist_widgets(self):
        #scroll bar right side
        self.scrollbar=tk.Scrollbar(self.tracklist,orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=1,sticky='ns',rowspan=5)

        #scroll bar bottom side
        self.scrollbar2=tk.Scrollbar(self.tracklist,orient=tk.HORIZONTAL)
        self.scrollbar2.grid(row=5,column=0,sticky='ew',columnspan=3)

        #List where songs will appear
        self.list=tk.Listbox(self.tracklist,cursor='hand2',bg='#F6A9A9',fg='#483D8B',font=('times new roman',12,'italic','bold'),selectmode=tk.SINGLE,yscrollcommand=self.scrollbar.set,selectbackground='sky blue')
        self.enumerate_()
        self.list.config(height=22)

        #configure other scrollbar
        self.scrollbar.config(command=self.list.yview)
        self.scrollbar2.config(command=self.list.xview)

        # giving the position of list
        self.list.grid(row=0,column=0,rowspan=5)
        
        # binding the song
        #it will play the song on double click
        self.list.bind('<Double-1>',self.song)
        #it will play song on sekect + enter
        self.list.bind('<Return>',self.song)

    
    def retreive_songs(self):
        #blank list
        self.songlist=[]
        #opening file dialog
        directory= filedialog.askdirectory()
        for roots,dirs,files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1]=='.mp3':
                    path = (roots + '/' + file).replace('\\','/')
                    self.songlist.append(path)
        
        # dumping every song path to song.pickle
        with open('songs.pickle','wb') as f:
            pickle.dump(self.songlist, f)
        self.playlist = self.songlist
        # we will put every song name to songtrack bar
        self.tracklist['text']= f'Songs No- {str(len(self.playlist))}'
        # for deleting existing songs
        self.list.delete(0, tk.END)
        self.enumerate_()


    def enumerate_(self):
        #append all songs in the song track bar
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))
        self.tracklist['text']= f'Songs No- {str(len(self.playlist))}'

    # function for playing songs
    def song(self, event=None):
        #unpacking previous canvas 2
        try:
            self.canvas2.pack_forget()
        except:
            pass
        self.paused= False
        try:
            if event is not None:
                self.current=self.list.curselection()[0]
                for i in range(len(self.playlist)):
                    self.list.itemconfig(i,bg="sky blue")
            pygame.mixer.music.load(self.playlist[self.current])
            self.songtrack['text']=os.path.basename(self.playlist[self.current])
            self.g=f"--Now playing - {os.path.basename(self.playlist[self.current])}--"
            def shift():
                x1, y1, x2, y2 = self.canvas2.bbox("marquee")
                if (x2 < 0 or y1 < 0):  # reset the coordinates
                    x1 = self.canvas2.winfo_width()
                    y1 = 20
                    self.canvas2.coords("marquee", x1, y1)
                else:
                    self.canvas2.move("marquee", -20, 0)
                self.canvas2.after(1000 // self.fps, shift)
                ############# Main program ###############

            self.canvas2 = tk.Canvas(root, bg='#F6A9A9')
            self.canvas2.pack(fill="both", expand=1)
            
            self.text5 = "Where words fail, music speaks!"
            self.text3 = self.canvas2.create_text(0, -2000, text=self.text5, font=('consolas', 15, 'bold','italic'),
                                                fill='#00008b', tags=("marquee"), anchor='w')
            x1, y1, x2, y2 = self.canvas2.bbox("marquee")
            width = 620
            height = 1
            self.canvas2['width'] = width
            self.canvas2['height'] = height
            self.fps = 2  # Change the fps to make the animation faster/slower
            shift()
        except:
            messagebox.showerror('error',"Please select one of the song")
        self.song2=MP3(self.playlist[self.current])
        self.songlength= self.song2.info.length
        self.play['image']=pause
        self.played=True
        try:
            self.canvas.grid_forget()
        except:
            pass
        self.canvas = tk.Label(self.track)
        self.canvas.configure(width=520,height=350)
        self.canvas.grid(row=0,column=0,columnspan=2)
        if self.paused == False:
            #playing the GIF image
            self.l = AnimatedGIF(self.canvas,'C:/Users/saipa/OneDrive/Desktop/Music/12.gif')
            self.l.pack()
        else:
            self.canvas['image']=img


            
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg="sky blue")
        self.progress_bar['value']=0
        self.progress_bar['maximum']=ceil(self.songlength)

        self.x=0
        pygame.mixer.music.play()
        try:
            for i in range(self.x, ceil(self.songlength)):
                sleep(1)
                self.x= self.x + 1
                self.progress_bar['value']=self.x
                self.progress_bar.update()
                if self.x == ceil(self.songlength):
                    break
                if not self.paused:
                    continue
                else:
                    break
        except:
            pass
        if self.shuffled == True:
            if self.current == 0:
                self.current += 1
            elif self.current > 0 and self.current<(len(self.playlist)-1):
                self.current += 1
            elif self.current==(len(self.playlist)-1):
                self.current = 0
            self.song()
        else:
            pass
        if self.loop2 == True:
            self.song()
        #removing GIF after finishing the song
        try:
            self.canvas.grid_forget()
        except:
            pass
        self.canvas = tk.Label(self.track)
        self.canvas.configure(width=520,height=350)
        self.canvas.grid(row=0,column=0,columnspan=2)
        self.canvas['image']=img


    #function for pause and play the song via buttons
    def pause_song(self, event=None):
        if not self.paused:
            self.paused=True
            try:
                self.canvas2.pack_forget()
            except:
                pass
            def shift():
                x1, y1, x2, y2 = self.canvas2.bbox("marquee")
                if (x2 < 0 or y1 < 0):  # reset the coordinates
                    x1 = self.canvas2.winfo_width()
                    y1 = 20
                    self.canvas2.coords("marquee", x1, y1)
                else:
                    self.canvas2.move("marquee", -20, 0)
                self.canvas2.after(1000 // self.fps, shift)
                ############# Main program ###############

            self.canvas2 = tk.Canvas(root, bg='#F6A9A9')
            self.canvas2.pack(fill="both", expand=1)
            
            self.text5 = "(::)Song is paused(::)"
            self.text3 = self.canvas2.create_text(0, -2000, text=self.text5, font=('consolas', 15, 'bold','italic'),
                                                fill='#00008b', tags=("marquee"), anchor='w')
            x1, y1, x2, y2 = self.canvas2.bbox("marquee")
            width = 620
            height = 1
            self.canvas2['width'] = width
            self.canvas2['height'] = height
            self.fps = 2  # Change the fps to make the animation faster/slower
            shift()

            #we paste again
            try:
                self.canvas.grid_forget()
            except:
                pass
            self.canvas = tk.Label(self.track)
            self.canvas.configure(width=520,height=350)
            self.canvas.grid(row=0,column=0,columnspan=2)
            if self.paused == False:
                #playing the GIF image
                self.l = AnimatedGIF(self.canvas,'C:/Users/saipa/OneDrive/Desktop/Music/gif2.gif')
                self.l.pack()
            else:
                self.canvas['image']=img
            if self.shuffled == True:
                self.shuffle = False
            if self.loop2 == True:
                self.loop2 = False
            
            pygame.mixer.music.pause()
            self.play['image']=play
            self.progress_bar['value']=self.x
            self.progress_bar.update()
        else:
            if self.played==False:
                self.song()
            pygame.mixer.music.unpause()
            if self.confirm == True:
                self.shuffled = True
            if self.confirm2== True:
                self.loop2=True
            self.paused = False

            try:
                self.canvas2.pack_forget()
            except:
                pass
            def shift():
                x1, y1, x2, y2 = self.canvas2.bbox("marquee")
                if (x2 < 0 or y1 < 0):  # reset the coordinates
                    x1 = self.canvas2.winfo_width()
                    y1 = 20
                    self.canvas2.coords("marquee", x1, y1)
                else:
                    self.canvas2.move("marquee", -20, 0)
                self.canvas2.after(1000 // self.fps, shift)
                ############# Main program ###############

            self.canvas2 = tk.Canvas(root, bg='#F6A9A9')
            self.canvas2.pack(fill="both", expand=1)
            
            self.text5 = self.g
            self.text3 = self.canvas2.create_text(0, -2000, text=self.text5, font=('consolas', 15, 'bold','italic'),
                                                fill='#00008b', tags=("marquee"), anchor='w')
            x1, y1, x2, y2 = self.canvas2.bbox("marquee")
            width = 620
            height = 1
            self.canvas2['width'] = width
            self.canvas2['height'] = height
            self.fps = 2  # Change the fps to make the animation faster/slower
            shift()
            #again continue thw gif
            try:
                self.canvas.grid_forget()
            except:
                pass
            self.canvas = tk.Label(self.track)
            self.canvas.configure(width=520,height=350)
            self.canvas.grid(row=0,column=0,columnspan=2)
            self.l = AnimatedGIF(self.canvas,'C:/Users/saipa/OneDrive/Desktop/Music/gif2.gif')
            self.l.pack()
            self.play['image']=pause
            
            #resume the prgressbar
            try:
             for i in range(self.x, ceil(self.songlength)):
                sleep(1)
                self.x= self.x + 1
                self.progress_bar['value']=self.x
                self.progress_bar.update()
                if self.x == ceil(self.songlength):
                    break
                if not self.paused:
                    continue
                else:
                    break
            except:
               pass
            if self.shuffled == True:
                if self.current == 0:
                    self.current += 1
                elif self.current > 0 and self.current<(len(self.playlist)-1):
                    self.current += 1
                elif self.current==(len(self.playlist)-1):
                    self.current = 0
                self.song()
            else:
                pass
            if self.loop2 == True:
                self.song()
            try:
                self.canvas.grid_forget()
            except:
                pass
            self.canvas = tk.Label(self.track)
            self.canvas.configure(width=520,height=350)
            self.canvas.grid(row=0,column=0,columnspan=2)
            self.canvas['image']=img

    
    # function for playing prev song
    def prev_song(self, event=None):
        if self.current > 0:
            self.current -= 1
        else:
            self.current=0
        self.list.itemconfigure(self.current + 1, bg='sky blue')
        self.song()
    
    #function for playing next song
    def next_song(self,event=None):
         if self.current < len(self.playlist)-1:
            self.current += 1
         else:
            self.current=0
         self.list.itemconfigure(self.current , bg='sky blue')
         self.song()
    
    #for playing all songs in a row
    
    def playall(self, event=None):
        if self.shuffled == False:
            self.shuffled=True
            self.confirm = True
            self.shuffle['image']=shuffle2
        elif self.shuffled == True:
            self.shuffled = False
            self.confirm=False
            self.shuffle['image']=shuffle
            
    #For looping
    def repeat(self, event=None):
        if self.loop2 == False:
            self.loop2=True
            self.confirm2 = True
            self.loop['image']=loop2
        elif self.loop2 == True:
            self.loop2 = False
            self.confirm2=False
            self.loop['image']=loop

    # function for changing volume
    def change_volume(self, event=None):
        self.v = self.volume.get()
        pygame.mixer.music.set_volume(self.v/10)



from tkinter.ttk import Label   

class AnimatedGIF(Label, object):
    def __init__(self, master, path, forever=True):
        self._master = master
        self._loc = 0
        self._forever = forever

        self._is_running = False

        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self._frames.append(photoframe)

                i += 1
                im.seek(i)
        except EOFError:
            pass

        self._last_index = len(self._frames) - 1

        try:
            self._delay = im.info['duration']
        except:
            self._delay = 10

        self._callback_id = None

        super(AnimatedGIF, self).__init__(master, image=self._frames[0])

    def start_animation(self, frame=None):
        if self._is_running: return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self._is_running = False

    def _animate_GIF(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc])

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).grid(**kwargs)

    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).place(**kwargs)

    def pack_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).grid_forget(**kwargs)

    def place_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).place_forget(**kwargs)



            




root = tk.Tk()
root.config(bg="#F6A9A9")
root.title("Music player")
root.geometry('790x570+170+100')
root.attributes("-alpha",0.9)
root.resizable(0,0)

root.iconbitmap('C:/Users/saipa/OneDrive/Desktop/Music/y.ico')
image=Image.open('C:/Users/saipa/OneDrive/Desktop/Music/music1.jpg')
image=image.resize((524,354), Image.ANTIALIAS)
img=ImageTk.PhotoImage(image)

image=Image.open('C:/Users/saipa/OneDrive/Desktop/Music/pause.png')
image=image.resize((45,46), Image.ANTIALIAS)
pause=ImageTk.PhotoImage(image)


image=Image.open('C:/Users/saipa/OneDrive/Desktop/Music/previous.png')
image=image.resize((45,46), Image.ANTIALIAS)
prev=ImageTk.PhotoImage(image)


image=Image.open('C:/Users/saipa/OneDrive/Desktop/Music/play.png')
image=image.resize((45,46), Image.ANTIALIAS)
play=ImageTk.PhotoImage(image)


image=Image.open('C:/Users/saipa/OneDrive/Desktop/Music/shuffle.png')
image=image.resize((65,50), Image.ANTIALIAS)
shuffle=ImageTk.PhotoImage(image)


image=Image.open('C:/Users/saipa/OneDrive/Desktop/Music/shuffle2.png')
image=image.resize((65,50), Image.ANTIALIAS)
shuffle2=ImageTk.PhotoImage(image)


image=Image.open('C:/Users/saipa/OneDrive/Desktop/Music/next.png')
image=image.resize((45,46), Image.ANTIALIAS)
next_ =ImageTk.PhotoImage(image)


image=Image.open('C:/Users/saipa/OneDrive/Desktop/Music/loop.jpg')
image=image.resize((45,46), Image.ANTIALIAS)
loop=ImageTk.PhotoImage(image)


image=Image.open('C:/Users/saipa/OneDrive/Desktop/Music/loop2.png')
image=image.resize((45,46), Image.ANTIALIAS)
loop2=ImageTk.PhotoImage(image)




window = music(master=root)

window.mainloop()
