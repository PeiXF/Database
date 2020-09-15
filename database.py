import tkinter
import tkinter.ttk
import tkinter.messagebox
import pyodbc


"""用来执行SQL语句，尤其是INSERT和DELETE语句"""
def doSql(sql):
    conn = pyodbc.connect(r'Driver={SQL Server}; Server=7OYK6G3WND0G5PX;'
                          r'Database=机场信息管理系统; Trusted_Connection=yes;')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


"""把数据库里的记录读取出来，然后在表格中显示"""
def bindData(sql, List):
    # 删除表格中原来的所有行
    for row in List.get_children():
        List.delete(row)

    # 读取数据库中的所有数据
    conn = pyodbc.connect(r'Driver={SQL Server}; Server=7OYK6G3WND0G5PX;'
                          r'Database=机场信息管理系统; Trusted_Connection=yes;')
    cur = conn.cursor()
    cur.execute(sql)
    temp = cur.fetchall()

    # 把数据插入表格
    for i, item in enumerate(temp):
        List.insert('', 1, values=list(item))


root = tkinter.Tk()                 # 创建tkinter应用程序窗口
root.geometry("1100x600+120+50")    # 设置窗口大小和位置
root.resizable(False, False)        # 不允许改变窗口大小
root.title("机场信息管理系统")          # 设置窗口标题


def B_pilot_click():
    global pilot
    pilot = tkinter.Tk()  # 创建tkinter应用程序窗口
    pilot.geometry("1100x600+120+50")  # 设置窗口大小和位置
    pilot.resizable(False, False)  # 不允许改变窗口大小
    pilot.title("机长")  # 设置窗口标题

    # 在窗口上放置标签组件和用于输入航班号的文本框组件
    lbFlight = tkinter.Label(pilot, text='航班号：')
    lbFlight.place(x=10, y=10, width=60, height=20)
    global entryFlight
    entryFlight = tkinter.Entry(pilot)
    entryFlight.place(x=80, y=10, width=150, height=20)
    # 创建按钮进行查询
    B_pilot_flight = tkinter.Button(pilot, text='查询', command=B_pilot_flight_click)
    B_pilot_flight.place(x=50, y=50, width=160, height=40)

    # 在窗口上放置标签组件和用于输入飞机状态的文本框组件
    lbStatus = tkinter.Label(pilot, text='飞机状态：')
    lbStatus.place(x=410, y=10, width=60, height=20)
    global entryStatus
    entryStatus = tkinter.Entry(pilot)
    entryStatus.place(x=480, y=10, width=150, height=20)
    # 创建按钮进行修改
    B_pilot_status = tkinter.Button(pilot, text='修改', command=B_pilot_status_click)
    B_pilot_status.place(x=450, y=50, width=160, height=40)


def B_pilot_status_click():
    Status = entryStatus.get().strip()
    Flight = entryFlight.get().strip()
    if Status == '':
        tkinter.messagebox.showerror(title='操作错误', message='必须输入更新后的状态')
        return
    doSql("UPDATE T_planes SET status_plane = '" + Status + "'"
          " FROM T_planes, T_flights WHERE T_planes.plane_number = T_flights.plane_number"
          " AND T_flights.flight = '" + Flight + "'")
    tkinter.messagebox.showinfo('操作完成', '修改成功')


def B_pilot_flight_click():
    Flight = entryFlight.get().strip()
    if Flight == '':
        tkinter.messagebox.showerror(title='操作错误', message='必须输入航班号')
        return

    # 显示乘客信息表格
    frame = tkinter.Frame(pilot)
    frame.place(x=300, y=200, width=520, height=360)
    # 滚动条
    scrollBar = tkinter.Scrollbar(frame)
    scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    # Treeview组件
    tree_pilot_passenger = tkinter.ttk.Treeview(frame,
                                                columns=('c1', 'c2', 'c3', 'c4', 'c5'),
                                                show="headings",
                                                yscrollcommand=scrollBar.set)
    tree_pilot_passenger.column('c1', width=100, anchor='center')
    tree_pilot_passenger.column('c2', width=100, anchor='center')
    tree_pilot_passenger.column('c3', width=100, anchor='center')
    tree_pilot_passenger.column('c4', width=100, anchor='center')
    tree_pilot_passenger.column('c5', width=100, anchor='center')
    tree_pilot_passenger.heading('c1', text='航班号')
    tree_pilot_passenger.heading('c2', text='乘客ID')
    tree_pilot_passenger.heading('c3', text='姓名')
    tree_pilot_passenger.heading('c4', text='座位号')
    tree_pilot_passenger.heading('c5', text='性别')
    tree_pilot_passenger.pack(side=tkinter.LEFT, fill=tkinter.Y)
    # Treeview组件与垂直滚动条结合
    scrollBar.config(command=tree_pilot_passenger.yview)

    bindData("SELECT * FROM pilot_passengers_V WHERE flight = '" + Flight + "'", tree_pilot_passenger)

    # 显示航班信息表格
    frame = tkinter.Frame(pilot)
    frame.place(x=50, y=120, width=1000, height=50)
    # Treeview组件
    tree_pilot_plane = tkinter.ttk.Treeview(frame,
                                            columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',\
                                                     'c9', 'c10', 'c11', 'c12', 'c13', 'c14'),
                                            show="headings")
    tree_pilot_plane.column('c1', width=60, anchor='center')
    tree_pilot_plane.column('c2', width=60, anchor='center')
    tree_pilot_plane.column('c3', width=60, anchor='center')
    tree_pilot_plane.column('c4', width=60, anchor='center')
    tree_pilot_plane.column('c5', width=50, anchor='center')
    tree_pilot_plane.column('c6', width=50, anchor='center')
    tree_pilot_plane.column('c7', width=60, anchor='center')
    tree_pilot_plane.column('c8', width=50, anchor='center')
    tree_pilot_plane.column('c9', width=50, anchor='center')
    tree_pilot_plane.column('c10', width=140, anchor='center')
    tree_pilot_plane.column('c11', width=140, anchor='center')
    tree_pilot_plane.column('c12', width=70, anchor='center')
    tree_pilot_plane.column('c13', width=70, anchor='center')
    tree_pilot_plane.column('c14', width=50, anchor='center')
    tree_pilot_plane.heading('c1', text='航班号')
    tree_pilot_plane.heading('c2', text='飞机号')
    tree_pilot_plane.heading('c3', text='机型')
    tree_pilot_plane.heading('c4', text='制造商')
    tree_pilot_plane.heading('c5', text='载客量')
    tree_pilot_plane.heading('c6', text='载油量')
    tree_pilot_plane.heading('c7', text='飞机状态')
    tree_pilot_plane.heading('c8', text='始发地')
    tree_pilot_plane.heading('c9', text='目的地')
    tree_pilot_plane.heading('c10', text='起飞时间')
    tree_pilot_plane.heading('c11', text='落地时间')
    tree_pilot_plane.heading('c12', text='航空公司')
    tree_pilot_plane.heading('c13', text='航班状态')
    tree_pilot_plane.heading('c14', text='登机口')
    tree_pilot_plane.pack(side=tkinter.LEFT, fill=tkinter.Y)
    # Treeview组件与垂直滚动条结合
    scrollBar.config(command=tree_pilot_plane.yview)

    bindData("SELECT * FROM pilot_plane_V WHERE flight = '" + Flight + "'", tree_pilot_plane)


def B_passenger_click():
    global passenger
    passenger = tkinter.Tk()  # 创建tkinter应用程序窗口
    passenger.geometry("1100x600+120+50")  # 设置窗口大小和位置
    passenger.resizable(False, False)  # 不允许改变窗口大小
    passenger.title("乘客")  # 设置窗口标题

    B_passenger_ID = tkinter.Button(passenger, text='查询', command=B_passenger_ID_click)
    B_passenger_ID.place(x=50, y=50, width=160, height=40)
    B_passenger_ID = tkinter.Button(passenger, text='退订', command=B_passenger_delete_click)
    B_passenger_ID.place(x=220, y=50, width=160, height=40)

    # 在窗口上放置标签组件和用于输入姓名的文本框组件
    lbID = tkinter.Label(passenger, text='ID：')
    lbID.place(x=10, y=10, width=40, height=20)
    global entryID
    entryID = tkinter.Entry(passenger)
    entryID.place(x=60, y=10, width=150, height=20)


def B_passenger_ID_click():
    ID = entryID.get().strip()
    if ID == '':
        tkinter.messagebox.showerror(title='操作错误', message='必须输入姓名')
        return

    # 在窗口上放置用来显示信息的表格，使用Treeview组件实现
    frame = tkinter.Frame(passenger)
    frame.place(x=50, y=100, width=1000, height=360)
    # 滚动条
    scrollBar = tkinter.Scrollbar(frame)
    scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    # Treeview组件
    tree_passenger = tkinter.ttk.Treeview(frame,
                                          columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10'),
                                          show="headings",
                                          yscrollcommand=scrollBar.set)
    tree_passenger.column('c1', width=80, anchor='center')
    tree_passenger.column('c2', width=90, anchor='center')
    tree_passenger.column('c3', width=80, anchor='center')
    tree_passenger.column('c4', width=90, anchor='center')
    tree_passenger.column('c5', width=90, anchor='center')
    tree_passenger.column('c6', width=90, anchor='center')
    tree_passenger.column('c7', width=90, anchor='center')
    tree_passenger.column('c8', width=90, anchor='center')
    tree_passenger.column('c9', width=140, anchor='center')
    tree_passenger.column('c10', width=140, anchor='center')
    tree_passenger.heading('c1', text='乘客ID')
    tree_passenger.heading('c2', text='姓名')
    tree_passenger.heading('c3', text='性别')
    tree_passenger.heading('c4', text='航班号')
    tree_passenger.heading('c5', text='座位号')
    tree_passenger.heading('c6', text='行李号')
    tree_passenger.heading('c7', text='始发地')
    tree_passenger.heading('c8', text='目的地')
    tree_passenger.heading('c9', text='起飞时间')
    tree_passenger.heading('c10', text='落地时间')
    tree_passenger.pack(side=tkinter.LEFT, fill=tkinter.Y)
    # Treeview组件与垂直滚动条结合
    scrollBar.config(command=tree_passenger.yview)

    bindData("SELECT * FROM passengers_V WHERE ID_passenger = " + ID, tree_passenger)

def B_passenger_delete_click():
    ID = entryID.get().strip()
    if ID == '':
        tkinter.messagebox.showerror(title='操作错误', message='必须输入姓名')
        return
    doSql("DELETE FROM T_abroad WHERE ID_passenger = " + ID)
    tkinter.messagebox.showinfo('操作完成', '删除成功')


def B_admin_click():
    admin = tkinter.Tk()  # 创建tkinter应用程序窗口
    admin.geometry("1100x600+120+50")  # 设置窗口大小和位置
    admin.resizable(False, False)  # 不允许改变窗口大小
    admin.title("机场管理员")  # 设置窗口标题

    # 在窗口上放置用来显示信息的表格，使用Treeview组件实现
    frame = tkinter.Frame(admin)
    frame.place(x=50, y=200, width=1000, height=360)
    # 滚动条
    scrollBar = tkinter.Scrollbar(frame)
    scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    # Treeview组件
    tree_admin = tkinter.ttk.Treeview(frame,
                                      columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'),
                                      show="headings",
                                      yscrollcommand=scrollBar.set)
    tree_admin.column('c1', width=100, anchor='center')
    tree_admin.column('c2', width=100, anchor='center')
    tree_admin.column('c3', width=100, anchor='center')
    tree_admin.column('c4', width=100, anchor='center')
    tree_admin.column('c5', width=100, anchor='center')
    tree_admin.column('c6', width=100, anchor='center')
    tree_admin.column('c7', width=190, anchor='center')
    tree_admin.column('c8', width=190, anchor='center')
    tree_admin.heading('c1', text='停机位')
    tree_admin.heading('c2', text='机位状态')
    tree_admin.heading('c3', text='登机口')
    tree_admin.heading('c4', text='登机口状态')
    tree_admin.heading('c5', text='航班号')
    tree_admin.heading('c6', text='航班状态')
    tree_admin.heading('c7', text='起飞时间')
    tree_admin.heading('c8', text='落地时间')
    tree_admin.pack(side=tkinter.LEFT, fill=tkinter.Y)
    # Treeview组件与垂直滚动条结合
    scrollBar.config(command=tree_admin.yview)

    bindData("SELECT * FROM admin_V", tree_admin)

    # 在窗口上放置标签组件和用于输入航班号的文本框组件
    lbFlight_admin = tkinter.Label(admin, text='航班号：')
    lbFlight_admin.place(x=10, y=10, width=60, height=20)
    global entryFlight_admin
    entryFlight_admin = tkinter.Entry(admin)
    entryFlight_admin.place(x=80, y=10, width=150, height=20)

    lbOrigin_time = tkinter.Label(admin, text='起飞时间：')
    lbOrigin_time.place(x=310, y=10, width=60, height=20)
    global entryOrigin_time
    entryOrigin_time = tkinter.Entry(admin)
    entryOrigin_time.place(x=380, y=10, width=150, height=20)

    lbDestination_time = tkinter.Label(admin, text='降落时间：')
    lbDestination_time.place(x=610, y=10, width=60, height=20)
    global entryDestination_time
    entryDestination_time = tkinter.Entry(admin)
    entryDestination_time.place(x=680, y=10, width=150, height=20)

    B_admin_submit = tkinter.Button(admin, text='修改', command=B_admin_submit_click)
    B_admin_submit.place(x=450, y=50, width=160, height=40)


def B_admin_submit_click():
    Destination_time = entryDestination_time.get().strip()
    Origin_time = entryOrigin_time.get().strip()
    Flight_admin = entryFlight_admin.get().strip()
    if Flight_admin == '':
        tkinter.messagebox.showerror(title='操作错误', message='必须输入航班号')
        return
    doSql("UPDATE T_flights SET origin_time = '" + Origin_time + "', destination_time = '" + Destination_time + "' "
          " FROM T_flights WHERE T_flights.flight = '" + Flight_admin + "'")
    tkinter.messagebox.showinfo('操作完成', '修改成功')


B_pilot = tkinter.Button(root, text='机长', command=B_pilot_click)
B_pilot.place(x=180, y=140, width=160, height=40)
B_passenger = tkinter.Button(root, text='乘客', command=B_passenger_click)
B_passenger.place(x=180, y=220, width=160, height=40)
B_admin = tkinter.Button(root, text='机场管理员', command=B_admin_click)
B_admin.place(x=180, y=300, width=160, height=40)


root.mainloop()


# # 在窗口上放置用于添加通信录的按钮，并设置按钮单击事件函数
# def buttonAddClick():
#     # 检查姓名
#     name = entryName.get().strip()
#     if name == '':
#         tkinter.messagebox.showerror(title='很抱歉', message='必须输入姓名')
#         return
#
#     # 所有输入都通过检查，插入数据库
#     sql = 'INSERT INTO addressList(name,sex,age,department,telephone,qq) VALUES("' \
#           + name + '","' + sex + '",' + age + ',"' + department + '","' \
#           + telephone + '","' + qq + '")'
#     doSql(sql)
#
#     # 添加记录后，更新表格中的数据
#     bindData()