import tkinter as tk
import pandas as pd
from tkinter import ttk
import matplotlib.pyplot as plt
import sys
import os

app = tk.Tk()
app.geometry("1000x1000")
app.title("Проект")

label1 = tk.Label(text="Выберите акцию:")
label1.pack()

scroll_bar = tk.Scrollbar(app)

scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

stock = tk.StringVar(app)
stock.set("Акция")
stock = tk.Listbox(app, width=40, height=10, selectmode=tk.SINGLE)
stock.insert(1, 'aadr')
stock.insert(2, 'aaxj')
stock.insert(3, 'acim')
stock.insert(4, 'acwi')
stock.insert(5, 'acwv')
stock.insert(6, 'acwx')
stock.insert(7, 'adra')
stock.insert(8, 'adrd')
stock.insert(9, 'adre')
stock.insert(10, 'adru')
stock.insert(11, 'afk')
list_selected = []
stock.pack()


def selectedItem():
    '''
         Данная функция фиксирует ввыбранную пользователем акцию
    '''
    for i in stock.curselection():
        list_selected.append(stock.get(i))


def fixFirstAndLastDate(name):
    """
    Данная функция формирует первую и последнюю дату в датасете
    """

    label = tk.Label(text="Выберите время отслеживания хода цены акции:", font=("Arial", 14))
    label.pack()

    # space1 = tk.Label(text="", font=("Arial", 14))
    # space1.pack()
    label4 = tk.Label(text="Формат ввода: год-месяц-день")
    label4.pack()

    df = pd.read_csv(name)
    times = tk.Label(text=f'Первая дата в датасете: {df.Date[0]}')
    times.pack()

    timef = tk.Label(text=f'Последняя дата в датасете: {df.Date[df.shape[0] - 1]}')
    timef.pack()

    label2 = tk.Label(text="Время начала:")
    label2.pack()
    app.time1 = tk.Entry(app)  # .pack(padx=8, pady=8)
    app.time1.pack()
    time = []

    def fixInputTimeStart():
        '''
         Данная функция фиксирует введенное пользователем время начала отслеживания хода цены акции
        '''
        # print('#')
        time_start1 = app.time1.get()
        # print(time_start1)
        time.append(time_start1)


    def printInputTimeFinish():
        '''
        Формирует окно ввода времени окончания датасета
        '''
        label3 = tk.Label(text="Время окончания:")
        label3.pack()
        app.time2 = tk.Entry()  # .pack(padx=8, pady=8)
        app.time2.pack()

        def fixInputTimeFinish():
            '''
                 Данная функция фиксирует введенное пользователем время конца отслеживания хода цены акции
            '''
            # print('#')
            time_start2 = app.time2.get()
            time.append(time_start2)
            # print(time)

        def finalButton():
            btn = tk.Button(app, text="Увидеть статистику данной акции!", command=function_of_the_app,
                            activebackground='blue')
            btn.pack()

        btn2 = tk.Button(app, text='Продолжить', command=lambda: [fixInputTimeFinish(), finalButton()], bg='red')
        btn2.pack()

        # print(time)

        def printPlotStock(df):
            '''
            Данная функция рисует график изменения цены акции
            '''
            up = df[df.Close >= df.Open]

            down = df[df.Close < df.Open]
            col1 = 'green'
            col2 = 'red'
            width = 30
            width2 = 3

            plt.bar(up.index, up.Close - up.Open, width, bottom=up.Open, color=col1)
            plt.bar(up.index, up.High - up.Close, width2, bottom=up.Close, color=col1)
            plt.bar(up.index, up.Low - up.Open, width2, bottom=up.Open, color=col1)

            plt.bar(down.index, down.Close - down.Open, width, bottom=down.Open, color=col2)
            plt.bar(down.index, down.High - down.Open, width2, bottom=down.Open, color=col2)
            plt.bar(down.index, down.Low - down.Close, width2, bottom=down.Close, color=col2)

            plt.show()

        def printStatisticTable(df_1):
            '''
            Данная функция выводит таблицу с основной статистикой по акции
            '''
            list_rows = []
            list_ind = list(df_1.index)
            list_col = list(df_1.columns)
            list_col.insert(0, 'index')
            # print(list_ind)
            for i in range(df_1.shape[0]):
                tp = list(df_1.iloc[i])
                tp.insert(0, list_ind[i])
                list_rows.append(tuple(tp))
            # print(list_rows)
            # print(list_col)
            tree = ttk.Treeview(columns=list_col, show="headings")
            tree.pack(fill=tk.BOTH, expand=1)

            tree.heading(f"{list_col[0]}", text="Index")
            tree.heading(f"{list_col[1]}", text="Open")
            tree.heading(f"{list_col[2]}", text="High")
            tree.heading(f"{list_col[3]}", text="Low")
            tree.heading(f"{list_col[4]}", text="Close")
            tree.heading(f"{list_col[5]}", text="Volume")

            for row in list_rows:
                tree.insert("", tk.END, values=row)

        def analysesOfTheStock(name):
            '''
            Подгатовка датасета для формирования графика и таблицы со статистикой
            '''
            df = pd.read_csv(name)
            df.drop('OpenInt', axis=1, inplace=True)
            if len(time) < 2:
                label4 = tk.Label(
                    text="К сожалению, Вы не ввели время, поэтому анализ будет проведен по всему датасету.")
                label4.pack()
                # print('К сожалению Вы не ввели время, поэтому анализ будет проведен по всему датасету.')
                df.set_index('Date', inplace=True)
                df.index = pd.to_datetime(df.index)
                # print(time)
                # print(df[time[0]])
                df_1 = pd.DataFrame(df.describe())
                # print(df_1.iloc[1])
                printStatisticTable(df_1)
                printPlotStock(df)

            else:
                if time[0] == ' ':
                    print(time[0])
                    inds = 0
                elif list(df.Date).count(time[0]) == 0:
                    label4 = tk.Label(
                        text="К сожалению, информация о данной акции на дату начала отсутствует, поэтому была взята первая дата в датасете.")
                    label4.pack()
                    inds = 0
                elif list(df.Date).count(time[0]) != 0:
                    inds = list(df.Date).index(time[0])
                if time[1] == ' ':
                    indf = df.shape[0]
                elif list(df.Date).count(time[1]) == 0:
                    label4 = tk.Label(
                        text="К сожалению, информация о данной акции на дату конец отсутствует, поэтому была взята последняя дата в датасете.")
                    label4.pack()
                    indf = df.shape[0]
                elif list(df.Date).count(time[1]) != 0:
                    indf = list(df.Date).index(time[1])
                    # print(indf)
                    # print(df.shape[0])

                df = df.iloc[inds:indf]

                df.set_index('Date', inplace=True)
                df.index = pd.to_datetime(df.index)
                df_1 = pd.DataFrame(df.describe())
                printStatisticTable(df_1)
                printPlotStock(df)



        def function_of_the_app():
            '''
                 Данная функция выводит статистику выбранной ранее акции. А именно:\
                 count, mean, std, 25%, 50%, 75% и график хода ее цены.
            '''
            for i in list_selected:
                if i == 'aadr':
                    analysesOfTheStock('aadr.us.csv')

                if i == 'aaxj':
                    analysesOfTheStock('aaxj.us.csv')

                if i == 'acim':
                    analysesOfTheStock('acim.us.csv')

                if i == 'actx':
                    analysesOfTheStock('actx.us.csv')

                if i == 'acwv':
                    analysesOfTheStock('acwv.us.csv')

                if i == 'acwi':
                    analysesOfTheStock('acwi.us.csv')

                if i == 'acwx':
                    analysesOfTheStock('acwx.us.csv')

                if i == 'adra':
                    analysesOfTheStock('adra.us.csv')

                if i == 'adrd':
                    analysesOfTheStock('adrd.us.csv')

                if i == 'adre':
                    analysesOfTheStock('adre.us.csv')

                if i == 'adru':
                    analysesOfTheStock('adru.us.csv')

                if i == 'afk':
                    analysesOfTheStock('afk.us.csv')

                def restartProgramme():
                    os.execl(sys.executable, sys.executable, *sys.argv)
                #
                tk.Button(app, text="Перегрузить", command=restartProgramme, activebackground='blue').pack()

    btn1 = tk.Button(app, text='Продолжить', command=lambda: [fixInputTimeStart(), printInputTimeFinish()],
                     activebackground='blue')
    btn1.pack()


def printTimeOfTheStock():
    '''
         Данная функция выводит первую и последнюю дату в датасете
    '''
    for i in list_selected:
        if i == 'aadr':
            fixFirstAndLastDate('aadr.us.csv')

        if i == 'aaxj':
            fixFirstAndLastDate('aaxj.us.csv')

        if i == 'acim':
            fixFirstAndLastDate('acim.us.csv')

        if i == 'actx':
            fixFirstAndLastDate('actx.us.csv')

        if i == 'acwv':
            fixFirstAndLastDate('acwv.us.csv')

        if i == 'acwi':
            fixFirstAndLastDate('acwi.us.csv')

        if i == 'acwx':
            fixFirstAndLastDate('acwx.us.csv')

        if i == 'adra':
            fixFirstAndLastDate('adra.us.csv')

        if i == 'adrd':
            fixFirstAndLastDate('adrd.us.csv')

        if i == 'adre':
            fixFirstAndLastDate('adre.us.csv')

        if i == 'adru':
            fixFirstAndLastDate('adru.us.csv')

        if i == 'afk':
            fixFirstAndLastDate('afk.us.csv')


btn = tk.Button(app, text='Продолжить', command=lambda: [selectedItem(), printTimeOfTheStock()],
                activebackground='blue')
btn.pack()

app.mainloop()
