from config import csv_path, start_idx, end_idx
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter.constants import W
from data_handler import DataHandler
from PIL import Image, ImageTk

class ImageAnnotater:
    def __init__(self, csv_path, start_idx, end_idx) -> None:
        self.data_handler = DataHandler(csv_path)
        self.start_idx = start_idx
        self.curr_idx = self.start_idx - 1
        if end_idx == 0:
            self.end_idx = self.data_handler.get_dataset_len()
        else: self.end_idx = end_idx

        self.curr_dic = {}

        self.window = tk.Tk()
        self.window.title('Image Annotater')
        self.window.geometry('1280x720')
        self.window.configure(background='#ececec')

        self.option_list = ['Hateful IWT Meme', 'non-Hateful IWT Meme', 'NOT IWT Meme', 'Not Sure']
        self.option_value = tk.StringVar(self.window)
        
        self.frame_img = tk.Frame(master=self.window, width=700, height=720, bg='#ececec')
        self.frame_img.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.frame_img.columnconfigure(0, weight=1, minsize=700)
        self.frame_img.rowconfigure(0, weight=1, minsize=720)

        self.frame_panel = tk.Frame(master=self.window, width=580, height=720, bg='#ececec')
        self.frame_panel.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        self.frame_panel.columnconfigure(0, weight=1, minsize=580)

        self.label_img = tk.Label(master=self.frame_img, bg='blue')
        self.label_img.grid(row=0, column=0, padx=25)

        self.frame_info = tk.Frame(master=self.frame_panel, width=580, bg='#ececec')
        self.frame_info.pack(fill=tk.X)

        self.frame_input = tk.Frame(master=self.frame_panel, width=580, bg='#ececec')
        self.frame_input.pack(fill=tk.X, side=tk.BOTTOM)
        self.frame_input.columnconfigure(0, weight=1, minsize=580)
        # self.frame_input.grid_propagate(False)

        self.label_info_topic = tk.Label(master=self.frame_info, text='Topic', bg='#ececec', fg='dim grey', font=("Arial", 14))
        self.label_info_topic.grid(row=0, sticky=W, pady=6)

        self.label_info_topic_data = tk.Label(master=self.frame_info, bg='#ececec', fg='black', font=("Arial", 18))
        self.label_info_topic_data.grid(row=1, sticky=W)

        self.label_info_hashtag = tk.Label(master=self.frame_info, text='Hashtag', bg='#ececec', fg='dim grey', font=("Arial", 14))
        self.label_info_hashtag.grid(row=2, sticky=W, pady=6)

        self.label_info_hashtag_data = tk.Label(master=self.frame_info, bg='#ececec', fg='black', font=("Arial", 18))
        self.label_info_hashtag_data.grid(row=3, sticky=W)

        self.label_info_path = tk.Label(master=self.frame_info, text='Image Path', bg='#ececec', fg='dim grey', font=("Arial", 14))
        self.label_info_path.grid(row=4, sticky=W, pady=6)

        self.label_info_path_data = tk.Label(master=self.frame_info, bg='#ececec', fg='black', font=("Arial", 18))
        self.label_info_path_data.grid(row=5, sticky=W)

        self.label_info_bodytext = tk.Label(master=self.frame_info, text='Tweet Body Text', bg='#ececec', fg='dim grey', font=("Arial", 14))
        self.label_info_bodytext.grid(row=6, sticky=W, pady=6)

        # TODO
        # self.scroll_info_bodytext = tk.Scrollbar(master=self.frame_info, troughcolor='#ececec')
        # self.scroll_info_bodytext.grid(row=7, column=1, sticky=N+S+E)

        self.text_info_bodytext = tk.Text(master=self.frame_info, bg='#ececec', fg='black', font=("Arial", 15), wrap=tk.WORD,\
                                                highlightthickness=1, highlightcolor='grey', width=60, height=10)
        self.text_info_bodytext.grid(row=7, sticky=W)
        # self.scroll_info_bodytext.config(command=self.text_info_bodytext.yview)

        self.label_input_optmenu = tk.Label(master=self.frame_input, text='Image Label', bg='#ececec', fg='dim grey', font=("Arial", 14))
        self.label_input_optmenu.grid(row=0, sticky=W, pady=6)

        self.option_value.set('Select an label')
        self.optmenu_input = tk.OptionMenu(self.frame_input, self.option_value, *self.option_list)
        self.optmenu_input.configure(fg='black')
        self.optmenu_input.grid(row=1, sticky=W, padx=(0, 300))

        self.label_input_imgtext = tk.Label(master=self.frame_input, text='Image Text', bg='#ececec', fg='dim grey', font=("Arial", 14))
        self.label_input_imgtext.grid(row=2, sticky=W, pady=6)

        self.text_input_imgtext = tk.Text(master=self.frame_input, font=("Arial", 15), wrap=tk.WORD, bg='#d4d4d4', fg='black',\
                                    highlightthickness=1, highlightcolor='grey', width=62, height=5)
        self.text_input_imgtext.grid(row=3, sticky=W)

        self.frame_input_btns = tk.Frame(master=self.frame_input, height=60)
        self.frame_input_btns.grid(row=4, pady=20)

        self.btn_previous = tk.Button(master=self.frame_input_btns, text='Previous', width=12, height=2, fg='black',\
                                font=('TkDefaultFont', 18), relief=tk.GROOVE, command=self.btn_previous_press)
        self.btn_previous.grid(row=0, column=0)

        self.btn_save = tk.Button(master=self.frame_input_btns, text='Save & Next', width=12, height=2, fg='black',\
                                font=('TkDefaultFont', 18), relief=tk.GROOVE, command=self.btn_save_press)
        self.btn_save.grid(row=0, column=1, padx=5)

        self.btn_next = tk.Button(master=self.frame_input_btns, text='Next', width=12, height=2, fg='black',\
                                font=('TkDefaultFont', 18), relief=tk.GROOVE, command=self.load_next_img)
        self.btn_next.grid(row=0, column=2, padx=(0, 20))
        
        self.window.bind('<Return>', self.key_return)
        self.window.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.load_next_img()
        self.window.mainloop()

    def load_next_dic(self):
        return self.data_handler.get_data_on_row(self.curr_idx)

    def load_next_img(self):
        self.curr_idx += 1
        self.curr_dic = self.load_next_dic()
        self.window.title('Image Annotater - No.{:<5}({} - {})'.format(self.curr_idx, self.start_idx, self.end_idx))

        img = Image.open(self.curr_dic['sample_path'])
        resized_img = img.resize(self.set_image_size(img), Image.ANTIALIAS)
        tkimg = ImageTk.PhotoImage(resized_img)
        self.label_img.configure(image=tkimg)
        self.label_img.image = tkimg

        self.label_info_topic_data.configure(text=self.curr_dic['topic'])
        self.label_info_hashtag_data.configure(text='#' + self.curr_dic['hashtag'])
        self.label_info_path_data.configure(text=self.curr_dic['sample_path'])
        self.text_info_bodytext.configure(state=tk.NORMAL)
        self.text_info_bodytext.delete('1.0', tk.END)
        self.text_info_bodytext.insert('1.0', self.curr_dic['body_text'])
        self.text_info_bodytext.configure(state=tk.DISABLED)

        self.label_input_optmenu.configure(fg='dim grey')
        # self.btn_save.configure(text='Save & Next', fg='black')
        self.option_value.set('Select an label')
        if not np.isnan(self.curr_dic['label']):
            option = -1
            if self.curr_dic['label'] == 0:
                option = 1
            elif self.curr_dic['label'] == 1:
                option = 0
            else:
                option = int(self.curr_dic['label'])
            self.option_value.set(self.option_list[option])
        
        self.text_input_imgtext.delete('1.0', tk.END)
        # if not np.isnan(self.curr_dic['image_text']):
        self.text_input_imgtext.insert('1.0', self.curr_dic['image_text'])

        if self.curr_idx == self.start_idx:
            self.btn_previous.configure(state=tk.DISABLED)
        else: self.btn_previous.configure(state=tk.NORMAL)
        
        if self.curr_idx == self.end_idx:
            self.btn_next.configure(state=tk.DISABLED)
        else: self.btn_next.configure(state=tk.NORMAL)

    def btn_previous_press(self):
        self.curr_idx -= 2
        self.load_next_img()
    
    def btn_save_press(self):
        self.label_input_optmenu.configure(fg='dim grey')
        opt = self.option_value.get()

        if opt == 'Select an label':
            self.label_input_optmenu.configure(fg='red')
            return
        elif opt == 'Hateful IWT Meme':
            self.data_handler.set_label_on_row(self.curr_idx, 1)
        elif opt == 'non-Hateful IWT Meme':
            self.data_handler.set_label_on_row(self.curr_idx, 0)
        elif opt == 'NOT IWT Meme':
            self.data_handler.set_label_on_row(self.curr_idx, 2)
        else:
            self.data_handler.set_label_on_row(self.curr_idx, 3)

        # self.btn_save.configure(text='Saved!', fg='green')
        text = self.text_input_imgtext.get('1.0', tk.END)
        if text != '\n':
            self.data_handler.set_image_text_on_row(self.curr_idx, text)

        if self.curr_idx != self.end_idx:
            self.load_next_img()

    def key_return(self, *event):
        self.window.focus_set()

    def on_closing(self):
        option = messagebox.askyesnocancel(title='Quit', message='Do you want to save the results?', default='yes')
        if option == True:
            self.data_handler.save_dataframe()
            self.window.destroy()
        elif option == False:
            print('not save')
            self.window.destroy()
        else:
            return

    def set_image_size(self, img):
        width, height = img.size
        max_width = 640
        max_height = 720
        
        if width >= height:
            new_width = max_width
            new_height = new_width * height / width
            if new_height > max_height:
                new_height = max_height
                new_width = new_height * width / height
                # print('Width {}'.format(new_width))
        else:
            new_height = max_height
            new_width = new_height * width / height
            if new_width > max_width:
                new_width = max_width
                new_height = new_width * height / width
                # print('Height {}'.format(new_heights))

        return (int(new_width), int(new_height))



if __name__ == '__main__':
    ImageAnnotater(csv_path, start_idx, end_idx)
