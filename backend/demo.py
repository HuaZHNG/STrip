from data import Generator, init_generator
from run import Monitor


gen = init_generator("pku")

monitor = Monitor(gen.map)

# init people
for p in gen.people:
    monitor.addPeople(p.id, p.pos_id)

# run
for tick in range(40):
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


# return json format of infection index
print(monitor.getInfectionList())