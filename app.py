import rumps
import pyperclip
import time
import sys
import os
from tkinter import *

sys.path.append(os.path.abspath("SO_site-packages"))
root = Tk()
root.geometry("400x400")

class AwesomeStatusBarApp(rumps.App):
    @rumps.clicked('start')
    def run_app(self, _):
        def check_for_new_values():
            options = ['first item']
            recent_value = ''

            while True:
                tmp_value = pyperclip.paste()
                print(options)

                if tmp_value != recent_value:
                    recent_value = tmp_value
                    options.append(tmp_value)

                time.sleep(3)
        check_for_new_values()

    # @rumps.clicked('dropdown')
    # def run_dropdown(self, _):
    #     def check_for_new_values():
    #         recent_value = ''
    #         options = ['first item', 'second item']
    #         clicked = StringVar()
    #         clicked.set(options[0])
    #         drop = OptionMenu(root, clicked, *options)


    #         while True:
    #             tmp_value = pyperclip.paste()
    #             print(options)

    #             if tmp_value != recent_value:
    #                 recent_value = tmp_value
    #                 options.append(tmp_value)

    #             time.sleep(3)
    #             drop.pack()
    #             root.mainloop()
    #     check_for_new_values()



        

if __name__ == "__main__":
    AwesomeStatusBarApp("Awesome App").run()
