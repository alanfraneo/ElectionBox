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
from PIL import Image, ImageTk
import tkinter.font as tkfont
import json
import time

class Election:
    def __init__(self, parent):
        self.parent = parent
        # http://www.drewkeller.com/blog/comparison-fonts-similar-helvetica-and-arial-raspberry-pi
        # http://stackoverflow.com/a/4073037/1649003
        self.freesans14 = tkfont.Font(self.parent, family="FreeSans", size=14)
        self.freesans18 = tkfont.Font(self.parent, family="FreeSans", size=18)
        self.splash_bg = '#0078d7'
        self.app_bg = '#ffffff'
        self.error_txt = '#c62828'
        self.list_bg = '#c8e6c9'
        self.dark_font = '#373737'
        self.light_font = '#ffffff'
        self.parent.title("Election")
        # http://stackoverflow.com/questions/32090792/how-to-center-widgets-vertically-and-horizontally-in-window-with-tkinter
        self.parent.configure(background=self.splash_bg)
        self.parent.wm_geometry(newGeometry="%dx%d%+d%+d" % (300, 500, 100, 100))
        self.splash_frame = Frame(self.parent, bg=self.splash_bg)
        self.parent.bind('<Key>', self.identify_person)
        self.show_splash_screen()

    def show_splash_screen(self):
        intro_msg1 = Label(self.splash_frame, anchor=CENTER, text='Welcome!', bg=self.splash_bg,
                           fg=self.light_font, font=self.freesans18)
        intro_msg2 = Label(self.splash_frame, anchor=CENTER, bg=self.splash_bg, fg=self.light_font,
                           font=self.freesans14, text='Please place your finger on the sensor')

        # http://www.flaticon.com/free-icon/fingerprint-with-crosshair-focus_25927
        # http://effbot.org/tkinterbook/photoimage.htm
        # http://stackoverflow.com/questions/26080763/how-to-add-a-partially-transparent-image-to-tkinter
        image = Image.open('fingerprint-with-crosshair-focus.gif')
        print(image.mode)
        fingerprint_icon = ImageTk.PhotoImage(image)
        icon_label = Label(self.splash_frame, anchor=CENTER, bg=self.splash_bg, fg=self.light_font, image=fingerprint_icon)
        icon_label.image = fingerprint_icon

        intro_msg1.pack(fill="x")
        intro_msg2.pack(fill="x", pady=20)
        icon_label.pack(fill="x", pady=10)
        # http://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget
        self.splash_frame.pack(expand=True)

    @staticmethod
    def get_person__from_fingerprint(fingerprint_data):
        identified_voter = {}
        try:
            u_id = int(fingerprint_data.char)
        except ValueError:
            u_id = 0

        with open("voter_registry.json", 'r') as voter_registry_file:
            voters_json = json.load(voter_registry_file)
            for voter in voters_json:
                if voter['voter_id'] == u_id:
                    identified_voter = voter
        return identified_voter


    def identify_person(self, fingerprint_data):
        user = self.get_person__from_fingerprint(fingerprint_data)
        if len(user) > 0:
            # show new screen here
            # http://stackoverflow.com/questions/10267465/showing-and-hiding-widgets
            # http://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
            self.splash_frame.pack_forget()
            self.id_frame = Frame(self.parent, bg=self.app_bg)
            self.parent.unbind('<Key>')
            Label(self.id_frame, anchor=CENTER, text="Citizen Identity", bg=self.splash_bg, fg=self.light_font, padx=60,
                  font=self.freesans18).pack(fill="x", expand=True, pady=30)

            for key in user:
                if '_id' not in key:
                    Label(self.id_frame, anchor=W, text=key + ": " + user[key], bg=self.app_bg, fg=self.dark_font,
                          font=self.freesans14).pack(fill="x", pady=10, padx=10)

            # https: // www.tutorialspoint.com / python3 / tk_button.htm
            Button(self.id_frame, text="Vote", command=lambda c_id=user['constituency_id']: self.start_voting(c_id))\
                .pack(fill="x", pady=10)
            self.id_frame.pack(expand=True)
            self.id_frame.update()
            self.parent.configure(background=self.app_bg)
            self.update_voted_list(user['voter_id'], user['constituency_id'])
        else:
            # show error
            err_msg = Label(self.splash_frame, anchor=CENTER, bg=self.splash_bg, fg=self.error_txt,
                            font=self.freesans14, text='could not identify user, try again.')
            err_msg.pack()
            # http://stackoverflow.com/questions/11103741/python-tkinter-hide-a-widget-after-some-time
            self.splash_frame.after(3000, err_msg.destroy)

    @staticmethod
    def update_voted_list(voter_id, constituency_id):
        with open('voted_list.csv', mode='a', encoding='UTF-8') as b_file:
            b_file.write(str(voter_id) + ',' + str(constituency_id) + ',' + str(time.time()) + '\n')

    def start_voting(self, c_id):
        vote_selection = IntVar()

        def setvar():
            return vote_selection.get()

        self.id_frame.pack_forget()
        self.vote_frame = Frame(self.parent, bg=self.app_bg)
        ballot_list = self.get_ballot_for_constituency(c_id)
        Label(self.vote_frame, anchor=CENTER, text="Choose your candidate", bg=self.splash_bg, fg=self.light_font, padx=30,
              font=self.freesans18).pack(fill="x", expand=True, pady=30)

        for candidate in ballot_list:
            Radiobutton(self.vote_frame, text=candidate['Candidate'] + ' - Party: ' + candidate['Party'],
                        variable=vote_selection, value=candidate['id'], borderwidth=1, bg=self.app_bg,
                        fg=self.dark_font, pady=10, command=setvar).pack(fill="x", anchor=W)

        Radiobutton(self.vote_frame, text="None of the above [NOTA]", variable=vote_selection, value=0, borderwidth=1,
                    bg=self.app_bg, fg=self.dark_font, pady=10, command=setvar).pack(fill="x", anchor=W)
        Button(self.vote_frame, text="Submit Vote", command=lambda candidate_id=setvar, cons_id=c_id:
        self.submit_vote(candidate_id, cons_id)).pack(fill="x", pady=20)

        self.vote_frame.pack(expand=True)
        self.parent.configure(background=self.app_bg)

    @staticmethod
    def get_ballot_for_constituency(constituency_id):

        with open("candidates_constituency_map.json", 'r') as candidates_constituency_map:
            candidates_constituency_json = json.load(candidates_constituency_map)
            candidate_list = candidates_constituency_json[str(constituency_id)]
        return candidate_list

    # this function is called when submit vote button is clicked on the voting page.
    def submit_vote(self, candidate_id, cons_id):
        # increment count in XLS and save file.
        selected_candidate = candidate_id()
        print(selected_candidate)
        # hide vote and return to splash screen
        self.vote_frame.destroy()
        self.id_frame.destroy()
        self.splash_frame.pack(expand=True)
        # http://stackoverflow.com/questions/29634742/tkinter-toplevel-widgets-not-displaying-python
        # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/universal.html
        self.splash_frame.update_idletasks()
        self.parent.bind('<Key>', self.identify_person)
        self.parent.configure(background=self.splash_bg)
        self.update_vote_tally(candidate_id(), cons_id)

    @staticmethod
    def update_vote_tally(candidate_id, cons_id):
        with open('election_results.json', 'r+') as election_results_file:
            election_results_json = json.load(election_results_file)
            for result_obj in election_results_json:
                if result_obj['consitituency_id'] == cons_id:
                    vote_tally = result_obj['vote_tally']
                    votecount = 0
                    if str(candidate_id) in vote_tally:
                        votecount = vote_tally[str(candidate_id)]
                    votecount += 1
                    vote_tally[str(candidate_id)] = votecount
            election_results_file.seek(0)  # <--- should reset file position to the beginning.
            json.dump(election_results_json, election_results_file, indent=4)
            election_results_file.truncate()


def main():
    root = Tk()
    app = Election(root)
    root.mainloop()

if __name__ == '__main__':
    main()
