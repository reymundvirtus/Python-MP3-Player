from tkinter import *
from tkinter import filedialog # to access the file path for our music
import pygame, time
from mutagen.mp3 import MP3 # to know the song length
import tkinter.ttk as ttk

canvas = Tk()
canvas.title("Music Player")
canvas.iconbitmap("music_icons/favicon.ico")
app_width = 600
app_height = 200
screen_width = canvas.winfo_screenwidth()
screen_height = canvas.winfo_screenheight()
x = (screen_width / 200) + (app_width / 200)
y = (screen_height / 2) + (app_height / 2)
canvas.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
canvas.config(bg = '#f2f7f4')
canvas.wm_attributes('-transparentcolor','#f2f7f4')
f = ("Cambria", 10)

# initialize Pygame Mixer to have a sound
pygame.mixer.init()

# get the length time of the song
def play_time():
    # rab song time lapse
    current_time = pygame.mixer.music.get_pos() / 1000
    # throw up temp label to get data
    #temp_slider.config(text = f"Slider: {int(slider.get())} and Song Pos: {int(current_time)}")
    # converting to time format
    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))

    # get currently playing song
    current_song = song_list.curselection()
    song = song_list.get(current_song) # grab the song
    song = f"C:/Users/reymund virtus/Music/{song}.mp3"

    # get song length
    song_mut = MP3(song)

    # get the length of song
    global song_len
    song_len = song_mut.info.length

    # converting to time format
    converted_song_length = time.strftime("%M : %S", time.gmtime(song_len))

    # Increase current time by 1 second
    current_time += 1

    if int(slider.get()) == int(song_len):
        status_bar.config(text = f"Time Elapsed: {converted_song_length} ")
        next_song()
    elif paused:
        pass
    elif int(slider.get()) == int(current_time):
        # slider hasn't been moved
        slider_position = int(song_len)
        slider.config(to = slider_position, value = int(current_time))
    else:
        # slider has been moved
        slider_position = int(song_len)
        slider.config(to = slider_position, value = int(slider.get()))

        # converting to time format
        converted_current_time = time.strftime("%M : %S", time.gmtime(int(slider.get())))

        # output time in status bar
        status_bar.config(text = f"{converted_current_time}  -  {converted_song_length} ")

        # move this thing along by one second
        next_time = int(slider.get()) + 1
        slider.config(value = next_time)
    
    # output time in status bar
    #status_bar.config(text = f"Time Elapsed: {converted_current_time} of {converted_song_length} ")

    # update slider position value to the current time of song
    #slider.config(value = int(current_time))

    # update time
    status_bar.after(1000, play_time)


def fetch_songs():
    songs = filedialog.askopenfilenames(initialdir = "C:/Users/reymund virtus/Music", filetypes = (("mp3 Files", "*.mp3"),))
    
    for song in songs:
        # strip out the directory info and .mp3 extension from the song name
        song = song.replace("C:/Users/reymund virtus/Music/", "")
        song = song.replace(".mp3", "") 
        
        # adding a song
        song_list.insert(END, song)


def play(): # play a song
    # Reset slider status bar
    status_bar.config(text = "")
    slider.config(value = 0)

    song = song_list.get(ACTIVE)
    song = f"C:/Users/reymund virtus/Music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play()

    # call play_time function to get current time of the song
    play_time()

    # update slider to position
    #slider_position = int(song_len)
    #slider.config(to = slider_position, value = 0)


global paused
paused = False

def pause(is_paused): # pause a song
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


def next_song(): # next song button
    # Reset slider status bar
    status_bar.config(text = "")
    slider.config(value = 0)
    
    next_one = song_list.curselection()
    # add one to the current song number
    next_one = next_one[0] + 1
    song = song_list.get(next_one) # grab the next song
    song = f"C:/Users/reymund virtus/Music/{song}.mp3" # add directory structure
    pygame.mixer.music.load(song) # load the next song
    pygame.mixer.music.play(loops = 0)

    # clear active selectionbar to next
    song_list.selection_clear(0, END)
    # activate new song bar
    song_list.activate(next_one)
    # set active bar to next song
    song_list.selection_set(next_one, last = None)


def prev_song(): # play previous song
    # Reset slider status bar
    status_bar.config(text = "")
    slider.config(value = 0)

    next_one = song_list.curselection()
    # minus one to the current song number
    next_one = next_one[0] - 1
    song = song_list.get(next_one) # grab the next song
    song = f"C:/Users/reymund virtus/Music/{song}.mp3" # add directory structure
    pygame.mixer.music.load(song) # load the next song
    pygame.mixer.music.play(loops = 0)

    # clear active selectionbar to next
    song_list.selection_clear(0, END)
    # activate new song bar
    song_list.activate(next_one)
    # set active bar to next song
    song_list.selection_set(next_one, last = None)


# create slider function
def slide(x):
    #temp_slider.config(text = f"{int(slider.get())} of {int(song_len)}")
    song = song_list.get(ACTIVE)
    song = f"C:/Users/reymund virtus/Music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops = 0, start = int(slider.get()))


# volume function
def volume(x):
    pygame.mixer.music.set_volume(vol_slider.get())


# create playlist box
song_list = Listbox(canvas, bg = "#f2f7f4", font = f, fg = "white", selectbackground = "#1e77a5", selectforeground = "white", width = 40)
song_list.pack(pady = 5, side = LEFT)

# create player controller buttons images
prev_button_image = PhotoImage(file = "music_icons\previous.png")
next_button_image = PhotoImage(file = "music_icons\\next.png")
play_button_image = PhotoImage(file = "music_icons\play.png")
pause_button_image = PhotoImage(file = "music_icons\pause.png")
#stop_button_image = PhotoImage(file = "music_icons\stop.png")

# create status bar
status_bar = Label(canvas, bg = "#f2f7f4", font = f, fg = "white")
status_bar.pack(pady = 20, padx = 10)

# music slider
slider = ttk.Scale(canvas, from_ = 0, to = 100, orient = HORIZONTAL, value = 0, command = slide, length = 260)
slider.pack()

# temporary slider
#temp_slider = Label(canvas, text = "0", bg = "#f2f7f4")
#temp_slider.pack(pady = 10)

# create player control frame
controls_frame = Frame(canvas, bg = "#f2f7f4")
controls_frame.pack()

# create player control button
prev_button = Button(controls_frame, image = prev_button_image, borderwidth = 0, bg = "#f2f7f4", command = prev_song)
prev_button.grid(row = 0, column = 0, padx = 10, pady = 10)
pause_button = Button(controls_frame, image = pause_button_image, borderwidth = 0, bg = "#f2f7f4", command = lambda: pause(paused))
pause_button.grid(row = 0, column = 2, padx = 10, pady = 10)
play_button = Button(controls_frame, image = play_button_image, borderwidth = 0, bg = "#f2f7f4", command = play)
play_button.grid(row = 0, column = 1, padx = 10, pady = 10)
next_button = Button(controls_frame, image = next_button_image, borderwidth = 0, bg = "#f2f7f4", command = next_song)
next_button.grid(row = 0, column = 3, padx = 10, pady = 10)
#stop_button = Button(controls_frame, image = stop_button_image, borderwidth = 0)
#stop_button.grid(row = 0, column = 4)

# create volume label frame
volume_frame = LabelFrame(canvas, bg = "#f2f7f4")
volume_frame.pack()

# create volume slider
vol_slider = ttk.Scale(volume_frame, from_ = 0, to = 1, orient = HORIZONTAL, value = 1, command = volume, length = 125)
vol_slider.pack()

# create menu
fetch_songs()

# create player controller buttons

canvas.overrideredirect(1)
canvas.mainloop()