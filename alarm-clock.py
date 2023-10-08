import os
import sys
import threading
import time
from tkinter import *
from tkinter import messagebox

import pyglet

WORK_PATH = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))


class ControllerThread(threading.Thread):

    def __init__(self, player):
        threading.Thread.__init__(self)
        self.player = player


def on_closing():
    answer = messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?")
    if answer:
        player.pause()
        player.next_source()
        player.delete()
        root.destroy()
        sys.exit()


def get_melodies_sheet(files):
    melodies_sheet = []
    for file in files:
        if not file.endswith('.mp3'):
            continue
        melodies_sheet.append(file)
    return melodies_sheet


def start():
    try:
        entered_hours = hour_entry.get()
        entered_minutes = minutes_entry.get()
        current_hour = time.strftime('%H', time.localtime())
        current_minutes = time.strftime('%M', time.localtime())
        remaining_minutes = (int(entered_hours) - int(current_hour)) * 60 + (int(entered_minutes) - int(current_minutes))
        if remaining_minutes > -1 and (int(entered_hours) <= 23 and int(entered_minutes) <= 59):
            selected_music = variable.get()
            directory = f'{os.getcwd()}/alarms/'
            selected_music_path = f'{directory}{selected_music}'
            alarm_label['text'] = f'Будильник установлен на {entered_hours}:{entered_minutes} \n' \
                                  f'Будильник прозвенит через {remaining_minutes} мин.'
            root.update()
            i = True
            while i:
                now = str(time.strftime("%H:%M", time.localtime()))
                if now == f'{entered_hours}:{entered_minutes}' and i:
                    i = False
                    source = pyglet.media.load(selected_music_path, streaming=True)
                    player.queue(source)
                    player.play()
                    c = ControllerThread(player)
                    c.start()
                time.sleep(2)
        else:
            alarm_label['text'] = 'Проверьте вводимые данные!'
    except ValueError:
        pass


def stop():
    player.pause()
    player.next_source()


if __name__ == '__main__':
    player = pyglet.media.Player()

    root = Tk()
    root.protocol('WM_DELETE_WINDOW', on_closing)
    root.geometry("420x450")
    root.resizable(width=False, height=False)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.title('Будильник')
    iconbit = os.path.join(WORK_PATH, "iconbit.ico")
    root.iconbitmap(iconbit)

    now = time.strftime("%H:%M", time.localtime())

    label = Label(
        root,
        text=f'Текущее время: {now}',
        bg='#FFCC00',
        fg='#000000',
        bd=2,
        font='Verdana',
        width=80,
        height=2
    )
    label2 = Label(
        root,
        text='Установить будильник на:',
        bg='#DA692F',
        fg='#000000',
        bd=2,
        font='Verdana',
        width=26,
        height=1
    )
    hours_label = Label(
        root,
        text='Введите час',
        bg='#DA692F',
        fg='#000000',
        bd=2,
        font='Verdana',
        width=15,
        height=1
    )
    minutes_label = Label(
        root,
        text='Введите минуту',
        bg='#DA692F',
        fg='#000000',
        bd=2,
        font='Verdana',
        width=15,
        height=1
    )
    hour_entry = Entry(root, bg='#CECECE', font='Cambria', justify='center', width=5)
    minutes_entry = Entry(root, bg='#CECECE', font='Cambria', justify='center', width=5)

    directory = f'{os.getcwd()}/alarms/'
    os.makedirs(directory, exist_ok=True)
    files_sheet = sorted(os.listdir(directory))
    melodies = get_melodies_sheet(files_sheet)

    if not melodies:
        alarm_label = Label(
            root,
            text=f'Нет мелодий. \n'
                 f'Поместите mp3 мелодии в папку alarms, \n'
                 f'она появилась возле exe-файла',
            bg='#FFCC00',
            fg='#000000',
            bd=2,
            font='Verdana',
            width=43,
            height=5
        )

        label.pack()
        label2.place(x=0, y=60)
        hours_label.place(x=45, y=90)
        minutes_label.place(x=45, y=130)
        hour_entry.place(x=210, y=91)
        minutes_entry.place(x=210, y=131)
        alarm_label.place(x=0, y=250)
        root.mainloop()
    else:
        variable = StringVar(root)
        selector = OptionMenu(root, variable, *melodies)

        set_btn = Button(
            text="⏰ Установить будильник ⏰",
            width=35,
            height=2,
            bg='#6EA6C1',
            fg='#000000',
            font=('Verdana', 13, 'bold'),
            command=start
        )

        stop_btn = Button(
            text="Остановить мелодию",
            width=35,
            height=2,
            bg='#FF0000',
            fg='#000000',
            font=('Verdana', 13, 'bold'),
            command=stop
        )

        music_label = Label(
            root,
            text=f'Выберете мелодию:',
            bg='#FFCC00',
            fg='#000000',
            bd=2,
            font='Verdana',
            width=20,
            height=2
        )

        alarm_label = Label(
            root,
            text=f'',
            bg='#FFCC00',
            fg='#000000',
            bd=2,
            font='Verdana',
            width=43,
            height=3
        )

        label.pack()
        label2.place(x=0, y=60)
        hours_label.place(x=45, y=90)
        minutes_label.place(x=45, y=130)
        hour_entry.place(x=210, y=91)
        minutes_entry.place(x=210, y=131)
        music_label.place(x=10, y=190)
        selector.place(x=240, y=190)
        set_btn.place(x=0, y=270)
        stop_btn.place(x=0, y=325)
        alarm_label.place(x=0, y=390)
        root.mainloop()
