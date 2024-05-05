import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
import requests
from io import BytesIO
import pygame

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Family Guy Quiz")

        self.questions = [
            ("What is Peter's youngest son's name? ", "STEWIE", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyNV7ASFpNVLXGSjX_LLGqls4QgAcaItej80EeBtNFzQ&s","MP3/PGLaugh.mp3", "Damn right", "Warm up? OK! ", "MP3/SGDamn.mp3", "MP3/SGSpecial.mp3"),
            ("Who has a secret relationship with Mayor West? ", "MEG", "https://www.slashfilm.com/img/gallery/new-family-guy-tribute-to-adam-west/intro-import.jpg", "MP3/AW.mp3", "Shhh it's a secret", "Really", "MP3/Meg.mp3", "MP3/Jam.mp3"),
            ("What street do the Griffin's live on? ", "SPOONER", "https://static1.srcdn.com/wordpress/wp-content/uploads/2017/04/Family-Guy-the-Griffin-House.jpg", "MP3/FGOpening.mp3", "You probably know the house number too stalker", "You SUCK!", "MP3/RH.mp3", "MP3/WHAT.mp3"),
            ("What kind of pet does Quagmire have? ", "CAT", "https://static1.srcdn.com/wordpress/wp-content/uploads/2019/09/Quagmire-in-Family-Guy.jpg", "MP3/GGUN.mp3", "Of course he loves pussy", "Are you even trying?", "MP3/Quag.mp3", "MP3/Quagcat.mp3"),
            ("Which one of Peter's friends lives across the street? ", "CLEVELAND", "https://static.wikia.nocookie.net/familyguyfanon/images/1/10/The_Brown_House_%28Family_Guy%29.png/revision/latest?cb=20180405024241", "MP3/Giraffe.mp3", "Of course he does, except when he had his own show", "Have you ever watched the show?", "MP3/Bath.mp3", "MP3/CleveHouse.mp3")
        ]
        self.current_question_index = 0

        self.question_frame = tk.Frame(self.master)
        self.question_frame.pack()

        self.display_question()

    def display_question(self):
        question, _, image_url, sound_mp3, _, _, _, _, = self.questions[self.current_question_index]

        response = requests.get(image_url) 
        image_data = response.content
        image = Image.open(BytesIO(image_data))

        standard_size = (400, 400)

        image.thumbnail(standard_size)

        photo = ImageTk.PhotoImage(image)

        pygame.mixer.init()

        pygame.mixer.music.load(sound_mp3)

        pygame.mixer.music.play()

        if hasattr(self, "image_label"):
            self.image_label.destroy()
        self.image_label = tk.Label(self.question_frame, image=photo)
        self.image_label.image = photo 
        self.image_label.pack()

        if hasattr(self, "question_label"):
            self.question_label.destroy()
        self.question_label = tk.Label(self.question_frame, text=question)
        self.question_label.pack()

        if hasattr(self, "answer_entry"):
            self.answer_entry.destroy()
        self.answer_entry = tk.Entry(self.question_frame)
        self.answer_entry.pack()
        self.answer_entry.focus_set()

        if hasattr(self, "submit_button"):
            self.submit_button.destroy()
        self.submit_button = tk.Button(self.question_frame, text="Submit", command=self.check_answer)
        self.submit_button.pack()

        self.master.bind('<Return>', lambda event: self.check_answer())

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().upper()
        _, correct_answer, _, _, correct_response, incorrect_response, good_mp3, bad_mp3 = self.questions[self.current_question_index]

        pygame.mixer.init()

        pygame.mixer.music.load(good_mp3, bad_mp3)

        pygame.mixer.music.play()

        if user_answer == correct_answer:
            pygame.mixer.music.load(good_mp3)
            pygame.mixer.music.play()
            messagebox.showinfo("RIGHT", correct_response,)
        else:
            pygame.mixer.music.load(bad_mp3)
            pygame.mixer.music.play()
            messagebox.showerror("FAIL!", incorrect_response,)

        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            messagebox.showinfo("Completed", "You have finished the quiz!")
            self.master.destroy()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()