import math
from sympy.solvers import solve
from sympy import Symbol
i = 0
z = 1
a = Symbol('a')
es = Symbol('es')
esff = Symbol('esff')
esf = Symbol('esf')
esp = Symbol('esp')
espf = Symbol('espf')
Aas = Symbol('Aas')
apay = Symbol('apay')
def unesf(ele,tex):
    ele = 'Elegir unidades '+ ele
    un = ['1) kgf/cm2','2) MPa', '3) ksi']
    for x in un:
        print(x)
    uni = int(input(ele))
    unr = ['kgf/cm2','MPa', 'ksi']
    if uni == 1:
        print(tex,unr[0],':')
        dato = float(input())
    elif uni == 2:
        print(tex,unr[1],':')
        dato = float(input())
        dato = dato * 10**2/9.81
    elif uni == 3:
        print(tex,unr[2],':')
        dato = float(input())
        dato = dato*1000*(0.454/(2.54)**2)
    return dato
def unmom(ele,tex):
    un = ['1) Tonf*m','2) kgf*cm','3) kN*m']
    unr = ['Tonf*m','kgf*cm','kN*m']
    ele = 'Elegir unidades '+ele+': '
    tex = 'Momento '+tex+' en'
    for x in un:
        print(x)
    uni = int(input(ele))
    if uni == 1:
        print(tex,unr[0],':')
        M = float(input())
        M = M*(1E5)
    elif uni == 2:
        print(tex,unr[1],':')
        M = float(input())
    elif uni == 3:
        print(tex,unr[2],':')
        M = float(input())
        M = M*(1E5/9.81)
    return M
def acero():
    z = 1
    rec = [0,0,0,0,0,0,0]
    varAs = [0,0,0,0,0,0,0]
    j = 0
    As = 0
    print('Unidades fy')
    tex = 'Esfuerzo de fluencia (fy) en'
    ele = 'fy: '
    fy = unesf(ele,tex)
    while z == 1:
        num = int(input('Numero de la varilla: '))
        anum = math.pi*(num/8*2.54)**2/4 #area varilla cm2
        print('Número de varillas del #',num,':')
        nvar = int(input())
        rec[j] = float(input('Recubrimiento (cm): '))
        As = nvar*anum + As #área total acero
        varAs[j] = nvar*anum
        z = int(input('1) Más varillas, 2) Todas: '))
        j = j + 1
    return As, rec, varAs, fy
def beta(fc):
    if fc <= 280:
        beta1 = 0.85
    else:
        beta1 = 1.05-fc/1400
    return beta1
ele = int(input('1) Evaluar diseño 2) Diseñar: '))
if ele == 1:
    b = float(input('Ancho del perfil (b) en cm: '))
    h = float(input('Altura del perfil (h) en cm: '))
    Ag = b*h
    ele = 'resist. cncr.: '
    tex = 'Resistencia concreto (fc) en'
    print('Concreto')
    fc = unesf(ele,tex)
    print('Módulo de elasticidad del acero')
    ele = 'mod. elast.: '
    tex = 'Módulo de elasticidad (Es) en'
    Es = unesf(ele,tex)
    #Acero a tensión
    print('Acero a tensión')
    tension = acero()
    Ast = tension[0]
    recvt = tension[1]
    varAst = tension[2]
    fy = tension[3]
    ey = fy/Es
    #Acero a compresión
    print('Acero a compresión')
    compresion = acero()
    Asp = compresion[0]
    recvp = compresion[1]
    varAsp = compresion[2]
    fyp = compresion[3]
    beta1 = beta(fc)
    d = h - recvt[0]
    dp = recvp[0]
    rho = Ast/(b*d)
    rhop = Asp/(b*d)
    #C=T
    aay = solve(0.85*fc*a*b+Asp*Es*((0.003/(a/beta1))*((a/beta1)-recvp[0]))-Ast*fy,a)
    print(aay)
    if aay[0]<0:
        a = aay[1]
    else:
        a = aay[0]
    c = a/beta1
    esayy = solve(0.003/c-esff/(d-c),esff)
    es = esayy[0]
    espayy = solve(0.003/c-espf/(c-dp),espf)
    esp = espayy[0]
    print(es, esp)
    if a > h:
        print('Existe exceso de acero a tensión, por lo que el concreto no es suficiente.')
        #C=T
        esay = solve(0.85*fc*beta1*(0.003*d/(0.003+esf))*b-esf*Es*Ast,esf)
        print(esay)
        if esay[0] <0:
            es = esay[1]
        else:
            es = esay[0]
        print('Deformación en el acero: ',es)
        fs = es*Es
        print('Esfuerzo en el acero: ',fs,'kgf/cm2')
        c = 0.003*d/(0.003+es)
        a = beta1*c
        print('c: ',c)
        print('a: ',a)
        Mn = fs*Ast*(d-a/2)
        print('El momento nominal es: ',Mn, 'kgf*cm')
        print('El momento nominal es: ',Mn*(1E-5),'Tonf*m')
        print('FALLA FRÁGIL')
    else:
        #Falla dúctil
        print('a = ',a)
        c = a/beta1
        print('c = ',c)
        #esay = solve(0.003/c-es/(d-c),es)
        es = 0.003/c*(d-c)
        #espay = solve(0.003/c-esp/(c-dp),esp)
        esp = 0.003/c*(c-dp)
        if esp>=ey:
            fsp = fyp
        else:
            fsp = esp*Es
        if es>0:
            print('Deformación acero tensión:',es)
        if Asp != 0:
            print('Deformación acero compresión:',esp)
            A2=Ast-Asp
            a = (A2*fyp)/(0.85*fc*b)
            c = a/beta1
            esp = 0.003/c*(c-dp)
            if esp > ey:
                print('El acero de compresión está fluyendo.')
                Mn1 = Asp*fyp*(d-dp)
                Mn2 = 0.85*fc*a*b*(d-a/2)
                Mn = Mn1 + Mn2
                print(Mn)
            else:
                print('El acero de compresión no está fluyendo, cambio de suposición.')
                aay = solve(0.85*fc*a*b+Asp*Es*((0.003/(a/beta1))*((a/beta1)-recvp[0]))-Ast*fy,a)
                if aay[0]<0:
                    a = aay[1]
                else:
                    a = aay[0]
                c = a/beta1
                print('a = ',a)
                print('c = ',c)
                esay = solve(0.003/c-es/(d-c),es)
                es = esay[0]
                espay = solve(0.003/c-esp/(c-dp),esp)
                esp = espay[0]
                Mn = 0.85*fc*a*b*(d-a/2)+Asp*Es*esp*(d-dp)
        if es>=ey:
            print('El acero a tensión está fluyendo.')
            Mn = 0.85*fc*a*b*(d-a/2)
            Mn = 0.85*fc*a*b*(d-a/2)+Asp*fsp*(d-dp)
            print('El momento nominal es: ',Mn, 'kgf*cm')
            print('El momento nominal es: ',Mn*(1E-5),'Tonf*m')
        else:
            print('El acero a tensión no fluye, cambiar suposición.')
            
elif ele == 2:
    ele= 'MAD'
    tex = 'actuante de diseño (MAD)'
    Mad = unmom(ele,tex)
    b = float(input('Ancho del perfil (b) en cm: '))
    h = float(input('Altura del perfil (h) en cm: '))
    Ag = b*h
    ele = 'resist. cncr.: '
    tex = 'Resistencia concreto (fc) en'
    print('Concreto')
    fc = unesf(ele,tex)
    beta1 = beta(fc)
    print('Módulo de elasticidad del acero')
    ele = 'mod. elast.: '
    tex = 'Módulo de elasticidad (Es) en'
    Es = unesf(ele,tex)
    print('Acero a tensión')
    tex = 'Esfuerzo de fluencia (fy) en'
    ele = 'fy: '
    fy = unesf(ele,tex)
    ey = fy/Es
    rec = float(input('Recubrimiento (cm): '))
    d = h - rec
    print('¿Agregar acero a compresión?')
    elec = int(input('1) Sí 2) No: '))
    if elec == 1:
        print('Acero a compresión')
        fyp = unesf(ele,tex)
        recp = float(input('Recubrimiento (cm): '))
        dp = recp
        fr = float(input('Factor de resistencia (Fr): '))
        rhob = 0.85*fc*beta1/fy*(0.003/(0.003+fy/Es))
        rhomax = 0.75*rhob
        qmax = rhomax * (fy/(0.85*fc))
        apay = solve(Mad-fr*(apay*fyp*(d-recp)+0.85*fc*b*d**2*qmax*(1-0.5*qmax)),apay)
        print(apay)
        if apay[0] > 0:
            Asp = apay[0]
            A2 = rhomax*b*d
            As = Asp + A2
            #C=T
            a = A2*fy/(0.85*fc*b)
            c = a/beta1
            esp = 0.003/c*(c-recp)
            if esp>ey:
                print('El acero a compresión fluye.')
                print('El acero a compresión es: ',Asp,'cm2')
                print('El acero a tensión es: ',As,'cm2')
            else:
                print('El acero a compresión no fluye, cambio de suposición.')
                A2 = qmax*b*d*0.85*fc/fy
                a = Symbol('a')
                Asp = Symbol('Asp')
                f1 = Mad-fr*(0.85*fc*a*b*(d-a/2)+Asp*Es*0.003/(a/beta1)*(a/beta1-dp))
                f2 = rhomax*b*d*fy-(0.85*fc*a*b+Asp*Es*0.003/(a/beta1)*(a/beta1-dp))
                sols = solve((f1, f2), (a, Asp))
                print(sols)
        else:
            print('Acero a compresión no es necesario.')
    else:
        fr = float(input('Factor de resistencia (Fr): '))
        #Mrd=Mad
        aay = solve(Mad-fr*(0.85*fc*a*b*(d-a/2)),a)
        print(aay)
        if abs(aay[0]) == abs(aay[1]):
            print('Error, el concreto en la sección no es suficiente para alcanzar el equilibrio.')
        else:
            if aay[0]<aay[1] and aay[0]>0:
                a = aay[0]
            else:
                a = aay[1]
            print('a: ',a)
            c = a/beta1
            print('c: ',c)
            es = 0.003/c*(d-c)
            print('La deformación en el acero es: ',es)
            if es > ey:
                print("El acero está fluyendo")
            #As
            asay = solve(0.85*fc*a*b-Aas*fy,Aas)
            As = asay[0]
            print('El área de acero requerida es:',As,'cm2')
            #Varillas aprox
else:
    print('Error')