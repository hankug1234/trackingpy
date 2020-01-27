import numpy as np
import math

class predict:
 def __init__(self,default_velocity,delay,alpha):
     self.id_list = dict()
     self.default_velocity = default_velocity
     self.delay = delay
     self.alpha = alpha

 def change_delay(self,num):
     self.delay +=num*self.alpha

 def free_id_list_id(self):
     id_list_keys = self.id_list.keys()
     for key in id_list_keys:
         if self.id_list[key]['state'] == False:
             del self.id_list[id]
         else:
             self.id_list[key]['state'] = False

 def run(self,detected_object_with_centerbottom,ids=None):
     locations = dict()
     self.change_delay(len(detected_object_with_centerbottom))
     for index,dowc in enumerate(detected_object_with_centerbottom):
       id = ids[index]
       self.update(dowc,id)
       p_location = self.predict_location(self.id_list[id]['location'],self.id_list[id]['direction'],self.id_list[id]['velocity'],self.delay)
       locations[id] = p_location
     self.free_id_list_id()
     return locations

 def update(self, dowc, id=None):
     id_list_keys = self.id_list.keys()
     current_location = [dowc[4], dowc[5]]
     if id in id_list_keys:
         past_location = self.id_list[id]['location']
         direction = [past_location[0]-current_location[0],past_location[1]-current_location[1]]
         self.id_list[id]['location'] = current_location
         self.id_list[id]['direction'] = direction
         self.id_list[id]['velocity'] = math.sqrt(direction[0]**2,direction[1]**2)
     else:
         self.id_list[id] = dict()
         self.id_list[id]['location'] = current_location
         self.id_list[id]['direction'] = None
         self.id_list[id]['velocity'] = self.default_velocity
     self.id_list[id]['state'] = True


 def predict_location(self,location,direction,velocity,delay):
    if direction == None:
        return location
    length_of_direction = math.sqrt(direction[0]**2 + direction[1]**2)
    speed = velocity*delay
    normal_direction = [direction[0]/length_of_direction,direction[1]/length_of_direction]
    return [location[0]+(normal_direction[0]*speed),location[1]+(normal_direction[1]*speed)]