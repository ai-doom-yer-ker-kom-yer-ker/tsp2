import tkinter as tk
import math
from tkinter import messagebox
import pandas as pd

def calculate():
    try:
        tt=10
        r = float(percent.get())/100
        t = int(forvard.get())
        k = int(futurs.get())
        n = int(period.get())
        sigma= float(volatil.get())
        u=math.exp(sigma*(tt/n)**(1/2))
        d=1/u
        p=(math.exp(r*tt/n)-d)/(u-d)
        q=1-p
        strike=0.7
        strike2=0.8
        base=pd.DataFrame(columns=['t0','t1','t2','t3','t4','t5','t6','t7','t8','t9','t10'],index=range(0,11))

        init=base.copy()
        for i in range(0,11):
            if i==0:
                init.iloc[[i],[i]]=r
                for j in range(i+1,11):
                    init.iloc[[i],[j]]=init.iloc[[i],[j-1]]*d
            else:
                init.iloc[[i],[i]]=init.iloc[[i-1],[i-1]]*u
                for j in range(i+1,11):
                    init.iloc[[i],[j]]=init.iloc[[i],[j-1]]*d

        zcb10=base.copy()
        zcb10['t10']=1
        for i in range(1,11):
            for j in range(0,11-i):
                zcb10.iloc[[j],[10-i]]=(p*zcb10.iloc[j+1,11-i]+q*zcb10.iloc[j,11-i])/(1+init.iloc[j,10-i])

        zcbt=base.iloc[:t+1,:t+1].copy()
        zcbt[f't{t}']=1
        for i in range(1,t+1):
            for j in range(0,t+1-i):
                zcbt.iloc[[j],[t-i]]=(p*zcbt.iloc[j+1,t+1-i]+q*zcbt.iloc[j,t+1-i])/(1+init.iloc[j,t-i])

        nocoupon=zcb10.iloc[0,0]/zcbt.iloc[0,0]

        zov=base.iloc[:k+1,:k+1].copy()
        zov[f't{k}']=zcb10.loc[:k+1,f't{k}']
        for i in range(1,k+1):
            for j in range(0,k+1-i):
                zov.iloc[[j],[k-i]]=(p*zov.iloc[j+1,k+1-i]+q*zov.iloc[j,k+1-i])

        svo=base.iloc[:k+1,:k+1].copy()
        for j, x in enumerate(zov[f't{k}']):
            svo.loc[j,f't{k}']=max(0,x-strike)
        for i in range(1,k+1):
            for j in range(0,k+1-i):
                svo.iloc[[j],[k-i]]=max(max(zcbt.iloc[j,k-i]-strike,0),((p*svo.iloc[j+1,k+1-i]+q*svo.iloc[j,k+1-i])/math.exp(r*tt/k)))

        goyda=svo.copy()
        for i in range(1,k+1):
            for j in range(0,k+1-i):
                goyda.iloc[[j],[k-i]]=max(max(zcbt.iloc[j,k-i]-strike2,0),((p*goyda.iloc[j+1,k+1-i]+q*goyda.iloc[j,k+1-i])/math.exp(r*tt/k)))

        label_result.config(text=f"Результат:\nZCB10: {(zcb10.iloc[0,0])*100:.2f}%\n ZCBt: {(zcbt.iloc[0,0])*100:.2f}%\n Ft: {nocoupon:.2f}\n Фьючурс: {(zov.iloc[0,0])*100:.2f}%\n Американский опцион, E=70%: {(svo.iloc[0,0])*100:.2f}%\n Американский опцион, E=80%: {(goyda.iloc[0,0])*100:.2f}%")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите значения во все поля")

# Создаем окно
root = tk.Tk()
root.title("nag36 lab2 tsp")
root.geometry("300x500")

# Поля ввода
tk.Label(root, text="r, %:").pack(pady=5)
percent = tk.Entry(root)
percent.pack()
percent.insert(0,"5")

tk.Label(root, text="t:").pack(pady=5)
forvard = tk.Entry(root)
forvard.pack()
forvard.insert(0,"7")

tk.Label(root, text="k:").pack(pady=5)
futurs = tk.Entry(root)
futurs.pack()
futurs.insert(0,"4")

tk.Label(root, text="n:").pack(pady=5)
period = tk.Entry(root)
period.pack()
period.insert(0,"10")

tk.Label(root, text="sigma:").pack(pady=5)
volatil = tk.Entry(root)
volatil.pack()
volatil.insert(0,"0.1")

# Кнопка
tk.Button(root, text="Рассчитать", command=calculate).pack(pady=10)

# Поле вывода (Label)
label_result = tk.Label(root, text="Результат: ", font=("Arial", 12))
label_result.pack(pady=10)

# Запуск программы
root.mainloop()