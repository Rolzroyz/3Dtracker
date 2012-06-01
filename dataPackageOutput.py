def packageOutput(f,pkg):
    FILE = open(f,'w')
    i = 0
    j = -1
    ev = '#### Event '
    ndg = '#### Num Points: '
    rtn = '####\n'
    sp = ' '
    nl = '\n'
    for i in range(len(pkg)):
        pt = str(len(pkg[i]))
        n = str(i)
        q = ev + n + ndg + pt + rtn
        FILE.write(q)

        for j in range(len(pkg[i])):
            dg = str(pkg[i][j].x) + sp + str(pkg[i][j].y) + sp + str(pkg[i][j].z) + sp + str(pkg[i][j].adc) + nl
            FILE.write(dg)
    f = FILE.close()

