# ######################
# Workflow:
# --------
# ->Splash Screen
# |
# +fingerprint trigger
# |
# ->Id confirmation screen
# |
# +vote btn
# |
# ->Voting screen.
# |
# +confirm vote btn
# |
# -> Splash Screen
# #######################
# https://www.tutorialspoint.com/python/python_gui_programming.htm


from tkinter import *
import tkinter.font as tkfont
from PIL import Image, ImageTk


# this function is called when submit vote button is clicked on the voting page.
def submit_vote(candidate_id, vframe, sframe):
    # increment count in XLS and save file.
    selected_candidate = candidate_id()
    print(selected_candidate)
    # hide vote and return to splash screen
    vframe.pack_forget()
    sframe.pack(expand=True)
    # http://stackoverflow.com/questions/29634742/tkinter-toplevel-widgets-not-displaying-python
    # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/universal.html
    sframe.update_idletasks()
    election_window.configure(background=splash_bg)
    return True


def get_ballot_for_constituency(constituency_id):
    return [{"id": 1, "Candidate": "Blade Mani", "Party": "BMK"},
            {"id": 2, "Candidate": "Rowdy Ragu", "Party": "BMM"},
            {"id": 3, "Candidate": "Maatu Ravi", "Party": "BMW"},
            {"id": 4, "Candidate": "Appu", "Party": "Independent"}]


def start_voting(c_id, user_id, idframe, sframe):
    vote_selection = IntVar()

    def setvar():
        return vote_selection.get()

    idframe.pack_forget()
    vote_frame = Frame(election_window, bg=app_bg)
    ballot_list = get_ballot_for_constituency(c_id)
    Label(vote_frame, anchor=CENTER, text="Choose your candidate", bg=splash_bg, fg=light_font, padx=30,
          font=freesans18).pack(fill="x", expand=True, pady=30)

    for candidate in ballot_list:
        Radiobutton(vote_frame, text=candidate['Candidate']+' - Party: '+candidate['Party'], variable=vote_selection,
                    value=int(candidate['id']), borderwidth=1, bg=app_bg, fg=dark_font, pady=10,
                    command=setvar).pack(fill="x", anchor=W)

    Radiobutton(vote_frame, text="None of the above [NOTA]", variable=vote_selection,
                value=0, borderwidth=1, bg=app_bg, fg=dark_font, pady=10,
                command=setvar).pack(fill="x", anchor=W)
    Button(vote_frame, text="Submit Vote",
           command=lambda candidate_id=setvar, vframe=vote_frame, sframe=sframe:
           submit_vote(candidate_id, vframe, sframe)).pack(fill="x", pady=20)

    vote_frame.pack(expand=True)
    election_window.configure(background=app_bg)


def get_person__from_fingerprint(fingerprint_data):
    # return {}
    return {"id": 1, "Name": "Alan", "Age": "27", "Mobile": "8056776065", "Constituency": "Thanjavur",
            "constituency_id": 1}


def identify_person(fingerprint_data, sframe):
    user = get_person__from_fingerprint(fingerprint_data)
    if len(user) > 0:
        # show new screen here
        # http://stackoverflow.com/questions/10267465/showing-and-hiding-widgets
        # http://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
        sframe.pack_forget()
        id_frame = Frame(election_window, bg=app_bg)

        Label(id_frame, anchor=CENTER, text="Citizen Identity", bg=splash_bg, fg=light_font, padx=60,
              font=freesans18).pack(fill="x", expand=True, pady=30)

        for key in user:
            if key != 'id' and key != 'constituency_id':
                Label(id_frame, anchor=W, text=key + ": " + user[key], bg=app_bg, fg=dark_font, font=freesans14) \
                    .pack(fill="x", pady=10, padx=10)

        # https: // www.tutorialspoint.com / python3 / tk_button.htm
        Button(id_frame, text="Vote", command=lambda c_id=user['constituency_id'], u_id=user['id'], idframe=id_frame,
               sframe=sframe: start_voting(c_id, u_id, idframe, sframe)).pack(fill="x", pady=10)
        id_frame.pack(expand=True)
        election_window.configure(background=app_bg)
    else:
        # show error
        err_msg = Label(sframe, anchor=CENTER, bg=splash_bg, fg=error_txt,
                        font=freesans14, text='could not identify user, try again.')
        err_msg.pack()
        # http://stackoverflow.com/questions/11103741/python-tkinter-hide-a-widget-after-some-time
        sframe.after(3000, err_msg.pack_forget)


election_window = Tk()

# http://www.drewkeller.com/blog/comparison-fonts-similar-helvetica-and-arial-raspberry-pi
# http://stackoverflow.com/a/4073037/1649003
freesans12 = tkfont.Font(root=election_window, family="FreeSans", size=12)
freesans14 = tkfont.Font(root=election_window, family="FreeSans", size=14)
freesans18 = tkfont.Font(root=election_window, family="FreeSans", size=18)
freesans12Bold = tkfont.Font(root=election_window, family="FreeSans", size=12, weight='bold')
freesans14Bold = tkfont.Font(root=election_window, family="FreeSans", size=14, weight='bold')
splash_bg = '#0078d7'
app_bg = '#ffffff'
error_txt = '#c62828'
list_bg = '#c8e6c9'
dark_font = '#373737'
light_font = '#ffffff'

splash_frame = Frame(election_window, bg=splash_bg)
intro_msg1 = Label(splash_frame, anchor=CENTER, text='Welcome!', bg=splash_bg, fg=light_font, font=freesans18)
intro_msg2 = Label(splash_frame, anchor=CENTER, bg=splash_bg, fg=light_font,
                   font=freesans14, text='Please place your finger on the sensor')

# http://www.flaticon.com/free-icon/fingerprint-with-crosshair-focus_25927
# http://effbot.org/tkinterbook/photoimage.htm
# http://stackoverflow.com/questions/26080763/how-to-add-a-partially-transparent-image-to-tkinter
image = Image.open('fingerprint-with-crosshair-focus.gif')
print(image.mode)
fingerprint_icon = ImageTk.PhotoImage(image)
icon_label = Label(splash_frame, anchor=CENTER, bg=splash_bg, fg=light_font, image=fingerprint_icon)
icon_label.image = fingerprint_icon

intro_msg1.pack(fill="x")
intro_msg2.pack(fill="x", pady=20)
icon_label.pack(fill="x", pady=10)
# http://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget
icon_label.bind('<Button-1>', lambda event, sframe=splash_frame: identify_person(1, sframe))
splash_frame.pack(expand=True)

election_window.title("Election")
# http://stackoverflow.com/questions/32090792/how-to-center-widgets-vertically-and-horizontally-in-window-with-tkinter
election_window.configure(background=splash_bg)
election_window.wm_geometry(newGeometry="%dx%d%+d%+d" % (300, 500, 100, 100))
election_window.mainloop()
