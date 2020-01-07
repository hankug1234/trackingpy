import tracking

#list1 = [tracking.Location(1.5, 7.0), tracking.Location(2.0, 1.0)];
#list2 = [tracking.Location(1.7, 6.0), tracking.Location(1.7, 2.0)];
#list3 = [[tracking.Location(1.6, 5.3), tracking.Location(1.3, 4.5), tracking.Location(1.5, 3.2), tracking.Location(1.4, 2.5), tracking.Location(1.6, 1.6)],
               #[tracking.Location(1.5, 3.0), tracking.Location(1.0, 4.0), tracking.Location(0.7, 5.0), tracking.Location(0.6, 6.0), tracking.Location(0.5, 7.0)]];

list1 = [tracking.Location(1.5,7.0),tracking.Location(2.0,1.0),tracking.Location(1.0,1.0)];
list2 = [tracking.Location(1.7,6.0),tracking.Location(1.7,2.0),tracking.Location(1.3,2.0)];
list3 = [[tracking.Location(1.6,5.3),tracking.Location(1.3,4.5),tracking.Location(1.5,3.2),tracking.Location(1.4,2.5),tracking.Location(1.6,1.6)],[tracking.Location(1.5,3.0),tracking.Location(1.0,4.0),tracking.Location(0.7,5.0),tracking.Location(0.6,6.0),tracking.Location(0.5,7.0)]
,[tracking.Location(1.6,3.0),tracking.Location(1.8,4.0),tracking.Location(2.1,5.0),tracking.Location(2.2,6.0),tracking.Location(2.2,7.0)]]



t1 = tracking.Location(0.0,6.5)
t2 = tracking.Location(3.0,6.5)
t3 = tracking.Location(3.0,0.0)
t4 = tracking.Location(0.0,0.0)

n = 3
r = 1.0
num = 5

id_list = tracking.id_node_list()
past = tracking.points(0,list())
past.make_init_points(list1,id_list,r)


print("length: "+str(past.length))
print("-----------------------------")

for i in range(0,n):
    print("id: "+str(past.list[i].id)+" r: "+str(past.list[i].r)+" distance: "+str(past.list[i].distance)+" direction: "+str(past.list[i].direction.x)+" "+str(past.list[i].direction.y)+" point: "+str(past.list[i].p.x)+" "+str(past.list[i].p.y))

print("------------------------------")
current = tracking.points(0,list())
current.make_points(list2)

track = tracking.tracking(id_list,0.5,0.7,1.0,t1,t2,t3,t4)

k = 0

while(k<num):
    track.run(past,current)
    tracking.points.make_current_to_past(current)
    past = current

    for i in range(0,n):
        list1[i] = list3[i][k]

    if(past.length == 0):
        print("------------------------------")
        print("no data")
        print("------------------------------")
    else:
        print("-----------------------------")
        for i in range(0, past.length):
            print("id: " + str(past.list[i].id) + " r: " + str(past.list[i].r) + " distance: " + str(past.list[i].distance) + " direction: " + str(past.list[i].direction.x) + " " + str(past.list[i].direction.y) + " point: " + str(past.list[i].p.x) + " " + str(past.list[i].p.y))
        print("------------------------------")
    current = tracking.points(0,list())
    current.make_points(list1)
    k+=1

