import json
from django.shortcuts import HttpResponse
from demo import monitor
from data import Generator, init_generator
from run import Monitor


gen = init_generator("pku")

monitor = Monitor(gen.map)

# init people
for p in gen.people:
    monitor.addPeople(p.id, p.pos_id)

def getlist():
    if monitor.tick == 0:
        for tick in range(10):
            print('====Tick', monitor.tick, "====")
            add = gen.act()

            # update human state
            for k, v in add.items():
                for id in v:
                    monitor.updatePeopleState(id, k)

            # update human position
            for p in gen.people:
                monitor.updatePeoplePos(p.id, p.pos_id)

            if tick > 6:
                # print infection index
                index, _ = monitor.getInfectionMap()
                print(index)

                # find contacts of a confirmed person
                print(monitor.confirmed)
                lst = list(monitor.confirmed)[0]
                print(lst, monitor.findContacts(lst))

            monitor.updateTick()

    print('====Tick', monitor.tick, "====")
    add = gen.act()

    # update human state
    for k, v in add.items():
        for id in v:
            monitor.updatePeopleState(id, k)

    # update human position
    for p in gen.people:
        monitor.updatePeoplePos(p.id, p.pos_id)

    # print infection index
    index, _ = monitor.getInfectionMap()
    print(index)

    # find contacts of a confirmed person
    print(monitor.confirmed)
    lst = list(monitor.confirmed)[0]
    print(lst, monitor.findContacts(lst))

    returnlist = monitor.getInfectionList()
    print(returnlist)
    monitor.updateTick()

    return returnlist

def getcontact(request):
    if monitor.tick == 0:
        for tick in range(10):
            print('====Tick', monitor.tick, "====")
            add = gen.act()

            # update human state
            for k, v in add.items():
                for id in v:
                    monitor.updatePeopleState(id, k)

            # update human position
            for p in gen.people:
                monitor.updatePeoplePos(p.id, p.pos_id)

            if tick > 6:
                # print infection index
                index, _ = monitor.getInfectionMap()
                print(index)

                # find contacts of a confirmed person
                print(monitor.confirmed)
                lst = list(monitor.confirmed)[0]
                print(lst, monitor.findContacts(lst))

            monitor.updateTick()

    print('====Tick', monitor.tick, "====")
    add = gen.act()

    # update human state
    for k, v in add.items():
        for id in v:
            monitor.updatePeopleState(id, k)

    # update human position
    for p in gen.people:
        monitor.updatePeoplePos(p.id, p.pos_id)

    # print infection index
    # index, _ = monitor.getInfectionMap()
    # print(index)

    # find contacts of a confirmed person
    print(monitor.confirmed)
    # for lst in list(monitor.confirmed):
    #     print(lst, monitor.findContacts(lst))
    lst = list(monitor.confirmed)[0]
    print(lst, monitor.findContacts(lst))
    print(monitor.findContacts(lst))

    # print(type(lst), type(request))
    # returnlist = monitor.findContacts(request)
    # if int(request) in list(monitor.confirmed):
    #     print("true")
    # else:
    #     print("false")
    # if int(request) == lst:
    #     print("true")
    # else:
    #     print("false")
    print(int(request), monitor.findContacts(int(request)))
    monitor.updateTick()
    dict = monitor.findContacts(int(request))
    print(dict)
    return dict

def index(request):
    # return HttpResponse(json.dumps(json_to_python))
    return HttpResponse(getlist())

def contact(request):
    # return HttpResponse(getcontact(request))
    return HttpResponse(json.dumps(getcontact(request.GET.get('key'))))

# print(contact(0))
