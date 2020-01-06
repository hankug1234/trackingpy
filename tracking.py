import math
class Location:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    @staticmethod
    def in_direction(a,b):
        ab = a.x*b.x + a.y*b.y
        abs_a = math.sqrt(a.x**2 + a.y**2)
        abs_b = math.sqrt(b.x**2 + b.y**2)

        if(ab == 0):
            return True
        cos = ab/(abs_a*abs_b)
        if((cos<=1)and(cos>=0)):
            return True
        else:
            return False

    @staticmethod
    def distance(zero,a):
        x = zero.x - a.x
        y = zero.y - a.y
        return math.fabs(math.sqrt(x**2 + y**2))

    @staticmethod
    def sub(a,b):
        re = Location(a.x - b.x,a.y - b.y)
        return re

    @staticmethod
    def normalize(a):
        d = math.sqrt(a.x**2 + a.y**2)
        re = Location(a.x/d,a.y/d)
        return re

    @staticmethod
    def cross_multiple(a,b):
        return a.x*b.y - a.y*b.x

    @staticmethod
    def ccw(a,c,d):
        n1 = Location.sub(c,a)
        n2 = Location.sub(d,a)
        n1 = Location.normalize(n1)
        n2 = Location.normalize(n2)

        cross_v = Location.cross_multiple(n1,n2)

        if(cross_v>0):
            return -1
        elif(cross_v<0):
            return 1
        else:
            return 0

    @staticmethod
    def in_threshold(p,t1,t2,t3,t4):
        c1 = Location.ccw(t1,t2,p)
        c2 = Location.ccw(t2,t3,p)
        c3 = Location.ccw(t3,t4,p)
        c4 = Location.ccw(t4,t1,p)
        if(c1 == 1):
            if(c2 == 1):
                if(c3 == 1):
                    if(c4 == 1):
                        return True
        return False


class point:
    def __init__(self,id,p,direction,r,distance):
        self.id = id
        self.p = p
        self.direction = direction
        self.r = r
        self.distance = distance

class points:
    def __init__(self,length = 0,list = list()):
        self.length = length
        self.list = list

    def make_init_points(self,p_list,id_list,r):
        self.length = len(p_list)
        for i in range(0,len(p_list)):
            new_d = point(id_list.get_id(),Location(p_list[i].x,p_list[i].y),Location(0.0,0.0),r,0.0)
            self.list.append(new_d)

    def make_points(self,p_list):
        self.length = len(p_list)
        for i in range(0, len(p_list)):
            new_d = point(-1,Location(p_list[i].x,p_list[i].y),Location(0.0,0.0),0.0,0.0)
            self.list.append(new_d)

    @staticmethod
    def make_current_to_past(current):
        new_l = list()
        for i in range(0,len(current.list)):
            if(current.list[i].id != -1):
                new_l.append(point(current.list[i].id,current.list[i].p,current.list[i].direction,current.list[i].r,current.list[i].distance))

        del current.list[0:]
        current.list = new_l
        current.length = len(new_l)



class table:
    def __init__(self,box,list=list()):
        self.box = box
        self.list = list
    @staticmethod
    def init_c(list):
        for i in range(0,len(list)):
            list[i].box = 0
    @staticmethod
    def init_i(list1,list2):
        for i in range(0, len(list1)):
            list1[i].box = list2[i].id

    def add_c(self,data):
        new_d = point(data.id,data.p,data.direction,data.r,data.distance)
        if(len(self.list == 0)):
            self.list.append(new_d)
        else:
            state = 0
            for i in range(0,len(list)):
                if(self.list[i].distance >= new_d.distance):
                    state = 1
                    self.list.insert(i,new_d)
                    break
            if(state == 1):
                self.list.append(new_d)
        self.box+=1

    def add_i(self, data, current):
        new_d = point(current, data.p, data.direction, data.r, data.distance)
        if (len(self.list == 0)):
            self.list.append(new_d)
        else:
            state = 0
            for i in range(0, len(list)):
                if (self.list[i].distance >= new_d.distance):
                    state = 1
                    self.list.insert(i, new_d)
                    break
            if (state == 1):
                self.list.append(new_d)

    def delet_c(self,id):
        if(len(self.list) != 0):
            for i in range(0, len(self.list)):
                if(self.list[i].id == id):
                    self.box -=1
                    return self.list.pop(i)
        return None

    @staticmethod
    def insert_i(list,data,current):
        for i in range(0,len(list)):
            if(list[i].box == data.id):
                list[i].add_i(data,current)
                break

    @staticmethod
    def is_all_zero(list):
        for i in range(0,len(list)):
            if(list[i].box != 0):
                return False
        return True

    @staticmethod
    def delet_all(list,index):
        del list[index].list[0:]
        list[index].box = 0





class id_state:
    def __init__(self,id,state):
        self.id = id
        self.state = state

    @staticmethod
    def state_change(list,id,state):
        for i in range(0,len(list)):
            if(list[i].id == id):
                list[i].state = state

class id_node:
    def __init__(self,id):
        self.id = id

class id_node_list:
    def __init__(self,max_id = -1,list=list()):
        self.max_id = max_id
        self.list = list

    def make_id_node(self):
        self.max_id+=1
        re = id_node(self.max_id)
        self.list.append(re)

    def get_id(self):
        if(len(self.list) == 0):
            self.make_id_node()
        re = self.list.pop(0)
        return re.id

    def free_id(self,id):
        re = id_node(id)
        self.list.append(re)


class tracking:
    def __init__(self,id_list,margin,alpha,dr,t1,t2,t3,t4):
        self.id_list = id_list
        self.margin = margin
        self.alpha = alpha
        self.dr = dr
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4

    def run(self,past,current):
        C = list()
        I = list()
        state_id = list()

        for i in range(0, past.length):
            C.append(table(0))
            state_id.append(id_state( past.list[i].id,0))

        for i in range(0, current.length):
            I.append(table(0))

        table.init_c(C)
        table.init_i(I,past.list)

        for i in range(0, past.length):
            for j in range(0, current.length):
                d1 = Location.distance(past.list[i].p,current.list[j].p)
                d2 = math.fabs(past.list[i].r - d1)
                past.list[i].distance = d2
                if(d2 < self.margin):
                    if((past.list[i].direction.x != 0.0)and(past.list[i].direction.y != 0.0)):
                        if(Location.in_direction(past.list[i].direction, Location.sub(current.list[j].p,past.list[i].p)) == True):
                            table.add_c(C,j,past.list[i])
                    else:
                        table.add_c(C,j,past.list[i])

        while(table.is_all_zero(C) == False):
            for i in range(0, current.length):
                if(C[i].box != 0):
                    table.insert_i(I,C[i].list[0])

            for i in range(0, past.length):
                s = False
                for j in range(0,len(I[i].list)):
                    if(C[I[i].list[j].id].box == 1):
                        s = True
                        num = I[i].list[j].id
                        current.list[num].id = I[i].box
                        current.list[num].distance = I[i].list[j].distance
                        new_l = Location(-I[i].list[j].p.x + current.list[num].p.x, -I[i].list[j].p.y + current.list[num].p.y)
                        current.list[num].direction = new_l
                        current.list[num].r = self.alpha*I[i].list[j].r + ((1 - self.alpha)*math.sqrt((new_l.x**2)+(new_l.y**2)))
                        id_state.state_change(state_id,I[i].box,1)
                        table.delet_all(C,num)
                        break

                if(s == True):
                    if(I[i].box != 0):
                        num = I[i].list[0].id
                        current.list[num].id = I[i].box
                        current.list[num].distance = I[i].list[0].distance
                        new_l = Location(-I[i].list[0].p.x + current.list[I[i].list[0].id].p.x,-I[i].list[0].p.y + current.list[I[i].list[0].id].p.y)
                        current.list[num].direction = new_l
                        current.list[num].r = self.alpha*I[i].list[0].r + ((1 - self.alpha)*math.sqrt((new_l.x**2)+(new_l.y**2)))
                        id_state.state_change(C,num)
                    table.delet_all(I,i)

            for i in range(0, past.length):
                    if(state_id[i].state == 1):
                        for j in range(0, current.length):
                           table.delet_c(C[j],state_id[i].id)

        for i in range(0, current.length):
            if( current.list[i].id == -1):
                current.list[i].id = self.id_list.get_id()
                current.list[i].r = self.dr
                dd = Location(0.0,0.0)
                current.list[i].direction = dd
                current.list[i].distance = 0.0

            if(Location.in_threshold(current.list[i].p,self.t1,self.t2,self.t3,self.t4) == False):
                self.id_list.free_id(current.list[i].id)
                current.list[i].id = -1

        for i in range(0, past.length):
            if(state_id[i].state == 0):
                self.id_list.free_id(state_id[i].id)










        



