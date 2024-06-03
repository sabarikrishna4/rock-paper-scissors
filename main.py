from typing import Tuple
import customtkinter
import random
from PIL import Image
import time
from threading import Thread
import playsound

customtkinter.set_appearance_mode("dark")


class RPS_GAME(customtkinter.CTk):
    def __init__(
        self,
    ):
        super().__init__()
        self.geometry("400x250")
        self.resizable(width=0, height=0)
        self.user_flag = False
        self.opp_flag = False

        self.rock_img = customtkinter.CTkImage(
            Image.open("Image\\rock.png"), size=(60, 60)
        )
        self.paper_img = customtkinter.CTkImage(
            Image.open("Image\\paper.png"), size=(60, 60)
        )
        self.scissor_img = customtkinter.CTkImage(
            Image.open("Image\\scissor.png"), size=(60, 60)
        )

        self.items_images = {
            self.rock_img: "Rock",
            self.paper_img: "Paper",
            self.scissor_img: "Scissor",
        }

        self.items_list = [self.rock_img, self.paper_img, self.scissor_img]

        self.rock_btn = customtkinter.CTkButton(
            self,
            text="",
            image=self.rock_img,
            width=75,
            height=75,
            fg_color="#5b5c60",
            command=lambda: self.select_btn(self.rock_img, self.rock_btn),
        )
        self.rock_btn.place(x=10, y=10)
        self.paper_btn = customtkinter.CTkButton(
            self,
            text="",
            image=self.paper_img,
            width=75,
            height=75,
            fg_color="#bdb28c",
            command=lambda: self.select_btn(self.paper_img, self.paper_btn),
        )
        self.paper_btn.place(x=10, y=90)
        self.scissor_btn = customtkinter.CTkButton(
            self,
            text="",
            image=self.scissor_img,
            width=75,
            height=75,
            fg_color="light green",
            command=lambda: self.select_btn(self.scissor_img, self.scissor_btn),
        )
        self.scissor_btn.place(x=10, y=170)

        self.btn_list = [self.rock_btn, self.paper_btn, self.scissor_btn]

        self.user_frame = customtkinter.CTkFrame(
            self, corner_radius=15, fg_color="white", width=100, height=100
        )
        self.user_frame.place(x=120, y=40)

        self.opponent_frame = customtkinter.CTkFrame(
            self, corner_radius=15, fg_color="white", width=100, height=100
        )
        self.opponent_frame.place(x=265, y=40)

        self.you_txt = customtkinter.CTkLabel(self, text="You", font=("Bold", 18))
        self.you_txt.place(x=155, y=8)
        self.opp_txt = customtkinter.CTkLabel(self, text="Opponent", font=("Bold", 18))
        self.opp_txt.place(x=275, y=8)

        self.winner_txt = customtkinter.CTkLabel(
            self, text="Winner :", font=("Bold", 18)
        )
        self.winner_txt.place(x=170, y=175)
        self.winner = customtkinter.CTkLabel(self, text="", font=("Bold", 18))
        self.winner.place(x=250, y=175)
        Thread(target=self.game_start, daemon=True).start()
        Thread(target=self.rgb_background, daemon=True).start()

    def move_sound(self):
        playsound.playsound("Sound/move.mp3")

    def game_win(self):
        playsound.playsound("Sound/game_win.mp3")

    def game_start(self):
        playsound.playsound("Sound/game_start.mp3")

    def game_over(self):
        playsound.playsound("Sound/game_over.mp3")

    def game_draw(self):
        playsound.playsound("Sound/game_draw.mp3")

    def select_btn(self, item, btn):
        Thread(target=self.move_sound, daemon=True).start()
        self.user_flag = False
        self.opp_flag = False
        self.user_item = item
        self.winner.configure(text="")
        try:
            self.select_item_btn.destroy()
        except:
            pass
        for i in self.btn_list:
            i.configure(state="disabled")
        self.select_item_btn = customtkinter.CTkButton(
            self.user_frame,
            image=item,
            text="",
            width=90,
            height=90,
            fg_color="#144870",
            corner_radius=15,
        )
        self.select_item_btn.place(x=3, y=5)
        Thread(target=self.opponent_player, daemon=True).start()

    def opponent_player(self):
        try:
            self.select_opp_btn.destroy()
        except:
            pass
        self.wait_txt = customtkinter.CTkLabel(
            self.opponent_frame,
            text="Wait...",
            width=50,
            height=50,
            fg_color="white",
            corner_radius=15,
            text_color="black",
            font=("bold", 18),
        )
        self.wait_txt.place(x=14, y=25)
        time.sleep(0.5)
        itm = random.choices(self.items_list)
        self.select_opp_btn = customtkinter.CTkButton(
            self.opponent_frame,
            image=itm[0],
            text="",
            width=90,
            height=90,
            fg_color="#144870",
            corner_radius=15,
        )
        self.select_opp_btn.place(x=3, y=5)

        self.opp_item = itm[0]
        t1 = Thread(target=self.main_fun, daemon=True)
        t1.start()
        t1.join()
        for i in self.btn_list:
            i.configure(state="enable")

    def rgb_background(self):
        while True:
            if self.user_flag == True:
                try:
                    self.user_frame.configure(fg_color="red")
                    time.sleep(0.1)
                    self.user_frame.configure(fg_color="Blue")
                    time.sleep(0.1)
                    self.user_frame.configure(fg_color="green")
                    time.sleep(0.1)
                    self.user_frame.configure(fg_color="white")
                except:
                    self.user_frame.configure(fg_color="white")
            elif self.opp_flag == True:
                try:
                    self.opponent_frame.configure(fg_color="red")
                    time.sleep(0.1)
                    self.opponent_frame.configure(fg_color="Blue")
                    time.sleep(0.1)
                    self.opponent_frame.configure(fg_color="green")
                    time.sleep(0.1)
                    self.opponent_frame.configure(fg_color="white")
                except:
                    self.opponent_frame.configure(fg_color="white")

            else:
                time.sleep(0.1)

    def main_fun(self):
        opp_itm = self.items_images.get(self.opp_item)
        user_itm = self.items_images.get(self.user_item)
        print(opp_itm)
        print(user_itm)
        if user_itm == opp_itm:
            print("Draw")
            Thread(target=self.game_draw, daemon=True).start()
            self.winner.configure(text="Draw")
            self.user_flag = False
            self.opp_flag = False
        elif user_itm == "Rock" and opp_itm == "Paper":
            self.winner.configure(text="Opponent")
            Thread(target=self.game_over, daemon=True).start()
            self.user_flag = False
            self.opp_flag = True
        elif user_itm == "Rock" and opp_itm == "Scissor":
            self.winner.configure(text="You")
            Thread(target=self.game_win, daemon=True).start()
            self.user_flag = True
            self.opp_flag = False
        elif user_itm == "Paper" and opp_itm == "Rock":
            self.winner.configure(text="You")
            Thread(target=self.game_win, daemon=True).start()
            self.user_flag = True
            self.opp_flag = False
        elif user_itm == "Paper" and opp_itm == "Scissor":
            self.winner.configure(text="Opponent")
            Thread(target=self.game_over, daemon=True).start()
            self.user_flag = False
            self.opp_flag = True
        elif user_itm == "Scissor" and opp_itm == "Rock":
            self.winner.configure(text="Opponent")
            Thread(target=self.game_over, daemon=True).start()
            self.user_flag = False
            self.opp_flag = True
        elif user_itm == "Scissor" and opp_itm == "Paper":
            self.winner.configure(text="You")
            Thread(target=self.game_win, daemon=True).start()
            self.user_flag = True
            self.opp_flag = False


if __name__ == "__main__":
    OBJ = RPS_GAME()
    OBJ.mainloop()
