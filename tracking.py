import math
class tool:

    @staticmethod
    def in_direction(a,b):
        ab = a[0]*b[0] + a[1]*b[1]
        abs_a = math.sqrt(a[0]**2 + a[1]**2)
        abs_b = math.sqrt(b[0]**2 + b[1]**2)

        if(ab == 0):
            return True
        cos = ab/(abs_a*abs_b)
        if((cos<=1)and(cos>=0)):
            return True
        else:
            return False

    @staticmethod
    def distance(zero,a):
        x = zero[0] - a[0]
        y = zero[1] - a[1]
        return math.fabs(math.sqrt(x**2 + y**2))

    @staticmethod
    def sub(a,b):
        re = [a[0] - b[0],a[1] - b[1]]
        return re

    @staticmethod
    def add(a,b):
        return [a[0] + b[0],a[1] + b[1]]

    @staticmethod
    def normalize(a):
        d = math.sqrt(a[0]**2 + a[1]**2)
        re = [a[0]/d,a[1]/d]
        return re

    @staticmethod
    def g_length(a):
        return math.sqrt(a[0]**2 + a[1]**2)

    @staticmethod
    def cross_multiple(a,b):
        return a[0]*b[1] - a[1]*b[0]

    @staticmethod
    def ccw(a,c,d):
        n1 = tool.sub(c,a)
        n2 = tool.sub(d,a)
        n1 = tool.normalize(n1)
        n2 = tool.normalize(n2)

        cross_v = tool.cross_multiple(n1,n2)

        if(cross_v>0):
            return -1
        elif(cross_v<0):
            return 1
        else:
            return 0

    @staticmethod
    def in_threshold(p,t1,t2,t3,t4):
        c1 = tool.ccw(t1,t2,p)
        c2 = tool.ccw(t2,t3,p)
        c3 = tool.ccw(t3,t4,p)
        c4 = tool.ccw(t4,t1,p)
        if(c1 == 1):
            if(c2 == 1):
                if(c3 == 1):
                    if(c4 == 1):
                        return True
        return False
    @staticmethod
    def init_id_state(id_state,past_list):
        for current in past_list:
            id_state[current.id] = 0

    @staticmethod
    def init_current_table(current_table, current_list):
        for index, current in enumerate(current_list):
            current_table[index] = list()

    @staticmethod
    def init_past_table(past_table, past_list):
        for past in past_list:
            past_table[past.id] = list()

    @staticmethod
    def add_table(table, table_id, data):
        new_point = point(data.id, data.location, data.direction, data.r, data.distance, data.b_box)
        new_point.set_temporary_id(data.temporary_id)
        if (len(table[table_id]) == 0):
            table[table_id].append(new_point)
        else:
            for index,current in enumerate(table[table_id]):
                if (current.distance >= new_point.distance):
                    table[table_id].insert(index, new_point)
                    return
            table[table_id].append(new_point)

    @staticmethod
    def set_current_point_values(current,c_index,past_point,id,alpha,id_state):
        current.point_list[c_index].id = id
        current.point_list[c_index].distance = past_point.distance
        current.point_list[c_index].direction = tool.sub(current.point_list[c_index].location, past_point.location)
        current.point_list[c_index].r = alpha * past_point.r + (1 - alpha) * tool.g_length(current.point_list[c_index].direction)
        id_state[id] = 1

    @staticmethod
    def delete_point_by_id(table,table_id,target_id):
        if (len(table[table_id]) != 0):
            for index,current in enumerate(table[table_id]):
                if (current.id == target_id):
                    return table[table_id].pop(index)
        return None

    @staticmethod
    def is_all_zero(current_table):
        current_table_key_list = list(current_table.keys())
        for key in current_table_key_list:
            if (len(current_table[key]) != 0):
                return False
        return True

    @staticmethod
    def delete_all(table, table_id):
        del table[table_id][0:]


class point:
    def __init__(self,id,location,direction,r,distance,b_box):
        self.id = id
        self.location = location
        self.direction = direction
        self.r = r
        self.distance = distance
        self.b_box = b_box
        self.temporary_id = None
        self.count = 0

    def set_temporary_id(self,id):
        self.temporary_id = id

class points:
    def __init__(self,point_list = list()):
        self.point_list = point_list

    def make_init_points(self,locations,id_list,r,b_boxs):
        for index,location in enumerate(locations):
            new_point = point(id_list.get_id(),[location[0],location[1]],None,r,0.0,b_boxs[index])
            self.point_list.append(new_point)

    def make_points(self,locations,b_boxs):
        for index, location in enumerate(locations):
            new_point = point(None,[location[0],location[1]],None,0.0,0.0,b_boxs[index])
            self.point_list.append(new_point)

    @staticmethod
    def make_current_to_past(current):
        new_point_list = list()
        for p in current.point_list:
            if(p.id != None):
                new_point_list.append(point(p.id,p.location,p.direction,p.r,p.distance,p.b_box))

        del current.point_list[0:]
        current.point_list = new_point_list

class id_node_list:
    def __init__(self,max_id = 100,id_list=range(0,100)):
        self.max_id = max_id
        self.id_list = list(id_list)

    def make_id(self):
        self.max_id+=1
        self.id_list.append(self.max_id)

    def get_id(self):
        if(len(self.id_list) == 0):
            self.make_id()
        return self.id_list.pop(0)

    def free_id(self,id):
        self.id_list.append(id)


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
        self.past = points(list())

    def run(self,past,current):
        current_table = dict()
        past_table = dict()
        id_state = dict()

        tool.init_current_table(current_table,current.point_list)
        tool.init_past_table(past_table,past.point_list)
        tool.init_id_state(id_state,past.point_list)

        for p_p in past.point_list:
            for c_index,c_p in enumerate(current.point_list):
                d1 = tool.distance(p_p.location,c_p.location)
                d2 = d1
                p_p.distance = math.fabs(d2)
                if(d2 < (p_p.r + self.margin)):
                    tool.add_table(current_table,c_index,p_p)

        current_table_key_list = list(current_table.keys())
        past_table_key_list = list(past_table.keys())
        while(tool.is_all_zero(current_table) == False):
            for key in current_table_key_list:
                if(len(current_table[key]) != 0):
                    current_table[key][0].set_temporary_id(key)
                    tool.add_table(past_table,current_table[key][0].id,current_table[key][0])

            for key in past_table_key_list:
                s = False
                for p_t_p in past_table[key]:
                    temporary_id = p_t_p.temporary_id
                    if(len(current_table[temporary_id]) == 1):
                        s = True
                        tool.set_current_point_values(current, temporary_id, p_t_p, key, self.alpha,id_state)
                        tool.delete_all(current_table,temporary_id)
                        break

                if(s == False):
                    if(len(past_table[key]) > 0):
                        temporary_id = past_table[key][0].temporary_id
                        tool.set_current_point_values(current, temporary_id, past_table[key][0], key, self.alpha, id_state)
                        tool.delete_all(current_table, temporary_id)

                tool.delete_all(past_table,key)

            for c_key in current_table_key_list:
                for p_key in past_table_key_list:
                    if(id_state[p_key] == 1):
                        tool.delete_point_by_id(current_table,c_key,p_key)

        for index,c_p in enumerate(current.point_list):
            if( c_p.id == None):
                current.point_list[index].id = self.id_list.get_id()
                current.point_list[index].r = self.dr
                current.point_list[index].direction = None
                current.point_list[index].distance = 0.0

            if(tool.in_threshold(c_p.location,self.t1,self.t2,self.t3,self.t4) == False):
                self.id_list.free_id(current.point_list[index].id)
                current.point_list[index].id = None

        ret = list()
        for key in past_table_key_list:
            if(id_state[key] == 0):
                #self.id_list.free_id(key)
                ret.append(key)
        return ret


    def perform_custom_tracking(self,detected_object_with_centerbottom):
       current = points(list())
       locations = list()
       b_boxs = list()
       tracked_object = list()

       for dowc in detected_object_with_centerbottom:
          b_boxs.append([dowc[0],dowc[1],dowc[2],dowc[3]])
          locations.append([dowc[4],dowc[5]])

       if len(self.past.point_list) == 0:
          current.make_init_points(locations,self.id_list,self.dr,b_boxs)
       else:
          current.make_points(locations,b_boxs)

       del_id = self.run(self.past,current)
       points.make_current_to_past(current)
       temp_past = current

       for t_p_p in temp_past.point_list:
         tracked_object.append([t_p_p.b_box[0], t_p_p.b_box[1], t_p_p.b_box[2], t_p_p.b_box[3], t_p_p.id])

       for p_p in self.past.point_list:
           if p_p.id in del_id:
               p_p.count+=1
               if p_p.count < 10:
                if p_p.direcion == None:
                   temp_past.point_list.append(p_p)
                else:
                   p_p.location = tool.add(p_p.location,p_p.direction)
                   temp_past.point_list.append(p_p)
               else:
                 self.id_list.free_id(p_p.id)

       self.past = temp_past

       return tracked_object








        



