import os

filename = 'stu.txt'


def main():
    while True:
        menue()
        choice = int(input("请选择"))
        if choice in [0, 1, 2, 3, 4, 5, 6, 7]:
            if choice == 0:
                answer = input('你真的要退出吗？y/n')
                if answer == 'Y' or answer == 'y':
                    print('谢谢你的使用')
                    break
                else:
                    continue
            elif choice == 1:
                insert()
            elif choice == 2:
                search()
            elif choice == 3:
                delete()
            elif choice == 4:
                modify()
            elif choice == 5:
                sort()
            elif choice == 6:
                total()
            elif choice == 7:
                show()


def menue():
    print(
        '--------------------------------------------------学生信息管理系统--------------------------------------------------')
    print('\t\t\t\t\t\t1.录入学生信息')
    print('\t\t\t\t\t\t2.查找学生信息')
    print('\t\t\t\t\t\t3.删除学生信息')
    print('\t\t\t\t\t\t4.修改学生信息')
    print('\t\t\t\t\t\t5.排序')
    print('\t\t\t\t\t\t6.统计学生人数')
    print('\t\t\t\t\t\t7.显示所有学生信息')
    print('\t\t\t\t\t\t0.退出')


def insert():
    stulist = []
    while True:
        id = input('请输入id(如1001)')
        if not id:
            break
        name = input('请输入姓名')
        if not name:
            break
        try:
            English = int(input('请输入英语成绩'))
            Java = int(input('请输入Java成绩'))
            Python = int(input('请输入Python成绩'))
        except ValueError:
            print('输入无效！请重新输入整数类型')
            continue
        stu = {'id': id, 'name': name, 'English': English, 'Java': Java, 'Python': Python}
        stulist.append(stu)
        answer = input('是否再次录入信息?y/n')
        if answer == 'y' or answer == 'Y':
            continue
        else:
            break
    save(stulist)
    print("学生信息录入完毕")


def save(lst):
    try:
        stu_txt = open(filename, 'a', encoding='utf-8')  # 这里为什么异常？
    except ValueError:
        stu_txt = open(filename, 'w', encoding='utf-8')
    for item in lst:
        # 换行录入
        stu_txt.write(str(item) + '\n')
    stu_txt.close()


def search():
    while True:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as sfile:
                student_old = sfile.readlines()
                answer = input('请输入查询方式1/2,1为id，2为姓名,或者退出，请输入tc')
                if answer == '1':
                    while True:
                        student_id = input("请输入学生id")
                        studentflag = ''
                        for item in student_old:
                            d = dict(eval(item))
                            if d['id'] == student_id:
                                studentflag = d['id']
                            if studentflag != '':
                                print('学生信息为：id：{0}，name：{1}，python：{2}，java:{3},english:{4}'.format(d['id'], d['name'],
                                                                                                     d['Python'],
                                                                                                     d['Java'],
                                                                                                     d['English']))
                            else:
                                print('没有其信息，请重新输入')
                        answer2 = input('是否继续查询y/n')
                        if answer2 == 'y':
                            continue
                        else:
                            break
                elif answer == '2':
                    while True:
                        student_name = input("请输入学生name")
                        studentflag = ''
                        for item in student_old:
                            d = dict(eval(item))
                            if d['name'] == student_name:
                                studentflag = d['name']
                            if studentflag != '':
                                print('学生信息为：id：{0}，name：{1}，python：{2}，java:{3},english:{4}'.format(d['id'], d['name'],
                                                                                                     d['Python'],
                                                                                                     d['Java'],
                                                                                                     d['English']))
                            else:
                                print('没有其信息，请重新输入')
                        answer2 = input('是否继续查询y/n')
                        if answer2 == 'y':
                            continue
                        else:
                            break
                else:
                    break
        else:
            break


def delete():
    while True:
        student_id = input("请输入学生id")
        if student_id != '':
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as file:
                    # readlines将文本每一行作为独立对象的字符串对象，并将对象放入列表中返回
                    student_old = file.readlines()
            else:
                student_old = []
            # 标记是否删除
            flag = False
            if student_old:
                with open(filename, 'w', encoding='utf-8') as wfile:
                    for item in student_old:
                        d = dict(eval(item))
                        if d['id'] != student_id:
                            wfile.write(str(d) + '\n')
                            # 把不是要删除的id，覆盖并重新写入，删除id不写入等于删除
                        else:
                            flag = True
                    # 等全部遍历完，如果由学生id信息，标记flag已经变为True
                    if flag:
                        print(f'id为{student_id}的学生信息已被删除')
                    else:
                        print(f'没有找到{student_id}的学生')
            else:
                print('无学生信息')
                break
            show()
            answer = input('是否继续删除？y/n\n')
            if answer == 'y':
                continue
            else:
                break


def modify():
    show()
    # 判断文件是否存在，如果存在就生成一个student_old
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as rfile:
            student_old = rfile.readlines()
    else:
        # 不存在就结束函数
        return
    student_id = input('请输入要修改学生的id')
    with open(filename, 'w', encoding='utf-8') as wfile:
        # 遍历student_old
        for item in student_old:
            d = dict(eval(item))
            if d['id'] == student_id:
                print('已找到学生，可以开始修改')
                # while循环的作用->让输入的信息正确
                while True:
                    try:
                        d['name'] = input('请输入姓名')
                        d['English'] = input('请输入英语成绩')
                        d['Python'] = input('请输入Python成绩')
                        d['Java'] = input('请输入Java成绩')
                    except ValueError:
                        print("输入错误")
                    else:
                        # 没有异常就执行
                        break
                wfile.write(str(d) + '\n')
            else:
                wfile.write(str(d) + '\n')
        answer = input('是否继续修改?y/n')
        if answer == 'y':
            modify()


def sort():
    pass


def total():
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as tfile:
            student_total = tfile.readlines()
            t = 0
            for _ in student_total:
                t += 1
            print('学生总人数认为：' + str(t))
    else:
        print('file is not exist')


def show():
    pass


if __name__ == '__main__':
    main()
