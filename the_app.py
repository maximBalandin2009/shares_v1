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
            timef = tk.Label(text='Внимание! Для того, чтобы перезагрузить вкладку Вам нужно будет закрыть окно с графиком!',font=("Arial", 20))
            timef.pack()
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
            listToPlot=[]
            listDates=[]
            for i in range(0, df.shape[0]-1):
                listToPlot.append(df.Close[i])
                listDates.append(df.index[i])

            line_plot_stock,= plt.plot(listDates,listToPlot, color='blue', label = f'{list_selected[0]}')

            listSTD=[]
            listDatesSTD=[]
            for j in range(0,df.shape[0]-30):
                #print(j)
                s=0
                for i in range(30):
                    s+=df.Close[j+i]
                listSTD.append(s/30)
                print(df.index[j+30])
                print(s/30)
                listDatesSTD.append(df.index[j+30])
            line_plot_std30,=plt.plot(listDatesSTD,listSTD,color='red', label = 'скользящее среднее (за каждые 30 дней)')
            listSTD1=[]
            listDatesSTD1=[]
            for j in range(0,df.shape[0]-200):
                #print(j)
                s=0
                for i in range(200):
                    s+=df.Close[j+i]
                listSTD1.append(s/200)
                print(df.index[j+200])
                print(s/200)
                listDatesSTD1.append(df.index[j+200])
            line_plot_std200,=plt.plot(listDatesSTD1,listSTD1,color='purple', label = 'скользящее среднее (за каждые 200 дней)')
            plt.legend(handles=[line_plot_stock, line_plot_std30,line_plot_std200])
            plt.xticks(rotation=30, ha='right')
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
                list_posible_sim=['1','2','3','4','5','6','7','8','9','0','-']

                df = pd.read_csv(name)
                df.drop('OpenInt', axis=1, inplace=True)

                if time[0] == ' ':
                    print(time[0])
                    inds = 0
                elif list(df.Date).count(time[0]) == 0:
                    isNotDate=False
                    for i in list(time[0]):
                        if list_posible_sim.count(i)==0:
                            label4 = tk.Label(
                                text="К сожалению, Вы ввели не дату, поэтому была взята первая дата в датасете.")
                            label4.pack()
                            isNotDate=True
                            inds = 0
                            break
                    if list(time[0]).count('-') != 2:
                        label4 = tk.Label(
                            text="К сожалению, Вы ввели не дату, поэтому была взята первая дата в датасете.")
                        label4.pack()
                        isNotDate = True
                        inds = 0

                    if isNotDate==False:
                        timeToMake=time[0].split('-')
                        print(timeToMake)
                        timeToMake1=[]
                        for i in timeToMake:
                            timeToMake1.append(int(i))
                        for j in range(12):
                            breakCycle=False
                            for i in range(1,timeToMake1[2]):
                                strToTest = f'{timeToMake1[0]}-0{timeToMake1[1]}-{timeToMake1[2]-i}'
                                print(strToTest)
                                if list(df.Date).count(strToTest) != 0:
                                    breakCycle=True
                                    inds = list(df.Date).index(strToTest)
                                    break
                            if breakCycle==True:
                                break
                            timeToMake1[1]=timeToMake1[1]-1
                elif list(df.Date).count(time[0]) != 0:
                    inds = list(df.Date).index(time[0])
                if time[1] == ' ':
                    indf = df.shape[0]
                elif list(df.Date).count(time[1]) == 0:
                    isNotDate = False
                    for i in list(time[1]):
                        if list_posible_sim.count(i) == 0:
                            label4 = tk.Label(
                                text="К сожалению, Вы ввели не дату, поэтому была взята первая дата в датасете.")
                            label4.pack()
                            isNotDate = True
                            indf = df.shape[0]
                            break
                    if list(time[1]).count('-') != 2:
                        label4 = tk.Label(
                            text="К сожалению, Вы ввели не дату, поэтому была взята первая дата в датасете.")
                        label4.pack()
                        isNotDate = True
                        indf = df.shape[0]


                    if isNotDate == False:
                        timeToMake = time[1].split('-')
                        print(timeToMake)
                        timeToMake1 = []
                        for i in timeToMake:
                            timeToMake1.append(int(i))
                        for j in range(12):
                            breakCycle = False
                            for i in range(1, timeToMake1[2]):
                                strToTest = f'{timeToMake1[0]}-0{timeToMake1[1]}-{timeToMake1[2] - i}'
                                print(strToTest)
                                if list(df.Date).count(strToTest) != 0:
                                    breakCycle = True
                                    indf = list(df.Date).index(strToTest)
                                    break
                            if breakCycle == True:
                                break
                            timeToMake1[1] = timeToMake1[1] - 1
                elif list(df.Date).count(time[1]) != 0:
                    indf = list(df.Date).index(time[1])

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
