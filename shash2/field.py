#все что касается классов шашка и поле



#класс шашка
class Fish:
    def __init__(self,colour, koordin_sim, koordin_numb,number):
        self.colour=colour
        self.king=0
        self.koordin_sim=koordin_sim
        self.koordin_numb=koordin_numb
        self.number=number

#класс поле
class Aquarium:
    def __init__(self):
        ch=0
        self.our_zoo=[]
        self.number_white=12
        self.number_black = 12
        num=0
        for i in range(8):
            print(i)
            if i<3:
                c='black'
            else:
                c='white'
            if i==3 or i==4:
                continue
            if ch:
                #начинается с а
                for j in [chr(z) for z in range(65,73) if z%2!=0]:
                    self.our_zoo.append(Fish(c,j,i+1,num))
                    num+=1
            else:
                #начинается с в
                for j in [chr(z) for z in range(65,73) if z%2==0]:
                    self.our_zoo.append(Fish(c, j, i+1,num))
                    num+=1
            ch+=1


