import random, tkinter
from console import Multiplication



class MultiplicationApp(Multiplication):
    MASTER = tkinter.Tk()
    MASTER.title('Multiplication Flash Cards')
    
    IDLE_TIME = 999
    DEFAULT_TIMER = 5
    DEFAULT_NAME = 'PLAYER'
    MULTIPLE_CHOICE_DEFAULT_FOCUS = 1
    
    MULTIPLE_CHOICE = 'MULTIPLE CHOICE'
    FILL_IN = 'FILL IN'
    ENTRY = 'ENTRY'
    MC_DOWN = 'DOWN'
    MC_UP = 'UP'
    
    def __init__(self, MASTER=None):
        """Initializes Multiplication Flash Cards console functions and starts application."""
        Multiplication.__init__(self)
        self._timer_label = None
        self._correct_display = None
        self._type_of_question = None
        self._mc_focus = self.MULTIPLE_CHOICE_DEFAULT_FOCUS
        
        self.timer = self.IDLE_TIME
        self._timer_choice = self.DEFAULT_TIMER
        self._timer_var = tkinter.IntVar(); self._timer_var.set(self.timer)
        
        self.question_list = [self.entry, self.multiple_choice, self.fill_in]
        
        self.start_screen()
        
    def start(self):
        """Opens separate window with flash cards application."""
        self.update_timer()
        self.MASTER.mainloop() # Starts the mainloop for application
        
    def start_screen(self):
        """
        Starts the option screen before starting application.
        Different options include the name used, minimum/maximum limit, and wrong amount before game over.
        Default options are given for these choices, and includes start/quit buttons as well.
        """
        self.timer = self.IDLE_TIME
        self._canvas = tkinter.Canvas(self.MASTER)
        self._canvas.grid()
        self._top_level() # Sets start screen canvas grid and spaces for widget placements
        
        self.reset_counter()
        self.reset_streak() # Resets game counters to 0
        
        # Next several statements follow same principle:
        # Sets widget placements for start screen canvas
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
        
        _num_range_label = tkinter.Label(self._canvas, text='What numbers\nto study?', 
                                         font=('Arial',25,'bold'), justify='right',anchor=tkinter.E)
        _num_range_label.grid(row=2, column=0, columnspan=2)
        self._min_num_listbox = tkinter.Listbox(self._canvas, exportselection=False)
        self._min_num_listbox.grid(row=2, column=1, columnspan=2, pady=10)
        self._min_num_listbox.insert(0, 'ALL NUMBERS (default)')
        self._min_num_listbox.insert(1, '6 AND ABOVE')
        self._min_num_listbox.insert(2, '6 AND BELOW')
        self._min_num_listbox.insert(3, 'DOUBLE DIGITS')
        for n in range(0,13):
            self._min_num_listbox.insert(tkinter.END, 'only {}\'s'.format(n))
        
        _wrong_label = tkinter.Label(self._canvas, text='How many can you \nonly get wrong?', 
                                     font='Arial 20 bold', justify='right',anchor=tkinter.E)
        _wrong_label.grid(row=3, column=0, columnspan=2)
        self._wrong_lb = tkinter.Listbox(self._canvas, exportselection=False, height=5)
        self._wrong_lb.grid(row=3, column=1, columnspan=2, pady=10)
        for n in range(1,6):
            if n == 1:
                self._wrong_lb.insert(tkinter.END, str(n) + ' (default)')
            else:
                self._wrong_lb.insert(tkinter.END, n)
            
        _timer_label = tkinter.Label(self._canvas, text='How much time \nper question?', 
                                     font='Arial 20 bold', justify='right', anchor=tkinter.E)
        _timer_label.grid(row=4, column=0, columnspan=2)
        self._timer_lb = tkinter.Listbox(self._canvas, exportselection=False, height=5)
        self._timer_lb.grid(row=4, column=1, columnspan=2, pady=10)
        self._timer_lb.insert(tkinter.END, '5 seconds (default)')
        self._timer_lb.insert(tkinter.END, '7 seconds')
        self._timer_lb.insert(tkinter.END, '10 seconds')
        self._timer_lb.insert(tkinter.END, '15 seconds')
        self._timer_lb.insert(tkinter.END, 'NO TIMER')
        
        _question_label = tkinter.Label(self._canvas, text='What kind of questions\nto be asked?', 
                                     font='Arial 20 bold', justify='right', anchor=tkinter.E)
        _question_label.grid(row=5, column=0, columnspan=2)
        self._question_lb = tkinter.Listbox(self._canvas, exportselection=False, height=4)
        self._question_lb.grid(row=5, column=1, columnspan=2, pady=10)
        self._question_lb.insert(tkinter.END, 'ALL QUESTIONS (default)')
        self._question_lb.insert(tkinter.END, self.MULTIPLE_CHOICE)
        self._question_lb.insert(tkinter.END, self.ENTRY)
        self._question_lb.insert(tkinter.END, self.FILL_IN)

        _start_button = tkinter.Button(self._canvas, text='Start!', font='Arial 18', command=self._on_start_down)
        _start_button.grid(row=7, column=1, columnspan=2, pady=10)
        
        _quit_button = tkinter.Button(self._canvas, text='Quit', font='Arial 18', command=self.MASTER.destroy)
        _quit_button.grid(row=7, column=2, pady=10)
        
        self.MASTER.bind('<Return>', lambda event: self._on_start_down())
        self.MASTER.bind('<Down>', lambda event: None)
        self.MASTER.bind('<Up>', lambda event: None)
        
    def game_over_screen(self):
        """Opens game over screen featuring a "Main Menu" button and "Quit" button."""
        self.timer = self.IDLE_TIME
        self._canvas = tkinter.Canvas(self.MASTER)
        self._canvas.grid()
        self._top_level()
        
        # Next several statements follow same principle:
        # Sets widget placements for game-over screen canvas
        _game_over = tkinter.Label(self._canvas, text='Game over! {}x{} = {}'.format(self.first, self.sec, self.first*self.sec), 
                                                                                      font='Arial 50 bold')
        _game_over.grid(row=0, column=0, columnspan=2, pady=10)
        _you_got = tkinter.Label(self._canvas, text='{} got:'.format(self._name), font='Arial 50 bold')
        _you_got.grid(row=1, column=0, padx=20)
        
        _correct = tkinter.Label(self._canvas, text='{} correct'.format(self._right), font='Arial 50 bold', foreground='green')
        _correct.grid(row=1, column=1)
        
        _wrong = tkinter.Label(self._canvas, text='{} wrong'.format(self._wrong_counter), font='Arial 50 bold', foreground='red')
        _wrong.grid(row=2, column=1)
        
        main_menu = tkinter.Button(self._canvas, text='Main menu', command=self._on_mainmenu)
        main_menu.grid(row=3, column=0, columnspan=2, pady=30)
        
        _quit = tkinter.Button(self._canvas, text='Quit', command=self.MASTER.destroy)
        _quit.grid(row=3, column=1, pady=30)
        
        self.MASTER.bind('<Return>', lambda event: self._on_mainmenu())
        self.MASTER.bind('<Down>', lambda event: None)
        self.MASTER.bind('<Up>', lambda event: None)        
    
    def _top_level(self):
        """Configures top level for canvas window."""
        top=self._canvas.winfo_toplevel()                
        top.rowconfigure(0, weight=1)            
        top.columnconfigure(0, weight=1)
        
    def _canvas_config(self):
        """Configures canvas rows and column positions and weights."""
        self._canvas.rowconfigure(0, weight=1)           
        self._canvas.columnconfigure(0, weight=1)
        
    def update_timer(self):
        """
        Continually updates application timer during usage.
        Idle time = 999 for start screen and game over screen.
        The timer is set to what the user chose in the start screen for questions.
        """
        self.timer -= 1
        if self.timer < 1:
            self.reset_streak()
            self._display_timeout()
            self.update_counter_wrong()
            if self.game_is_over():
                self._end_game()
            else:
                if self._type_of_question == self.ENTRY:
                    self._entry_destroy()
                elif self._type_of_question == self.FILL_IN:
                    self._fillin_destroy()
                elif self._type_of_question == self.MULTIPLE_CHOICE:
                    self._mc_destroy()
                self.new_numbers()
                self.display_numbers(self.first, self.sec)
                self._choose_question()
        elif self.timer >= self.IDLE_TIME-1:
            self.timer = self.IDLE_TIME
        else:
            self._timer_var.set(self.timer)
            self._display_timer()
        self.MASTER.after(1000, self.update_timer)
        
    def update_counter_correct(self):
        """Updates correct counter along with the wrong/correct displays."""
        self.inc_right()
        self.count_var.set('Correct: {}\nWrong: {}'.format(self._right, self._wrong_counter))
        
    def update_counter_wrong(self):
        """Updates wrong counter along with the wrong/correct displays."""
        self.inc_wrong()
        self.count_var.set('Correct: {}\nWrong: {}'.format(self._right, self._wrong_counter))
        
    def create_flashcards(self):
        """Creates problem screen featuring flash card interface and counter displays."""
        self._canvas = tkinter.Canvas(self.MASTER)
        self._canvas.grid()
        self._top_level()
        
        self.count_var = tkinter.StringVar()
        self.count_var.set('Correct: 0\nWrong: 0')
        
        self.counter = tkinter.Label(self._canvas, textvariable=self.count_var, font=('Arial',25,'bold'))
        self.counter.grid(row=0,column=0)
        
        self._main_menu = tkinter.Button(self._canvas, text='Main menu', command=self._on_mainmenu)
        self._main_menu.grid(row=20, column=2,          
            sticky=tkinter.S+tkinter.E, pady=30)
        
        self._quit = tkinter.Button(self._canvas, text='Quit', command=self.MASTER.destroy)
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
        """
        Chooses a random interface for the user to answer a problem.
        This includes multiple choice, fill-in, and entry.
        """
        random.choice(self.question_list)()
        
    def _num_format(self, num):
        """Formats numbers to properly align flash card interface."""
        return '{}'.format(num) if len(str(num)) == 3 else\
            ' {}'.format(num) if len(str(num)) == 2 else '  {}'.format(num)
        
    def entry_answer(self):
        """Returns user's answer to problem."""
        return self._answer.get()
    
    def _display_timer(self):
        if self._timer_label != None:
            self._timer_label.destroy()
        self._timer_label = tkinter.Label(self._canvas, textvariable=self._timer_var, 
                                          font=('Times New Roman',35),
                                          fg='red' if self.timer <= 3 else 'black')
        self._timer_label.grid(row=0, column=2, sticky=tkinter.N)
    
    def display_numbers(self, first, sec):
        """
        Displays the two numbers in flash card interface.
        Also calls the reset timer for every question asked.
        """
        self._first_num = tkinter.Label(self._canvas, text='{}'.format(first) if len(str(first)) == 2 else '  {}'.format(first), font=('Arial',100,'bold'))
        self._first_num.grid(row=1,column=1,
                         sticky=tkinter.N)
        
        self._sec_num = tkinter.Label(self._canvas, text='{}'.format(sec) if len(str(sec)) == 2 else '  {}'.format(sec), font=('Arial',100,'bold'))
        self._sec_num.grid(row=2,column=1,
                         sticky=tkinter.N)
        self._reset_timer()
        
    def _reset_timer(self):
        """Resets timer back to what user chose in the start screen."""
        self.timer = self._timer_choice+1
        
    def _display_SSerror(self):
        """
        Command to display Start Screen Error when user attempts to choose 
        "only 0's" option with FILL IN questions only.
        (This is illegal because fill-in questions require double digit answers.)
        """
        _welcome = tkinter.Label(self._canvas, text='ERROR: You can\'t have fill in questions with only 0\'s!',
                                      anchor=tkinter.N, fg='red',
                                      font=('Arial',20,'bold'))
        _welcome.grid(row=6, column=1, columnspan=2)
        
    def _display_correct(self):
        """Displays specific "Correct" messages if user answered correctly."""
        correct_messages = ['Good job {}!'.format(self._name), 'That\'s correct {}!'.format(self._name), 'Nice work {}!'.format(self._name)]
        self._correct_display = tkinter.Label(self._canvas, 
                                              text=random.choice(correct_messages) + ("\nThat's {} straight correct!".format(self._streak) if self._streak >= 5 else ''),
                                              font=('Arial',20,'bold'), anchor=tkinter.E, foreground='green')
        self._correct_display.grid(row=0, column=1)      
        
    def _display_wrong(self):
        """Displays specific "Wrong" messages if user answered incorrectly."""
        self._correct_display = tkinter.Label(self._canvas, text='That\'s incorrect! \n{} x {} = {}.'.format(self.first, self.sec, self.correct_answer(self.first, self.sec)),
                                              font=('Arial',20,'bold'), anchor=tkinter.E, foreground='red')
        self._correct_display.grid(row=0, column=1)
        
    def _display_timeout(self):
        """"Displays specific "Wrong" messages if user ran out of time in a question."""
        self._destroy_correct_display()
        self._correct_display = tkinter.Label(self._canvas, text='Time\'s up! \n{} x {} = {}.'.format(self.first, self.sec, self.correct_answer(self.first, self.sec)),
                                              font=('Arial',20,'bold'), anchor=tkinter.E, foreground='red')
        self._correct_display.grid(row=0, column=1)
        
    def _display_error(self):
        """Displays specific "Error" messages if user entered an invalid input."""
        self._correct_display = tkinter.Label(self._canvas, text='Invalid entry!',
                                              font=('Arial',20,'bold'), anchor='e', foreground='red')
        self._correct_display.grid(row=0, column=1)   
    
    def _destroy_correct_display(self):
        """Destroys correct label after every question to create a new one."""
        if self._correct_display != None:
            self._correct_display.destroy()    
    
    def _destroy_timer(self):
        """Destroys timer label after every second has passed."""
        self._timer_label.destroy()
        
    def new_numbers(self):
        """Creates new random numbers for specific problem."""
        self.first, self.sec = self.choose_numbers()
        if self.question_list == [self.fill_in]: 
            if self.correct_answer(self.first, self.sec) < 10:
                self.new_numbers()
        
    def entry(self):
        """Creates entry box for user to answer in a "Entry Question"."""
        self._type_of_question = self.ENTRY
        default_text = tkinter.StringVar(); default_text.set('What is the answer?')
        self._answer = tkinter.Entry(self._canvas, justify='center', textvariable=default_text)
        self._answer.grid(row=4,column=1)
        self._answer.bind('<Button-1>', lambda event: default_text.set('') if self._answer.get() == 'What is the answer?'\
                                 else None)
        self._answer.bind('<Key>', lambda event: default_text.set('') if self._answer.get() == 'What is the answer?'\
                                 else None)
        self._answer.bind('<Return>', lambda event: self._on_submit_down_entry())
        
        self.MASTER.bind('<Return>', lambda event: None)
        self.MASTER.bind('<Down>', lambda event: None)
        self.MASTER.bind('<Up>', lambda event: None)
        
        self._submit = tkinter.Button(self._canvas, text='Submit', command=self._on_submit_down_entry)
        self._submit.grid(row=4,column=2,sticky=tkinter.N)
        
        self._answer.focus()
        
    def multiple_choice(self):
        """Creates four specific multiple-choice buttons for user."""
        self._type_of_question = self.MULTIPLE_CHOICE
        self._mc_focus = self.MULTIPLE_CHOICE_DEFAULT_FOCUS
        def choices_list():
            """Creates a list of possible choices in a multiple-choice problem."""
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
        self.choice1.grid(row=4, column=1)
        self.choice1.bind('<Down>', lambda event: self.choice2.select())
        self.choice2 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[1]), font=('Arial',17,'bold'), variable=self._answer, value=choices[1])
        self.choice2.grid(row=5, column=1)
        self.choice3 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[2]), font=('Arial',17,'bold'), variable=self._answer, value=choices[2])
        self.choice3.grid(row=6, column=1)
        self.choice4 = tkinter.Radiobutton(self._canvas, text=self._num_format(choices[3]), font=('Arial',17,'bold'), variable=self._answer, value=choices[3])
        self.choice4.grid(row=7, column=1)
        
        self.MASTER.bind('<Return>', lambda event: self._on_submit_down_mc())
        self.MASTER.bind('<Down>', lambda event: self._on_down_mc(self.MC_DOWN))
        self.MASTER.bind('<Up>', lambda event: self._on_down_mc(self.MC_UP))
        
        self._submit = tkinter.Button(self._canvas, text='Submit', command=self._on_submit_down_mc)
        self._submit.grid(row=7,column=2,sticky=tkinter.N)
        
        self.choice1.select()
        
    def _on_down_mc(self, direction):
        """
        Submits user's answer and updates counters, problems, 
        and game over status for multiple choice questions.
        """
        if direction == self.MC_DOWN:
            self._mc_focus += 1
        elif direction == self.MC_UP:
            self._mc_focus -= 1
        else:
            self._mc_focus = 0
            
        if self._mc_focus <= self.MULTIPLE_CHOICE_DEFAULT_FOCUS-1:
            self._mc_focus = self.MULTIPLE_CHOICE_DEFAULT_FOCUS+3
        elif self._mc_focus >= self.MULTIPLE_CHOICE_DEFAULT_FOCUS+4:
            self._mc_focus = self.MULTIPLE_CHOICE_DEFAULT_FOCUS
        
        if self._mc_focus == self.MULTIPLE_CHOICE_DEFAULT_FOCUS:
            self.choice1.select()
        elif self._mc_focus == self.MULTIPLE_CHOICE_DEFAULT_FOCUS+1:
            self.choice2.select()
        elif self._mc_focus == self.MULTIPLE_CHOICE_DEFAULT_FOCUS+2:
            self.choice3.select()
        elif self._mc_focus == self.MULTIPLE_CHOICE_DEFAULT_FOCUS+3:
            self.choice4.select()
        
    def fill_in(self):
        """Creates a fill-in-the-blank question for the user."""
        self._type_of_question = self.FILL_IN
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
        self.fill_in_entry.bind('<Key>', lambda event: default_text.set('') if self.fill_in_entry.get() == 'Fill in the blank!'\
                                 else None)
        self.fill_in_entry.bind('<Return>', lambda event: self._on_submit_down_fillin())
        
        self.MASTER.bind('<Return>', lambda event: None)
        self.MASTER.bind('<Down>', lambda event: None)
        self.MASTER.bind('<Up>', lambda event: None)
        
        self._submit = tkinter.Button(self._canvas, text='Submit', command=self._on_submit_down_fillin)
        self._submit.grid(row=5, column=2)
        
        self.fill_in_entry.focus()
 
    def _mc_destroy(self):
        """Destroys widgets for multiple choice questions."""
        self.choice1.destroy()
        self.choice2.destroy()
        self.choice3.destroy()
        self.choice4.destroy()
        self._submit.destroy()
        
    def _entry_destroy(self):
        """Destroys widgets for entry questions."""
        self._answer.destroy()
        self._submit.destroy()
        
    def _fillin_destroy(self):
        """Destroys widgets for fill-in-the-blank questions."""
        self.answer_part.destroy()
        self.fill_in_entry.destroy()
        self._submit.destroy()
        
    def _correct_wrong_destroy(self):
        """Destroys widgets for wrong/correct counters."""
        self._correct_display.destroy()   
        
    def _on_start_down(self):
        """
        Starts application after user clicks the start button.
        Sets up various options derived from previous start screen and creates first problem for flash cards.
        """
        try:
            self._name = self._name_entry.get() if self._name_entry.get() != 'What is your name?' else self.DEFAULT_NAME
            
            if self._wrong_lb.get(tkinter.ACTIVE) == '1 (default)':
                self._count_choice = 1
            else:
                self._count_choice = int(self._wrong_lb.get(tkinter.ACTIVE))
                
            number_range = self._min_num_listbox.get(tkinter.ACTIVE)
            if number_range == 'ALL NUMBERS (default)':
                self._min_num, self._max_num = (0,12)
            elif number_range == '6 AND ABOVE':
                self._min_num, self._max_num = (6,12)
            elif number_range == '6 AND BELOW':
                self._min_num, self._max_num = (0,6)
            elif number_range == 'DOUBLE DIGITS':
                self._min_num, self._max_num = (10,12)
            else:
                self._min_num, self._max_num = (int(number_range.split()[1].strip('\'s')),)*2
                
            timer_choice = self._timer_lb.get(tkinter.ACTIVE)
            if timer_choice == 'NO TIMER':
                self._timer_choice = self.IDLE_TIME
            else:
                self._timer_choice = int(timer_choice.split()[0])
                
            question_choice = self._question_lb.get(tkinter.ACTIVE)
            if question_choice == self.MULTIPLE_CHOICE:
                self.question_list = [self.multiple_choice]
            elif question_choice == self.ENTRY:
                self.question_list = [self.entry]
            elif question_choice == self.FILL_IN:
                if number_range == 'only 0\'s':
                    self._canvas.destroy()
                    self.start_screen()
                    self._display_SSerror()
                    return
                self.question_list = [self.fill_in]
                
            self._canvas.destroy() # Destroys start screen canvas
            self.create_flashcards() # Create numbers for flash cards after finishing start screen
        except:
            pass 
        
    def _on_mainmenu(self):
        """Destroys widgets for main menu and creates start screen."""
        self._canvas.destroy()
        self.start_screen()
        
    def _on_enter_entry(self, event):
        """Submits user's answer if user pressed "Enter"."""
        self._on_submit_down_entry()
        
    def _on_submit_down_entry(self):
        """
        Submits user's answer and updates counters, problems, 
        and game over status for entry questions.
        """
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
            if self.game_is_over():
                self._end_game()
            else:
                self._entry_destroy()
                self.new_numbers()
                self.display_numbers(self.first, self.sec)
                self._choose_question()
        except ValueError:
            self._display_error()
            
    def _end_game(self):
        """Ends the flash card runtime and takes """
        self._canvas.destroy()
        self.game_over_screen()
        self.timer = self.IDLE_TIME
            
    def _on_submit_down_mc(self):
        """
        Submits user's answer and updates counters, problems, 
        and game over status for multiple choice questions.
        """
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
        if self.game_is_over():
            self._end_game()
        else:
            self._mc_destroy()
            self.new_numbers()
            self.display_numbers(self.first, self.sec)
            self._choose_question()
        
    def _on_submit_down_fillin(self):
        """
        Submits user's answer and updates counters, problems, 
        and game over status for fill-in questions.
        """
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
            if self.game_is_over():
                self._end_game()
            else:
                self._fillin_destroy()
                self.new_numbers()
                self.display_numbers(self.first, self.sec)
                self._choose_question()
        except ValueError:
            self._display_error()
            
if __name__ == '__main__':
    app = MultiplicationApp()
    app.start() # Start the application when running on main module

