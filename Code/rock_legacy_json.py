## ROCK LEGACY APP 🎸

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os

# JSON logic and funtions to save the data permanently

USER_FILE = "users.json" # creates users file in a defoult path
SONG_FILE = "songs.json" # creates songs file in a default path

def save_users():  # takes in-memory users dict, with parameters
    data = {
        name: {
            "password": u.password,
            "color": u.color,
            "active": u.active}
        for name, u in users.items()}
    with open (USER_FILE, "w") as f:  # saves it to a file
        json.dump(data, f, indent=4)  # python -> json + readable format

def load_users():
    if not os.path.exists(USER_FILE): # checks if the file exists in the system
        return {} # returns empty dictionary instead of data that isn't there
    with open(USER_FILE, "r") as f: # loads json data
        data = json.load(f) # rebuilds the dict from stored info
    return {name: User(name, d["password"], d["color"], d["active"]) for name, d in data.items()} 

def save_songs(): # as above
    with open(SONG_FILE, "w") as f: 
        json.dump(songs, f, indent=4)

def load_songs():
    if not os.path.exists(SONG_FILE):
        return []
    with open(SONG_FILE, "r") as f:
        return json.load(f)

# ---------SETUP DATABASE----------
# the app's basic feature was that all activities are tied to user's own account, marked by color
# The class will define the data and actions each user can perform with all the attributes strictly connected to the user

class User(): # user class stores and manages users information
    def __init__(self, name, password, color, active=True):
        self.name = name
        self.password = password
        self.color = color
        self.active = active
    
    def toggle_active(self):
        self.active = not self.active


users = load_users() # load existing users from json file
if not users: #if users file empty load with those users below

# create dictionary of users, set individual passwords and colors, flag as active/inactive (all users are active now)
    users = {
        "Coco": User("Coco", "Hulk123", "green", True),
        "Martin": User("Martin", "RockKing123", "cornflowerblue", True),
        "Jane": User("Jane", "BigJ123", "darkcyan", True),
        "Beto": User("Beto", "Betaso123", "darkorange", True),
        "Vari": User("Vari", "Latina123", "orchid", True),
        "Fer": User("Fer", "Latino123", "maroon", True),
        "AK": User("AK", "Coder123", "crimson", True)  }
save_users() # save to json file

# create foundations for music data
songs = load_songs() # load songs from file. Replaces the old empty array songs = []

# for keeping the app clean and polished, (no randomly entered info):
# make a list of genres
genres = {"Classic Rock", "Rock & Roll", "Hard Rock", "Heavy Metal", "Latino Rock", "Instrumental", "Soundtrack", "Pop/ Glam Rock", "Prog Rock", "Alternative", "Modern", "Punk", "Grunge", "Indie", "Metal"}

# make a list of decades
decades = {"50ties", "60ties", "70ties", "80ties", "90ties", "2000s"}

# create a list of available colors for users. Limited users = limited colors
available_colors = {
    "orange", "green", "blue", "cyan", "yellow", "maroon", "crimson",
    "purple", "pink", "teal", "lime", "magenta", "navy", "brown", "olive", "lightblue", "gold", "seagreen", "coral", "salmon", "turquoise", "violet", "indigo", "khaki", "plum", "firebrick", "slateblue", "saddlebrown", "mediumvioletred", "rosybrown", "goldenrod", "darkslategray", "burlywood", "darkolivegreen"
}

# create a function to use later eliminating already assigned colors so they don't get repeated amongst users
def get_available_colors():
    taken = {u.color for u in users.values()}
    return [c for c in available_colors if c not in taken]


# ---------- CORE PROGRAMMING ----------

# setup tkinter main window 
class RockLegacy(tk.Tk): # this class defines the main application window, managed GUI and logic
    def __init__(self):
        super().__init__()
        self.title("🎸 Rock Legacy 🎸")
        self.geometry("800x600")
        self.current_user = None # defines the variable of a user who signs in. Primarily no one
        self.login() # displays login screen

# 1. Designing the login window       
# Create a tool that clears current window from previous information. Without it the multiple widgets will overlap with each other- the program will look messy and may crash. This will be reused every time a new menu is being opened

    def window_cleaner(self):
        for widget in self.winfo_children(): # method that shows child widgets within parent widget
            widget.destroy() #destroys all displayed widgets
 
# 1a) Design the login window skeleton
    def login(self):
        self.window_cleaner() # clears the window every time UI restarts
        tk.Label(self, text="🎸 Y'ALL ROCK!! Select your username", font=("Helvetica", 20)).pack(pady=20)

# 1b) add a scrollable function for when the user database grow (expected 16 users as per group)
        container = ttk.Frame(self)
        container.pack(fill="both", expand=False, padx=20)

# 1c) populate the login page with users as per the users list, mark if active
        for username, user in users.items(): # loop thru existing users and create button for each one
            status = "ACTIVE" if user.active else "INACTIVE"
            btn = tk.Button(container, text= f"{username} ({status})", width=30, command=lambda u=username: self.ask_psswd(u)) # 1 button = 1 user/list
            btn.configure(fg=user.color) # username+status written in individual user's color
            btn.pack(pady=5)
    
        tk.Button(self, text="Quit", command=self.destroy).pack(side="bottom", pady=10)

# 1d) create a password-handling feature for each user
    def ask_psswd(self, username):
        user = users[username]
        if not user.active: # inactive users can't login
            messagebox.showinfo("Inactive", "This user is inactive and can't log in")
            return
        pswd = simpledialog.askstring("Password", f"Enter password for {username}", show="*") 
        if pswd is None: # if button cancel or x are pressed
            return
        if pswd == user.password:
            self.current_user = user # if login successful, this stores user-login info permanently within the app so everything the user does from now on is tied to individual activity.
            self.main_menu()
        else:
            messagebox.showinfo("Error", "Incorrect password")

# 2. Design main menu

    def main_menu(self):
        self.window_cleaner()

        tk.Label(self, text=f"Welcome {self.current_user.name}", font=("Helvetica", 20)).pack(pady=15)

# create menu options and assign buttons
# link to independent menus through command assignment 
        ttk.Button(self, text="Edit Profile", width=25, command=self.edit_profile_frame).pack(pady=5)
        ttk.Button(self, text="Manage Songs", width=25, command=self.manage_songs_frame).pack(pady=5)
        ttk.Button(self, text="View Catalogue", width=25, command=self.catalogue).pack(pady=5)
        ttk.Button(self, text="User Management", width=25, command=self.user_management).pack(pady=5)
        ttk.Button(self, text="Logout", width=25, command=self.logout).pack(pady=5)

#  create a layout for edit profile menu
    def edit_profile_frame(self):
        self.window_cleaner()
        tk.Label(self, text=f"Edit Profile", font=("Helvetica", 15)).pack(pady=10)

        ttk.Button(self, text="Change Username", width=30, command=self.change_username).pack(pady=5)
        ttk.Button(self, text="Change Password", width=30, command=self.change_password).pack(pady=5)
        ttk.Button(self, text="Deactivate Account", width=30, command=self.deactivate_account).pack(pady=5)
        ttk.Button(self, text="Back", width=30, command=self.main_menu).pack(pady=10)

# 2a) design the change username option for the edit profile menu
    def change_username(self):
        olduname = self.current_user.name
        newuname = simpledialog.askstring("Change username", "Enter your new username: ")
        if newuname is None:  # if the user cancels action
            return  
        if not newuname: # if the user makes no entry
            messagebox.showerror("Error", "Username can't be empty")
            return
        if newuname in users: # if user enters a name that belongs to another user
            messagebox.showerror("Error", f"{newuname} already exists!")
            return
        users[newuname]  = users.pop(olduname)
        # update current_user reference and name
        self.current_user = users[newuname]
        self.current_user.name = newuname
        messagebox.showinfo("Success", f"Username changed to {newuname}")
        self.main_menu()
        save_users() # import changes to json

# 2b) design the change password option in the edit profile menu
    def change_password(self):
        oldpswd = simpledialog.askstring("Change password", "Enter your current password: ", show="*")
        if oldpswd is None:
            return
        if oldpswd != self.current_user.password: # if passwords don't match
            messagebox.showerror("Error", "Incorrect current password")
            return
        newpswd = simpledialog.askstring("New password", "Enter new password:")
        if newpswd is None: # if user cancels
            return
        repswd = simpledialog.askstring("New password", "Re-enter your password:", show="*") # ask to confirm new password
        if repswd is None: # if user cancels
            return 
        if newpswd != repswd: # if new passwords don't match
            messagebox.showerror("Error", "Passwords don't match")
            return
        self.current_user.password = newpswd
        messagebox.showinfo("Success", "Password changed")
        save_users()

# 2c) design the deactivation option
    def deactivate_account(self):
        confirm = messagebox.askyesno("Deactivate", "Are you sure you want to deactivate your account?") # pop a yes/no prompt
        if confirm:
            self.current_user.active = False
            messagebox.showinfo("Success", "You have successfully deactivated your account.")
            self.logout() # return to login page
            save_users()

# 3. Design and handle the music menu
# design the look for the music menu the same way the Edit Profile menu was designed

    def manage_songs_frame(self):
        self.window_cleaner()
        tk.Label(self, text="Manage Songs", font=("Helvetica", 15)).pack(pady=10)

        ttk.Button(self, text="Add Song", width=30, command=self.add_song_graphics).pack(pady=5)
        ttk.Button(self, text="Delete Song", width=30, command=self.delete_song_graphics).pack(pady=5)
        ttk.Button(self, text="List Your Songs", width=30, command=self.list_songs).pack(pady=5)
        ttk.Button(self, text="Back", width=30, command=self.main_menu).pack(pady=10)

# 3a) design the whole Add Song structure.

# Each song needs to be added to the library. 
# Add logic to create a song catalogue based on specified parameters
    def add_song_logic(self, user, title, artist, genre, decade, notes):
        if not title or not artist or not genre or not decade: #makes sure the user fills all required entries
            return False
        songs.append({
            "title": title.strip(), # strips added to disregard whitespacing in free text
            "artist": artist.strip(),
            "genre": genre,
            "decade": decade,
            "notes": (notes.strip() if notes else ""), # notes optional, if none, proceed empty
            "user": user.name,
            "color": user.color
        })
        save_songs()
        return True
    

#  design the graphic elements in the window
    def add_song_graphics(self):
        self.window_cleaner()
        tk.Label(self, text="Add Song", font=("Helvetica", 15)).pack(pady=10)

    # for the desired layout more advanced features are necessary 
    # create a "holder" to keep all the fields neat and organised
        frame_setup = ttk.Frame(self)
        frame_setup.pack(pady=5)

    # create a manual entry for a song title
        ttk.Label(frame_setup, text="Title").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        title_entry = ttk.Entry(frame_setup, width=40)
        title_entry.grid(row=0, column=1, pady=5)

    # create a manual entry for the artist
        ttk.Label(frame_setup, text="Artist").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        artist_entry = ttk.Entry(frame_setup, width=40)
        artist_entry.grid(row=1, column=1, pady=5)

    # create an entry for genre. 
    # the app is meant to be user-friendly so keep the genres list selectable from expandable menu rather than having to do manual entry
        ttk.Label(frame_setup, text="Genre").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        genre_entry = ttk.Combobox(frame_setup, values=list(genres), state="readonly", width=40)
        genre_entry.grid(row=2, column=1, pady=5)

    # create an entry for decades (the exact same logic as with genre selection applies)
        ttk.Label(frame_setup, text="Decade").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        decade_entry = ttk.Combobox(frame_setup, values=list(decades), state="readonly", width=40)
        decade_entry.grid(row=3, column=1, pady=5)

    # create a space for optional notes about the song
        ttk.Label(frame_setup, text="Notes").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        notes_entry= ttk.Entry(frame_setup, width=40)
        notes_entry.grid(row=4, column=1, pady=5)

# fetch song data from the information entered by the user throught the graphic interface, then add the song to the catalogue invoking the logcial function
        def submit_song():
            title = title_entry.get().strip()
            artist = artist_entry.get().strip()
            genre = genre_entry.get()
            decade = decade_entry.get()
            notes= notes_entry.get().strip()
            add= self.add_song_logic(self.current_user, title, artist, genre, decade, notes)
            if add: 
                messagebox.showinfo("Success", f"{title} by {artist} added to the library")
                self.manage_songs_frame()
            else:
                messagebox.showerror("Error", "Missing or invalid data") 

        ttk.Button(self, text="Add Song", command=submit_song).pack(pady=10)
        ttk.Button(self, text="Back", command=self.manage_songs_frame).pack(pady=10)        

# 3b) create song deletion option
# you need a separate catalogue of songs that belong to specific user
    def list_user_songs(self, user):
        user_catalogue =[]
        for song in songs:
            if song["user"] == user.name:
                user_catalogue.append(song)
        return user_catalogue   
       
# design the logic to handle deletion of listed songs
    def delete_song_logic(self, user, title):
        # find first matching song by title (case-insensitive) for this user
        for song in list(songs):
            if song["user"] == user.name and song["title"].lower() == title.lower():
                songs.remove(song)
                save_songs()
                return f"{song['title']} by {song['artist']} removed from the library"
        return f"{title} not in the library"
            
# design the graphical interface
    def delete_song_graphics(self):
        self.window_cleaner()
        tk.Label(self, text="Delete Song", font=("Helvetica", 15)).pack(pady=10)

        user_songs = self.list_user_songs(self.current_user) # list song library of the current user
        if not user_songs: # create condition if no songs added
            tk.Label(self, text="You haven't added any songs yet").pack(pady=10)
            tk.Button(self, text="Back", command=self.manage_songs_frame).pack(pady=10)
            return
    
# create a list box and fill it with users songs    
        song_box= tk.Listbox(self, width=80, height=15)
        song_box.pack(pady=5)
        for tune in user_songs:
            song_box.insert(tk.END, f"{tune['artist']} - {tune['title']} - {tune['genre']} - {tune['decade']}")

# handle  selection through the list choice
        def select_delete():
            songsel = song_box.curselection() # returns selected item from the list with index no
            if not songsel:
                messagebox.showwarning("Select", "Select a song to delete")
                return
            index = songsel[0] # stores index number of the song user selected in the box
            song = user_songs[index]
            confirm = messagebox.askyesno("Confirm Delete", f"Delete {song['title']} by {song['artist']}?")              
            if confirm:
                msg = self.delete_song_logic(self.current_user, song["title"])
                messagebox.showinfo("Result", msg)
                self.manage_songs_frame()

        ttk.Button(self, text="Delete Selected", command=select_delete).pack(pady=5)
        ttk.Button(self, text= "Back", command=self.manage_songs_frame).pack(pady=10)

# 3c) design an option to list user's songs
    def list_songs(self):
        self.window_cleaner()
        tk.Label(self, text="List Your Songs", font=("Helvetica", 15)).pack(pady=10)

    # create a message if user didn't add any songs to their library
        user_songs = self.list_user_songs(self.current_user)
        if not user_songs:
            tk.Label(self, text="No songs added yet").pack(pady=10)
            tk.Button(self, text="Back", command=self.manage_songs_frame).pack(pady=10)
            return
    
    # design if songs in the library
    # create a scrollable frame to contain all the songs, add features
        canvas = tk.Canvas(self, height= 350)
        scrollbar = ttk.Scrollbar(self, orient= "vertical", command=canvas.yview) # adjusts the canvas as the scrollbar moves
        scroll_frame = ttk.Frame(canvas)

    # dynamically adjust the scrollbar to the changing frame
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
        canvas.create_window((0,0), window=scroll_frame, anchor="nw") # put scrollable frame inside canvas, from top left corner
        canvas.configure(yscrollcommand=scrollbar.set) # link the scrollbar to canvas

        canvas.pack(side="left", fill="both", expand=True, padx=(10,0))
        scrollbar.pack(side="right", fill="y", padx=(0,10))

    # display user's song list in the frame 
        for song in user_songs:
            info = tk.Label(scroll_frame, text=f"{song['artist']} - {song['title']} - {song['genre']} - {song['decade']}",
                   anchor="w", justify="left", fg=song.get("color")) # write in user's color
            info.pack(fill="x", padx=10, pady=5)

        ttk.Button(self, text="Back", command=self.manage_songs_frame).pack(pady=10)

# 4. Design catalogue with songs by the decade and genre
# design physical interface

    def catalogue(self):
        self.window_cleaner()
        tk.Label(self, text="Catalogue", font=("Helvetica", 15)).pack(pady=10)

# the buttons can't call results directly, instead they open another menu
        tk.Button(self, text="View by Decade", width=30, command= lambda: self.show_catalogue("Decade")).pack(pady=5)
        tk.Button(self, text="View by Genre", width=30, command= lambda: self.show_catalogue("Genre")).pack(pady=5)
        ttk.Button(self, text="Back", width=30, command=self.main_menu).pack(pady=10)

    def show_catalogue(self, view):
        self.window_cleaner()
        tk.Label(self, text=f"Catalogue by {view}", font=("Helvetica", 15)).pack(pady=10)

# create a decade/ genre sorting logic
        if view == "Decade":
            catalogue = {decade: [] for decade in decades}
            for song in songs:
                if song["decade"] in catalogue:
                    catalogue[song["decade"]].append(song)
        else:
            catalogue = {genre: [] for genre in genres}
            for song in songs:
                if song["genre"] in catalogue:
                    catalogue[song["genre"]].append(song)

# create a similar graphic design like in the previous menu
# again, create a scrollable area

        canvas = tk.Canvas(self, height=380)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollframe = ttk.Frame(canvas)

        scrollframe.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0,0), window=scrollframe, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(10,0))
        scrollbar.pack(side="right", fill="y", padx=(0,10))

# loop through the key in the categories and the song list in the catalogue dictionary, create a label for that category, and then list all the songs inside it.
        for key, songlist in catalogue.items():
            group = ttk.LabelFrame(scrollframe, text=key, padding=(10,5))
            group.pack(fill="x", padx=10, pady=5)
            if not songlist: 
                tk.Label(group, text="no songs").pack(anchor="w") # no added entries= empty box
            else:
                for song in songlist:
                    lbl = tk.Label(group, text=f"{song['artist']} - {song['title']} - {song['genre']} - {song['decade']}", anchor="w", justify="left", fg=song.get("color"))
                    lbl.pack(anchor="w")

        ttk.Button(self, text="Back", command=self.catalogue).pack(pady=10)

# 5. Design user management menu
# design graphic framework

    def user_management(self):
        self.window_cleaner()
        tk.Label(self, text="User Management", font=("Helvetica", 15)).pack(pady=10)
        ttk.Button(self, text="List Users", width=30, command=self.list_users).pack(pady=5)
        ttk.Button(self, text="Add Users", width=30, command=self.add_user_graphics).pack(pady=5)
        ttk.Button(self, text="Back", width=30, command=self.main_menu).pack(pady=5)

# 5a) create a logic and graphics for listing users    

    def list_users(self):
        self.window_cleaner()
        tk.Label(self, text="All Users", font=("Helvetica", 15)).pack(pady=10)

        for user in users.values():
            status = "ACTIVE" if user.active else "INACTIVE"
            showall = tk.Label(self, text=f"{user.name} ({status})", fg=user.color) # lists users in individual colors
            showall.pack(anchor="w", padx=10, pady=5)

        ttk.Button(self, text="Back", width=30, command=self.user_management).pack(pady=10)

# 5b) create add user function
# create logic for adding users

    def add_user_logic(self, name, password, color):
        name = name.strip()
        password = password.strip()
        color = color.strip()
        if not name or not password or not color:  # all fields required
            return "Name, password and color are required"
        if name in users:  # can't use someone else's name
            return f"{name} already exists!"
        if color not in available_colors or color in (u.color for u in users.values()): # can't use someone else's color 
            return f"{color} is not available"
        users[name] = User(name, password, color)
        save_users()
        return f"{name} added to the team"

# create a graphic frame for the logic
    def add_user_graphics(self):
        self.window_cleaner()
        tk.Label(self, text="Add User", font=("Helvetica", 15)).pack(pady=12)

        form= ttk.Frame(self)
        form.pack(pady=5)

        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        name_entry = ttk.Entry(form, width=40)
        name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        pswd_entry = ttk.Entry(form, show="*", width=40)
        pswd_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form, text="Color:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        color_sel = ttk.Combobox(form, values=get_available_colors(), state="readonly", width=35)
        color_sel.grid(row=2, column=1, pady=5)

# collect new user data from graphical interface and add user to the pool of users
        def submit_add_user():
            name = name_entry.get().strip()
            password = pswd_entry.get().strip()
            color = color_sel.get().strip()
            result = self.add_user_logic(name, password, color)
            messagebox.showinfo("Result", result)
            self.user_management()

        ttk.Button(self, text="Add User", command=submit_add_user).pack(pady=10)
        ttk.Button(self, text="Back", command=self.user_management).pack()

    def logout(self):
            self.current_user = None
            self.login()


if __name__ == "__main__":
    app = RockLegacy()
    app.mainloop()
