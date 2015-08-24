import random, tkinter

class Multiplication:
    def __init__(self):
        self._wrong_counter = 0
        self._right = 0
        self._min_num, self._max_num = (0,12)
        self._streak = 0
        
    def console_start(self):
        self._name = input('What is your name? ')
        while True:
            try:
                self._count_choice = int(input('How many times do you want to get wrong or else game over? (Choose number 1 or more) '))
                if self._valid_count_choice(self._count_choice):
                    print('You must choose a number 1 or more!')
                    continue
                break
            except ValueError:
                print('\nThat\'s not a valid number!')
                
        while not self.game_is_over(self._count_choice, self._wrong_counter):
            first, second = self.choose_numbers()
            answer = self.get_answer(first, second)
            if self.correct(answer, first, second):
                print("That's correct! Good job {}!".format(self._name))
                self.inc_right()
            else:
                print("Oh no! That's wrong {}! The correct answer was {}!".format(self._name,first*second))
                self.inc_wrong()
        print('Game over! {} got {} questions right!'.format(self._name,self._right))
                
                
    def choose_numbers(self):
        first = random.randint(self._min_num, self._max_num)
        return (first, random.randint(0,12))
    
    def get_answer(self, first, second):
        while True:
            try:
                return int(input('What is {} times {}? '.format(first,second)))
            except ValueError:
                print('That\'s not a valid number!')
        
    
    def valid_count_choice(self, count):
        return count < 1
    
    def correct_answer(self,first,sec):
        return first*sec
    
    def correct(self, answer, first, second):
        return answer == self.correct_answer(first, second)
    
    def inc_right(self):
        self._right += 1
        
    def inc_wrong(self):
        self._wrong_counter += 1
        
    def inc_streak(self):
        self._streak += 1
        
    def reset_streak(self):
        self._streak = 0
        
    def reset_counter(self):
        self._right, self._wrong_counter = (0,0)
    
    def game_is_over(self):
        return self._wrong_counter == self._count_choice

class MultiplicationApp(Multiplication):
    master = tkinter.Tk()
    
    def __init__(self, master=None):
        Multiplication.__init__(self)
        self.start_screen()
        
    def start(self):
        self.master.mainloop()
        
    def start_screen(self):
        self._canvas = tkinter.Canvas(self.master)
        self._canvas.grid()
        self._top_level()
        
        self.reset_counter()
        self.reset_streak()
        
        _welcome = tkinter.Label(self._canvas, text='Welcome to Multiplication Flash Cards!',
                                      anchor=tkinter.N, background='green',
                                      font=('Arial',40,'bold'))
        _welcome.grid(row=0, column=1, columnspan=2)
        
        
        _name_label = tkinter.Label(self._canvas, text='Name:', font=('Arial',25,'bold'), justify='right',anchor=tkinter.E)
        _name_label.grid(row=1, column=0, columnspan=2)
        default_text = tkinter.StringVar(); default_text.set('What is your name?')
        self._name_entry = tkinter.Entry(self._canvas, textvariable=default_text, 
                                         font=('Arial',25), justify='center')
        self._name_entry.grid(row=1, column=1, columnspan=2, pady=10,)
        self._name_entry.bind('<Button-1>', lambda x: default_text.set('') if self._name_entry.get() == 'What is your name?'\
                                 else None)
        self._name_entry.bind('<Return>', lambda event: self._on_start_down())
        
        _num_range_label = tkinter.Label(self._canvas, text='What numbers\nto study?', 
                                         font=('Arial',25,'bold'), justify='right',anchor=tkinter.E)
        _num_range_label.grid(row=2, column=0, columnspan=2)
        self._min_num_listbox = tkinter.Listbox(self._canvas, exportselection=False)
        self._min_num_listbox.grid(row=2, column=1, columnspan=2, pady=10)
        self._min_num_listbox.bind('<Return>', lambda event: self._on_start_down())
        self._min_num_listbox.insert(0, 'ALL NUMBERS')
        self._min_num_listbox.insert(1, '6 AND ABOVE')
        self._min_num_listbox.insert(2, '6 AND BELOW')
        self._min_num_listbox.insert(3, 'DOUBLE DIGITS')
        for n in range(0,13):
            self._min_num_listbox.insert(tkinter.END, 'only {}\'s'.format(n))
        
        _wrong_label = tkinter.Label(self._canvas, text='How many can you \nonly get wrong?', 
                                     font='Arial 20 bold', justify='right',anchor=tkinter.E)
        _wrong_label.grid(row=3, column=0, columnspan=2)
        self._wrong_lb = tkinter.Listbox(self._canvas, exportselection=False)
        self._wrong_lb.grid(row=3, column=1, columnspan=2, pady=10)
        self._wrong_lb.bind('<Return>', lambda event: self._on_start_down())
        for n in range(1,6):
            self._wrong_lb.insert(tkinter.END, n)
        
        _start_button = tkinter.Button(self._canvas, text='Start!', font='Arial 18', command=self._on_start_down)
        _start_button.grid(row=4, column=1, columnspan=2, pady=10)
        
        _quit_button = tkinter.Button(self._canvas, text='Quit', font='Arial 18', command=self._canvas.quit)
        _quit_button.grid(row=4, column=2, pady=10)
        
    def _on_start_down(self):
        self._name = self._name_entry.get() if self._name_entry.get() != 'What is your name?' else 'PLAYER'
        self._count_choice = int(self._wrong_lb.get(tkinter.ACTIVE))
        number_range = self._min_num_listbox.get(tkinter.ACTIVE)
        if number_range == 'ALL NUMBERS':
            self._min_num, self._max_num = (0,12)
        elif number_range == '6 AND ABOVE':
            self._min_num, self._max_num = (6,12)
        elif number_range == '6 AND BELOW':
            self._min_num, self._max_num = (0,6)
        elif number_range == 'DOUBLE DIGITS':
            self._min_num, self._max_num = (10,12)
        else:
            self._min_num, self._max_num = (int(number_range.split()[1].strip('\'s')),)*2
        self._canvas.destroy()
        self.create_flashcards()

    def game_over_screen(self):
        self._canvas = tkinter.Canvas(self.master)
        self._canvas.grid()
        self._top_level()
        
        _game_over = tkinter.Label(self._canvas, text='Game over!', font='Arial 50 bold')
        _game_over.grid(row=0, column=0, columnspan=2, pady=10)
        _you_got = tkinter.Label(self._canvas, text='{} got:'.format(self._name), font='Arial 50 bold')
        _you_got.grid(row=1, column=0, padx=20)
        
        _correct = tkinter.Label(self._canvas, text='{} correct'.format(self._right), font='Arial 50 bold', foreground='green')
        _correct.grid(row=1, column=1)
        
        _wrong = tkinter.Label(self._canvas, text='{} wrong'.format(self._wrong_counter), font='Arial 50 bold', foreground='red')
        _wrong.grid(row=2, column=1)
        
        main_menu = tkinter.Button(self._canvas, text='Main menu', command=self._on_mainmenu)
        main_menu.grid(row=3, column=0, columnspan=2, pady=30)
        
        _quit = tkinter.Button(self._canvas, text='Quit', command=self._canvas.quit)
        _quit.grid(row=3, column=1, pady=30)
        
    
    def _top_level(self):
        top=self._canvas.winfo_toplevel()                
        top.rowconfigure(0, weight=1)            
        top.columnconfigure(0, weight=1)
        
    def _canvas_config(self):
        self._canvas.rowconfigure(0, weight=1)           
        self._canvas.columnconfigure(0, weight=1)
        
    def update_counter_correct(self):
        self.inc_right()
        self.count_var.set('Correct: {}\nWrong: {}'.format(self._right, self._wrong_counter))
        
    def update_counter_wrong(self):
        self.inc_wrong()
        self.count_var.set('Correct: {}\nWrong: {}'.format(self._right, self._wrong_counter))
        
    def create_flashcards(self):
        self._canvas = tkinter.Canvas(self.master)
        self._canvas.grid()
        self._top_level()
        
        self.count_var = tkinter.StringVar()
        self.count_var.set('Correct: 0\nWrong: 0')
        
        self.counter = tkinter.Label(self._canvas, textvariable=self.count_var, font=('Arial',25,'bold'))
        self.counter.grid(row=0,column=0)
        
        self._main_menu = tkinter.Button(self._canvas, text='Main menu', command=self._on_mainmenu)
        self._main_menu.grid(row=20, column=2,          
            sticky=tkinter.S+tkinter.E, pady=30)
        
        self._quit = tkinter.Button(self._canvas, text='Quit', command=self._canvas.quit)
        self._quit.grid(row=20, column=3,          
            sticky=tkinter.S+tkinter.E, pady=30)
        
        self.new_numbers()
        
        self.display_numbers(self.first, self.sec)
        
        self._times = tkinter.Label(self._canvas, text='x', font=('Arial',100,'bold'))
        self._times.grid(row=2,column=0,
                         sticky=tkinter.N)

        self._line = tkinter.Label(self._canvas, text='------------------------------------------')
        self._line.grid(row=3, column=0, columnspan=2, sticky=tkinter.N)
        
        self._choose_question()
        
    def _choose_question(self):
        if len(str(self.correct_answer(self.first, self.sec))) > 1:
            random.choice([self.entry, self.multiple_choice, self.fill_in])()
        else:
            random.choice([self.entry, self.multiple_choice])()
        
    def _num_format(self, num):
        return '{}'.format(num) if len(str(num)) == 3 else\
            ' {}'.format(num) if len(str(num)) == 2 else '  {}'.format(num)
        
    def entry_answer(self):
        return self._answer.get()
    
    def display_numbers(self, first, sec):
        self._first_num = tkinter.Label(self._canvas, text='{}'.format(first) if len(str(first)) == 2 else '  {}'.format(first), font=('Arial',100,'bold'))
        self._first_num.grid(row=1,column=1,
                         sticky=tkinter.N)
        
        self._sec_num = tkinter.Label(self._canvas, text='{}'.format(sec) if len(str(sec)) == 2 else '  {}'.format(sec), font=('Arial',100,'bold'))
        self._sec_num.grid(row=2,column=1,
                         sticky=tkinter.N)
        
    def _display_correct(self):
        correct_messages = ['Good job {}!'.format(self._name), 'That\'s correct {}!'.format(self._name), 'Nice work {}!'.format(self._name)]
        self._correct_display = tkinter.Label(self._canvas, 
                                              text=random.choice(correct_messages) + ("\nThat's {} straight correct!".format(self._streak) if self._streak >= 5 else ''),
                                              font=('Arial',20,'bold'), anchor='e', foreground='green')
        self._correct_display.grid(row=0, column=1)      
        
    def _display_wrong(self):
        self._correct_display = tkinter.Label(self._canvas, text='That\'s incorrect! \n{} x {} = {}.'.format(self.first, self.sec, self.correct_answer(self.first, self.sec)),
                                              font=('Arial',20,'bold'), anchor='e', foreground='red')
        self._correct_display.grid(row=0, column=1)
        
    def _display_error(self):
        self._correct_display = tkinter.Label(self._canvas, text='Invalid entry!',
                                              font=('Arial',20,'bold'), anchor='e', foreground='red')
        self._correct_display.grid(row=0, column=1)   
        
    def new_numbers(self):
        self.first, self.sec = self.choose_numbers()
        
    def entry(self):
        default_text = tkinter.StringVar(); default_text.set('What is the answer?')
        self._answer = tkinter.Entry(self._canvas, justify='center', textvariable=default_text)
        self._answer.grid(row=4,column=1)
        self._answer.bind('<Button-1>', lambda event: default_text.set('') if self._answer.get() == 'What is the answer?'\
                                 else None)
        self._answer.bind('<Return>', lambda event: self._on_submit_down_entry())
        
        self._submit = tkinter.Button(self._canvas, text='Submit', command=self._on_submit_down_entry)
        self._submit.grid(row=4,column=2,sticky=tkinter.N)
        
    def multiple_choice(self):
        def choices_list():
            correct_answer = self.correct_answer(self.first, self.sec)
            if self.first == 0:
                return [0,1,2,3]
            elif self.sec == 0:
                return [0, self.first, random.choice([self.first-1,self.first+1]) if self.first-1 > 0 else self.first+1, random.choice([self.first-2,self.first+2]) if self.first-2 > 0 else self.first+2]
            elif 1 <= correct_answer <= 10:
                return list({correct_answer} | {correct_answer-n if correct_answer-n >= 0 else correct_answer+n for n in range(1,4)})
            return [correct_answer, random.randrange(correct_answer-10,correct_answer-3),
                       random.randrange(correct_answer+4,correct_answer+12), 
                       random.choice([i for i in range(correct_answer-3,correct_answer)]+\
                                     [i for i in range(correct_answer+1,correct_answer+4)])]

        choices = choices_list(); random.shuffle(choices)
        self._answer = tkinter.IntVar()
        self._answer.set(choices[0])
        
        self.choice1 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[0]), font=('Arial',17,'bold'), variable=self._answer, value=choices[0])
        self.choice1.grid(row=4, column=1); self.choice1.select()
        self.choice2 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[1]), font=('Arial',17,'bold'), variable=self._answer, value=choices[1])
        self.choice2.grid(row=5, column=1)
        self.choice3 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[2]), font=('Arial',17,'bold'), variable=self._answer, value=choices[2])
        self.choice3.grid(row=6, column=1)
        self.choice4 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[3]), font=('Arial',17,'bold'), variable=self._answer, value=choices[3])
        self.choice4.grid(row=7, column=1)
        
        self._canvas.bind('<Key>', lambda event: self._on_submit_down_mc())
        
        self._submit = tkinter.Button(self._canvas, text='Submit', command=self._on_submit_down_mc)
        self._submit.grid(row=7,column=2,sticky=tkinter.N)
        
    def fill_in(self):
        correct_answer = self.correct_answer(self.first, self.sec)
        
        # Displaying Incomplete answer Label
        to_replace = random.choice(str(correct_answer))
        self._answer_part = str(correct_answer).replace(to_replace, '_', 1)
        self.answer_part = tkinter.Label(self._canvas, text=self._answer_part, font=('Arial',100,'bold'))
        self.answer_part.grid(row=4, column=1)
        
        default_text = tkinter.StringVar(); default_text.set('Fill in the blank!')
        
        self.fill_in_entry = tkinter.Entry(self._canvas, justify='center', textvariable=default_text)
        self.fill_in_entry.grid(row=5, column=1)
        self.fill_in_entry.bind('<Button-1>', lambda event: default_text.set('') if self.fill_in_entry.get() == 'Fill in the blank!'\
                                 else None)
        self.fill_in_entry.bind('<Return>', lambda event: self._on_submit_down_fillin())
        
        self._submit = tkinter.Button(self._canvas, text='Submit', command=self._on_submit_down_fillin)
        self._submit.grid(row=5, column=2)
 
    def _mc_destroy(self):
        self.choice1.destroy()
        self.choice2.destroy()
        self.choice3.destroy()
        self.choice4.destroy()
        self._submit.destroy()
        
    def _entry_destroy(self):
        self._answer.destroy()
        self._submit.destroy()
        
    def _fillin_destroy(self):
        self.answer_part.destroy()
        self.fill_in_entry.destroy()
        self._submit.destroy()
        
    def _correct_wrong_destroy(self):
        self._correct_display.destroy()    
        
    def _on_mainmenu(self):
        self._canvas.destroy()
        self.start_screen()
        
    def _on_enter_entry(self, event):
        self._on_submit_down_entry()
        
    def _on_submit_down_entry(self):
        try:
            if (self._right, self._wrong_counter) != (0,0):
                self._correct_wrong_destroy()
            if self.correct(int(self.entry_answer()), self.first, self.sec):
                self.inc_streak()
                self._display_correct()
                self.update_counter_correct()
            else:
                self.reset_streak()
                self._display_wrong()
                self.update_counter_wrong()
            self._entry_destroy()
            self.new_numbers()
            self.display_numbers(self.first, self.sec)
            self._choose_question()
            if self.game_is_over():
                self._canvas.destroy()
                self.game_over_screen()
        except ValueError:
            self._display_error()
            
    def _on_submit_down_mc(self):
        if (self._right, self._wrong_counter) != (0,0):
            self._correct_wrong_destroy()
        if self.correct(self._answer.get(), self.first, self.sec):
            self.inc_streak()
            self._display_correct()
            self.update_counter_correct()
        else:
            self.reset_streak()
            self._display_wrong()
            self.update_counter_wrong()
        self._mc_destroy()
        self.new_numbers()
        self.display_numbers(self.first, self.sec)
        self._choose_question()
        if self.game_is_over():
            self._canvas.destroy()
            self.game_over_screen()
        
    def _on_submit_down_fillin(self):
        try:
            if (self._right, self._wrong_counter) != (0,0):
                self._correct_wrong_destroy()
            if self.correct(int(self._answer_part.replace('_', self.fill_in_entry.get())), 
                        self.first, self.sec):
                self.inc_streak()
                self._display_correct()
                self.update_counter_correct()
            else:
                self.reset_streak()
                self._display_wrong()
                self.update_counter_wrong()
            self._fillin_destroy()
            self.new_numbers()
            self.display_numbers(self.first, self.sec)
            self._choose_question()
            if self.game_is_over():
                self._canvas.destroy()
                self.game_over_screen()
        except ValueError:
            self._display_error()
            
        
if __name__ == '__main__':
    app = MultiplicationApp()
    app.start()         
