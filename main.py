import tracking

#list1 = [tracking.Location(1.5, 7.0), tracking.Location(2.0, 1.0)];
#list2 = [tracking.Location(1.7, 6.0), tracking.Location(1.7, 2.0)];
#list3 = [[tracking.Location(1.6, 5.3), tracking.Location(1.3, 4.5), tracking.Location(1.5, 3.2), tracking.Location(1.4, 2.5), tracking.Location(1.6, 1.6)],
               #[tracking.Location(1.5, 3.0), tracking.Location(1.0, 4.0), tracking.Location(0.7, 5.0), tracking.Location(0.6, 6.0), tracking.Location(0.5, 7.0)]];

list1 = [tracking.Location(1.5,7.0),tracking.Location(2.0,1.0),tracking.Location(1.0,1.0)];
list2 = [tracking.Location(1.7,6.0),tracking.Location(1.7,2.0),tracking.Location(1.3,2.0)];
list3 = [[tracking.Location(1.6,5.3),tracking.Location(1.3,4.5),tracking.Location(1.5,3.2),tracking.Location(1.4,2.5),tracking.Location(1.6,1.6)],[tracking.Location(1.5,3.0),tracking.Location(1.0,4.0),tracking.Location(0.7,5.0),tracking.Location(0.6,6.0),tracking.Location(0.5,7.0)]
,[tracking.Location(1.6,3.0),tracking.Location(1.8,4.0),tracking.Location(2.1,5.0),tracking.Location(2.2,6.0),tracking.Location(2.2,7.0)]]



t1 = tracking.Location(0.0,6.5)#물체의 좌표를 저장 하는 class 형
t2 = tracking.Location(3.0,6.5)
t3 = tracking.Location(3.0,0.0)
t4 = tracking.Location(0.0,0.0)

n = 3# 인원수
r = 1.0#평균 이동거리 지름
num = 5#반복 횟수

id_list = tracking.id_node_list()# 아이디를 할당 하기 위해서 아이디를 관리하는 class 를 생성
past = tracking.points(0,list())#물체의 좌표들을 모아 놓은 class 를 생서
past.make_init_points(list1,id_list,r)#맨 처음 받아들인 프레임의 물체의 좌표를 들에 초기 아이디를 부여 하고 평균 이동거리도 초기화 (맨 처음 프레임에만 사용 하는 함수)


print("length: "+str(past.length))
print("-----------------------------")

for i in range(0,n):
    print("id: "+str(past.list[i].id)+" r: "+str(past.list[i].r)+" distance: "+str(past.list[i].distance)+" direction: "+str(past.list[i].direction.x)+" "+str(past.list[i].direction.y)+" point: "+str(past.list[i].p.x)+" "+str(past.list[i].p.y))

print("------------------------------")
current = tracking.points(0,list())# 현재 받아들은 프레임의 물체의 좌표들을 저장할 class 생성
current.make_points(list2)# 행당 class 를 list2에 저장된 물체 좌표 들로 초기화 (처음 프레임 이후에 초기화를 위해 사용하는 함수)

track = tracking.tracking(id_list,0.5,0.7,1.0,t1,t2,t3,t4)
"""tracking object를 생성 
id_list: 아이디를 할당 해제 를 관리 할수 있는 class 
0.5 = margin 
0.7 = alpha 평균 이동 거리의 누적 평균을 계산할 때 과거 값을 얼마의 비율로 반영 하는 지에 대한 변수 로 (0~1) 까지 
1.0 = r 평균 이동 거리 초기 값 으로 (mapping 할수 있는 과거 프레임의 물체가 없을 경우 이값으로 평균 이동 거리를 초기화함
t1 t2 t3 t4 = 물체를 tracking 하는 관심 영역 boundary 지정에 사용되는 4개의 점값으로 좌측 상단 부터 시계 방향으로 입력
"""

k = 0

while(k<num):
    track.run(past,current)#tracking object를 실행 past는 과거 프레임 의 물체 리스트 current는 현재 프레임의 물체 리스트 current는 아이디 할당이 되어 있지 않음
    #run 함수의 결과로 current에 아이디와 여러 변수 들이 할당 됨
    tracking.points.make_current_to_past(current)# current에서 boundary 밖으로 이탈한 물체 들을 제외 하여 아이디를 해제 해 주는 함수
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

