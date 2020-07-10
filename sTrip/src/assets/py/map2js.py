with open('edge_geometry.json','w') as fout:
    fout.write('{ "edgeGeometry" : \n')
    # with open('../data/SH_map/SH_EdgeGeometry.txt') as fin:
    with open('./WA_EdgeGeometry.txt') as fin:
        result = []
        for line in fin.readlines():


            # fout.write('[')
            data = line.strip().split('^^')
            index = data[0]
            smd = data[1].split('^')
            pos = []
            for i in range(2, len(smd), 2):
                pos.append('[{0},{1}]'.format(smd[i], smd[i+1]))
            # # fout.write(data[0]+',\"'+data[2]+'\",')
            # for idx in range(4,len(data), 2):
            #     # result += '[' + data[idx] + ',' + data[idx+1] +'],'
            #     fout.write('['+data[idx]+','+data[idx+1]+'],')
            #     # fout.write(result)
            #
            #     # result =
            result.append('[{0}, "{1}", {2}]\n'.format(index, smd[0], ','.join(pos)))


    fout.write('[{0}]'.format(','.join(result)) + '}')
