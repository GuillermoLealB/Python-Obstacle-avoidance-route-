#  Leal Benitez Guillermo Roberto      18220810        

import Dijkstra #importo el mismo porgrma mostrado en clases sobre el algoritmo de Dijkstra 
import pygame, random, math

################################ Requeriemientos iniciales #########################################################################################################
color = (0, 0, 0) 
ancho = 800
altura = 600
Ncirculos = 50      #numero de obstaculos  
NNodos=150          #Numero de Nodos 
rnodos=2             #radio de mis nodos 
##################################  Configuracion de Pygame    ######################################################################################################

pygame.init()
pantalla = pygame.display.set_mode((ancho, altura))
pygame.display.set_caption("Ruta evasor de Obstaculos 2D")
pantalla.fill((216,203,187))

class circle():
    def __init__(self):
        self.x = random.randint(0,ancho)
        self.y = random.randint(0,altura)
        self.r = random.randint(5,70)

    def new(self):
        pygame.draw.circle(pantalla,(141, 128, 111), (self.x,self.y), self.r)
    def newnodo(self):
        pygame.draw.circle(pantalla,color, (self.x,self.y), rnodos)

##############################################################   OBSTACULOS   ###################################################################################### 

circulos = []
nodos=[]
posiciones=[]  
posnodo=[]
while len(circulos) <= Ncirculos:    #el circulo inicia vacio y generaremos hasta que le vector tenga n elementos deseados  
    new = circle()  
    c = circle()
    if new.x-new.r > 0 and new.y - new.r > 0 and new.x + new.r< ancho and new.y + new.r < altura: #para delimitar la creacion de circulos dentro de nuestro display 
        if any(pow(c.r - new.r, 2) <= (pow(c.x - new.x, 2) + pow(c.y - new.y, 2)) <=pow(c.r + new.r, 2) for c in circulos): #Geometria para el determinanto  de la posicion evitando el traslape
           continue  #ignora rodo lo demas cuando alguna condicion de traslape se genera, y saltamos a un siguiente ciclo
        circulos.append(new) # de lo contrario,agregamos las caracteristicas de circulo
        listpos=(new.x,new.y,new.r)#guardamos la posicion y el radio del circulo dibujado 
        posiciones.append(listpos)
        new.new() #dibujamos el circulo 
        pygame.display.update() 

############################################################### GENERADOR DE NODOS   ##############################################################################


while len(nodos) <= NNodos:    #while para asegurar que se generen los nodos deseados 
    nod=circle()  
    n=circle()
    trn=True      #candado de traslape de nodos 
    for i in range(len(posiciones)):  #for para pasar por todos los circulos(obstaculos) establecidos 
        posx,posy,posr=posiciones[i]#obtenemos las posiciones de nuestro obstaculo 
        if nod.x == posx and nod.y==posy: #preguntamos para confirmar que el punto no este en el mismo lugar que alguno de nuestros puntos generados  
            trn=False             
        if  math.hypot(posx - nod.x, posy- nod.y)<= nod.r + posr: #ahora confirmamos que mis nodos no sean menor que mi radio para no estar dentro de mis obstaculos 
            trn=False

    if (nod.x-nod.r > 0 and nod.y - nod.r > 0 and nod.x + nod.r< ancho and nod.y + nod.r < altura) and trn==True: # delimitamos la creacion de los nodos dentro de nuestro Display , ademas de que confirma si el candado de tralape de nodos esta en True
            if any(0 <= (pow(n.x - nod.x, 2) + pow(n.y - nod.y, 2)) <=pow(rnodos*2, 2) for n in nodos): #aplicamos la relacion de distacia entre puntos para evitar el traslape 
                continue # continua si existe algun tipo de traslape 
            nodos.append(nod)
            datanodos=(nod.x,nod.y) #guradamoS su posicion 
            posnodo.append(datanodos)
            nod.newnodo()  # dibujamos nuevo nodo 
            pygame.display.update() #actualizamos el display 



################################################################ NODO DE INCIO ####################################################################

inix=1
iniy=random.randint(0,600)  ##ASEGURAMOS QUE MI PUNTO INICIAL ESTE EN MI LADO IZQUIERDO PERO LA ALTURA VARIA ALEATOREAMENTE 
iniciodata=(inix,iniy)
posnodo.insert(0,iniciodata)
inicio=pygame.draw.circle(pantalla,(0,255,0), (inix,iniy), 2)
nodos.insert(0,inicio)

################################################################ NODO DE SALIDA  ##################################################################

finx=799
finy=random.randint(0,600) ##ASEGURAMOS QUE MI PUNTO INICIAL ESTE EN MI LADO DERECHA PERO LA ALTURA VARIA ALEATOREAMENTE 
findata=(finx,finy)
posnodo.append(findata)
fin=pygame.draw.circle(pantalla,(0,255,0), (finx,finy), 2)
nodos.append(fin)


################################################################# LINEAS DE UNION ###################################################################################


start=[]   ## aarray para grafo Inicio
end=[]      ##array para grafo fin 
pondera=[]  #Array para asignar la distancia 
posx=0 
posy=0    # Reutilizamos y Limpiamos lasvariables de posiciones 
posr=0 

while len(nodos)>0:  ## ciclo que generara hasta que la pila quede vacia  
    nx,ny=posnodo[len(nodos)-1]   #empezamos por el ultimo nodo de la pila , obtenemos su posicion, siendo mi nodo de referencia
    for k in range(0,len(nodos)-1):  #ciclo para asegurar que nuestro nodo de referencia se compare con todos los nodos existentes en la pila
        dibujar=True     
        nx2,ny2=posnodo[k] ##obtenemos la posicion de cada uno de los nodos diferentes 
        distanciaPunto_Punto=math.hypot(nx2-nx,ny2-ny) ##obtenemos la distancia del nodo referencia respecto a cada uno de mis nodos diferentes 
        
        ##### CALCULO DE LA PENDIENTE m= (y2-y1)/(x2-x1)  #####

        div=float(nx2-nx)  #obtenemos el denominador 
        if (div != 0):#proteccion contra una pendiente infinita  (division con denominador 0) , para la pendiente
            pendiente=(ny2-ny)/div# calculo de la pendiente
        elif div==0:
            pendiente=999999 # se agrega un valor muy alto para asemejar lo mas posible a la pendiente infinita que se daria si en un caso ,un nodo tiene la misma x y se tiene que unir
        
        ######## ECUACION DE LA RECTA  y-y1=m(x-x1)  #########
        ###  forma despejada que servira como referencis =  y-y1-mx+mx1=0

        Af=(-1*pendiente) # -m*X
        Bf=1              # Y
        Cf=(pendiente*nx)-ny #  -y1+(m*x1)
        for l in range(len(posiciones)): #ya teniendo los parametros ,vamos a revisar la posicion de cada uno de los circulos 
            posx,posy,posr=posiciones[l]  # obtenemos su posicion de cada circulo 
            numerador=float((Af*posx)+(Bf*posy)+(Cf)) # #### se realiza la formula de distancia entre un punto(centro de mi obstaculo) y una recta 
            denominador=(math.sqrt(pow(Af,2)+pow(Bf,2)))
            Distanciarecpunt=abs(numerador/denominador) #obtenemos la distancia entre el centro del circulo y la linea

            ### Al tener una ecuacion de la recta estamos considerando una RECTA INFINITA, a la hora de calcular distancia 
            ### puede marcarnos un traslape de linea y circulo incluso FUERA DE LA DISTANCIA ENTRE LOS NODOS que estamos intentando unir
            ### Por lo que deberiamos delimitar de alguna forma el area, poniendo una condicion extra 
            ### Mi solucion fue emplear la solucion matematica de relacion entre mis dos nodos de union respecto del circulo :
            
            distanciaPunt1_a_Cir=math.hypot(posx-nx,posy-ny) ## Medimos la distancia de mi nodo de referencia respecto al circulo 
            distanciaPunt2_a_Cir=math.hypot(posx-nx2,posy-ny2) ##Medimos la distancia de mi nodo en turno respecto mi circulo 

            #Al ya tener definida mi condicion de traslape entre nodos y obstaculos, solo queda resolver que la distancia de mis nodos a mi circulo
            #no puede ser mayor que la distancia entre mis dos nodos 
                                #posr se le suma 1 debido al ancho de mi linea 
            if Distanciarecpunt<=posr+1 and distanciaPunt1_a_Cir<=distanciaPunto_Punto and distanciaPunt2_a_Cir<=distanciaPunto_Punto : 
                dibujar=False #candado dibujara 
                break    # si existe el cumplimiento de estas tres situaciones , dejamos de comparar con los demas circulos debido a que ya sabemos que va a existir un objeto en medio 

        if dibujar==True:
            Data_grafp_ini=(len(nodos)-1)
            Data_grafo_Fin=(k)
            Data_pondera=distanciaPunto_Punto#### obtenemos mis datos para mi grafo
            start.append(Data_grafp_ini)
            end.append(Data_grafo_Fin)
            pondera.append(Data_pondera)
            pygame.draw.line(pantalla, (144, 92, 18), (nx, ny), (nx2,ny2 ))
            
    nodos.pop() ###borramos el ultimo nodo de la pila para asi no seguir infinitamente 
    pygame.display.update()





######################################## GRAFO Y DIJKSTRA ##################################################################

print('inicio ',start)
print('fin    ',end)
print('pondera',pondera)
g=Dijkstra.Grafo(start,end,pondera)
print('recorrido mas corto=',g.Dijkstra(0,NNodos+2))  ### imporar el programa dado en clases podemos dar usos a sus funciones y al algoritmo de dijkstra 

linea_camino=list(g.Dijkstra(0,NNodos+2))
if len(linea_camino)==1:
    print('imposible conectar nodos,obstaculo aisalando el nodo , intente otra vez o con mas nodos')
else:
####################################  UNIR CAMINO MAS CORTO  #################################################################### 

    for lon in range(len(linea_camino)):  #aseguramos que pase por todos los numeros de mi recorrido mas corto 
        camino=linea_camino[lon]
        if camino==0:
            posanterior=camino  
            continue
        for check in range(len(posnodo)):  #buscamos la misma posicion de todas las posiciones de mis nodos de lo que  mi reccorrido dijkstra diga 
            if check==camino:
                posactual=check
                break
        pygame.draw.line(pantalla, (0, 0, 0), posnodo[posactual], posnodo[posanterior],3)
        pygame.display.update()
        posanterior=posactual

################################################ Muestra de nuevo  ##############################################################################

#este ultimo paso es meramente demostrativo , vuelvo a imprimir los nodos y mis puntos inicial y final debido a que las lineas generadas los tapan
#con esto resalto que no se traslapan ni se generan dentro de mi circulo 

for x in range(len(posnodo)):
    posx,posy=posnodo[x]
    pygame.draw.circle(pantalla,(255,255,0), (posx,posy), rnodos)
pygame.draw.circle(pantalla,(0,255,0), (inix,iniy), 2)
pygame.draw.circle(pantalla,(0,255,0), (finx,finy), 2)
pygame.display.update()
##########################################   MANTENER DYSPLAY ABIERTO   #############################################################

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()   