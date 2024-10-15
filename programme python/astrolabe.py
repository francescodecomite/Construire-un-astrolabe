# On rajoute des cercles (verts) pour aider a la fabrication du rete
# Le nombre de points en SVG (ce qui ne veut rien dire)
TAILLE=500
# Le diametre du de la sphere celeste
R=1
# les bornes du carré centré. On fait tenir le tropique du Capricorne dedans (à revoir)
xmin=-1.05*R

def cartouche(x,y,texte,fonte="\"Caladea\"",taille=10):
     chaine="<text x=\""+str(transfo(x))+"\" y=\""+str(transfo(y))+"\" text-anchor=\"middle\" font-style=\"italic\" font-family="+fonte+" font-size=\""+str(taille)+"\">"+texte+"</text>"
     return chaine
# un rectangle pour le cartouche
def rect_cartouche(x,y,lar,hau,largeur=0.5,rx=0.5,ry=0.5):
     chaine="<rect x=\""+str(transfo(x))+"\" y=\""+str(transfo(y))+"\" width=\""+str(lar)+"\" height=\""+str(hau)+"\" rx=\""+str(rx)+"\" ry=\""+str(y)+"\" stroke=\"black\"  fill=\"none\"  stroke-width=\""+str(largeur)+"\" />\n"
     print(chaine)
     return chaine
    
# l equation du temps
def equationdutemps(x):
    # Nombre de jours depuis l'an 2000
    NB=365*(x-2000)+(x-2000)//4+1
    Tzero=NB/365250
    resu=[0 for i in range(366)]
    tabalpha=[0 for i in range(366)]
    tabLM=[0 for i in range(366)]
    tabquadrant=[0 for i in range(366)]
    tabquadrant2=[0 for i in range(366)]
    for i in range(366):
        T=Tzero+i/365250
        excent=0.0167086342-0.0004203654*T-0.0000126734*T*T
        epsi=23.43928111-((468.0927*T-0.0152*T*T)/3600)
        LM=280.46645683+((1296027711.03429*T+109.15809*T*T)/3600)
        while LM<0:
            LM=LM+360
        while LM>360:
            LM=LM-360
        tabLM[i]=LM
        omega=282.93734808+((61900.55290*T+164.47797*T*T)/3600)
        while omega<0:
            omega=omega+360
        while omega>360:
            omega=omega-360
        
        M=LM-omega
        while M<0:
            M=M+360
        while M>360:
            M=M-360
        centre=180/pi*(2*excent*sin(M*pi/180)+5.0/4*excent*excent*sin(2*M*pi/180)+13.0/12*excent*excent*excent*sin(3*M*pi/180))
        lambdas=LM+centre
        while lambdas<0:
            lambdas=lambdas+360
        while lambdas>360:
            lambdas=lambdas-360

        quadrant=3
        if lambdas<270:
            quadrant=2
        if lambdas<180:
            quadrant=1
        if lambdas<90:
            quadrant=0
        tabquadrant[i]=quadrant
        
        tanalpha=cos(epsi*pi/180)*tan(lambdas*pi/180)
        alpha=180/pi*atan(tanalpha)
        while (alpha<0):
         alpha=alpha+360
        while (alpha>360):
         alpha=alpha-360
        quadrant2=3
        if alpha<270:
            quadrant2=2
        if alpha<180:
            quadrant2=1
        if alpha<90:
            quadrant2=0
        
        tabquadrant2[i]=quadrant2
        #print("Alpha avant ",alpha)
        # ramener alpha dans le meme quadrant que lambdas
        # en degres
        
        if (quadrant2!=quadrant):
            alpha=alpha+180
            if alpha>360:
                alpha=alpha-360
       
        tabalpha[i]=alpha
        #print("Alpha après ", alpha)


         
        # en degres
        equation=alpha-LM
        #print("---> ",i," ",equation," ",alpha," ",LM," ",quadrant," ",quadrant2," ",lambdas)
        # en temps
        equation=equation*60*4
        resu[i]=equation
        if(equation<-1000):
            equation=alpha+(360-LM)
            equation=equation*60*4
            resu[i]=equation
            print("Probleme : ",i," ",resu[i])
            for j in range(i-5,i+1):
             print(" ",j," ",resu[j]," ",tabalpha[j]," ",tabLM[j]," ",tabquadrant[j]," ",tabquadrant2[j])
            #resu[i]=0
           
        minutes=int(equation)//60
        secondes=int(equation)%60
            
        if minutes<0:
         minutes=minutes+1
         secondes=60-secondes
        #print(i," ",equation," ",minutes," ",secondes)
    return resu




# Les coef de la transfo affine
coefA=-TAILLE/(2*xmin)
coefB=TAILLE/2

# Latitude : décochez la latitude pour laquelle vous voulez construire un tympan
"""
     Si vous voulez introduire une nouvelle latitude :
     -  Rajoutez-là dans la liste et décochez-la.
     -  Ajoutez une entrée pour cette latitude pour chacun des quatre dictionnaires ci-dessous
        (copiez celle de la latitude la plus proche, comme pour 44 et 46 dans les deux premiers dictionnaires)
     -  Regardez ce que ça donne.
     -  Si c'est ok pour vous, bingo ! Ca devrait marcher en 40 et 60 degrés.
     -  Sinon, ontactez-moi pour que je vous explique fdecomite@gmail.com
     
"""
#PHI=50.7333
#PHI=44
PHI=46
#PHI=30 # encore des problème avec cette latitude : décommentez la dernière ligne des 4 dictionnaires ci-dessous pour l'activer quand même...
#PHI=60

decalages={50.7333:[9,18.1,30.8,40.15,48.2,57.5,67,78.2,88.3],
           44:[6.5,16.8,30.4,40.15,48.2,57.65,67.4,79.25,91],
           46:[6.5,16.8,30.4,40.15,48.2,57.65,67.4,79.25,91],
           60:[14,22,32.6,41,48.42,57.1,65.55,75.5,84]}
           # Il y a encore des problèmes de cercles avec cette latiture 30:[6.5,16.8,30.4,40.15,48.2,57.65,67.4,79.25,91]

decalsup={50.7333:[58.6,62,65.5,68.6,71.55,74.4,77.4,80.35,83.4,86.7,90.2],
          44:[58.6,62.4,65.5,68.6,71.55,74.4,77.4,80.3,83.4,86.5,90],
          46:[58.6,62.4,65.5,68.6,71.55,74.4,77.4,80.3,83.4,86.5,90],
          60:[59,62.3,65.3,68.4,71.3,74.3,77.4,80.4,83.6,86.4,90]}
          # Il y a encore des problèmes de cercles avec cette latiture 30:[58.6,62.4,65.5,68.6,71.55,74.4,77.4,80.3,83.4,86.5,90]}

decaldroit={50.7333:[12.485,97.13,95.561,94.1,92.59],
            44:[7.2,17.27,96.85,95.15,93.45],
            46:[8.6,20.5,96.3,94.8,93.45],  
            60:[96.38,95,93.8,92.7,91.5]}
            # Il y a encore des problèmes de cercles avec cette latiture 30: [10,5.75,212,95.15,93.45]}

decalgauche={50.7333:[86.2,51.7,52.9,54.1,54.8],
             44:[91.3,81.32,51.6,53.18,54.18],
             46:[89.785,78.1,52,53.18,54.18], 
             60:[52.62,53.6,54.5,55.3,55.7]}
             # Il y a encore des problèmes de cercles avec cette latiture 30:[91.3,81.32,51.6,53.18,54.18] }
from math import *

def transfo(x):
    return coefA*x+coefB

def echelle(x):
    return coefA*x

def intersection(cercle1,cercle2):
    """
     Calculer les deux intersections de deux cercles
     cercleI : ((x,y),r)
    """
    x1=cercle1[0][0]
    y1=cercle1[0][1]
    b=cercle1[1]
    x2=cercle2[0][0]
    y2=cercle2[0][1]
    c=cercle2[1]
    a=(-x1*x1-y1*y1+x2*x2+y2*y2+b*b-c*c)/(2*(y2-y1))
    d=(x2-x1)/(y2-y1)
    A=d*d+1
    B=-2*x1+2*y1*d-2*a*d
    C=x1*x1+y1*y1-2*y1*a+a*a-b*b
    delta=B*B-4*A*C
    X1c=(-B+sqrt(delta))/(2*A)
    Y1c=a-(d*(-B+sqrt(delta))/(2*A))
    X1cp=(-B-sqrt(delta))/(2*A)
    Y1cp=a-(d*(-B-sqrt(delta))/(2*A))
    return ((X1c,Y1c),(X1cp,Y1cp))


LARGEUR=0.5    

def cercle(cx,cy,rayon,stroke="\"black\"" ,id="\"  \"",largeur=LARGEUR):
    return "<circle cx=\""+str(transfo(cx))+"\" cy=\""+str(transfo(cy))+"\"  r=\""+str(echelle(rayon))+"\" fill=\"none\" stroke="+stroke+" id="+id+"  stroke-width=\""+str(largeur)+"\" />\n"

def cercleinvisible(cx,cy,rayon,stroke="\"none\"" ,id="\"  \"",largeur=LARGEUR):
    return "<circle cx=\""+str(transfo(cx))+"\" cy=\""+str(transfo(cy))+"\"  r=\""+str(echelle(rayon))+"\" fill=\"none\" stroke="+stroke+" id="+id+"  stroke-width=\""+str(largeur)+"\" />\n"


def angle(degre):
    return pi*degre/180

def ligne(debut,fin,id="\" \"",stroke="\"black\""):
    chaine="<line x1=\""+str(transfo(debut[0]))+"\" y1=\""+str(transfo(debut[1]))+"\"   x2=\""+str(transfo(fin[0]))+"\" y2=\""+str(transfo(fin[1]))+"\"   id="+id+" stroke="+stroke+"  stroke-width=\""+str(LARGEUR)+"\" />"
    return chaine

def ligne_large(debut,fin,coef,id="\" \"",stroke="\"black\""):
    chaine="<line x1=\""+str(transfo(debut[0]))+"\" y1=\""+str(transfo(debut[1]))+"\"   x2=\""+str(transfo(fin[0]))+"\" y2=\""+str(transfo(fin[1]))+"\"   id="+id+" stroke="+stroke+"  stroke-width=\""+str(coef*LARGEUR)+"\" />"
    return chaine

def texte(string,chemin,offset=20):
    chaine="<text font-family=\"Arial, Helvetica, sans-serif\" font-size=\"7\" >\n"
    chaine=chaine+"<textPath xlink:href=\"#"+chemin+"\" startOffset=\""+str(offset)+"%\">"+string+"</textPath>\n "+"</text>"
    return chaine

"""
 image.write(polygone([(cote,int_cote[i]),(cote1,int_cote1[i]),(cote1,int_cote1[i+1]),(cote,int_cote[i+1])] fill=rempli,stroke="\"none\""))
"""
def polygone(l,fill="\"none\"",stroke="\"none\""):
     chaine=""
     for u in l:
          chaine=chaine+" "+str(transfo(u[0]))+","+str(transfo(u[1]))
     resu="<polygon points=\""+chaine+"\" fill="+fill+" stroke="+stroke+" />"
     print(resu)
     return resu


def arc(debut,fin,rayon,id="\" \"",largeur=LARGEUR,stroke="\"black\""):
    chaine="<path d=\"\n"
    chaine=chaine+"M"+str(transfo(debut[0]))+" "+str(transfo(debut[1]))+"\n"
    chaine=chaine+"A"+str(echelle(rayon))+" "+str(echelle(rayon))+" 0 0 0 "+str(transfo(fin[0]))+" "+str(transfo(fin[1]))+"\"  id="+id+" fill=\"none\"  stroke="+stroke+"   stroke-width=\""+str(largeur)+"\" />\n"
    return chaine

def arcinvisible(debut,fin,rayon,id="\" \"",largeur=LARGEUR):
    chaine="<path d=\"\n"
    chaine=chaine+"M"+str(transfo(debut[0]))+" "+str(transfo(debut[1]))+"\n"
    chaine=chaine+"A"+str(echelle(rayon))+" "+str(echelle(rayon))+" 0 0 0 "+str(transfo(fin[0]))+" "+str(transfo(fin[1]))+"\"  id="+id+" fill=\"none\"    stroke=\"none\"   stroke-width=\""+str(largeur)+"\" />\n"
    return chaine

def arcinvisible2(debut,fin,rayon,id="\" \"",largeur=LARGEUR):
    chaine="<path d=\"\n"
    chaine=chaine+"M"+str(transfo(debut[0]))+" "+str(transfo(debut[1]))+"\n"
    chaine=chaine+"A"+str(echelle(rayon))+" "+str(echelle(rayon))+" 0 1 0 "+str(transfo(fin[0]))+" "+str(transfo(fin[1]))+"\"  id="+id+" fill=\"none\"    stroke=\"none\"   stroke-width=\""+str(largeur)+"\" />\n"
    return chaine

def arcinvisible3(debut,fin,rayon,id="\" \"",largeur=LARGEUR):
    chaine="<path d=\"\n"
    chaine=chaine+"M"+str(transfo(debut[0]))+" "+str(transfo(debut[1]))+"\n"
    chaine=chaine+"A"+str(echelle(rayon))+" "+str(echelle(rayon))+" 0 1 1 "+str(transfo(fin[0]))+" "+str(transfo(fin[1]))+"\"  id="+id+" fill=\"none\"    stroke=\"none\"   stroke-width=\""+str(largeur)+"\" />\n"
    return chaine

def arcinvisible4(debut,fin,rayon,id="\" \"",largeur=LARGEUR):
    chaine="<path d=\"\n"
    chaine=chaine+"M"+str(transfo(debut[0]))+" "+str(transfo(debut[1]))+"\n"
    chaine=chaine+"A"+str(echelle(rayon))+" "+str(echelle(rayon))+" 0 0 1 "+str(transfo(fin[0]))+" "+str(transfo(fin[1]))+"\"  id="+id+" fill=\"none\"    stroke=\"none\"   stroke-width=\""+str(largeur)+"\" />\n"
    return chaine

def arc2(debut,fin,rayon,id="\" \"",largeur=LARGEUR,stroke="\"black\""):
    chaine="<path d=\"\n"
    chaine=chaine+"M"+str(transfo(debut[0]))+" "+str(transfo(debut[1]))+"\n"
    chaine=chaine+"A"+str(echelle(rayon))+" "+str(echelle(rayon))+" 0 1 0 "+str(transfo(fin[0]))+" "+str(transfo(fin[1]))+"\"  id="+id+" fill=\"none\" stroke="+stroke+"   stroke-width=\""+str(largeur)+"\" />\n"
    return chaine

def arc3(debut,fin,rayon,id="\" \"",largeur=LARGEUR,stroke="\"black\""):
    chaine="<path d=\"\n"
    chaine=chaine+"M"+str(transfo(debut[0]))+" "+str(transfo(debut[1]))+"\n"
    chaine=chaine+"A"+str(echelle(rayon))+" "+str(echelle(rayon))+" 0 1 1"+str(transfo(fin[0]))+" "+str(transfo(fin[1]))+"\"  id="+id+" fill=\"none\" stroke="+stroke+"   stroke-width=\""+str(largeur)+"\" />\n"
    return chaine

def arc4(debut,fin,rayon,id="\" \"",largeur=LARGEUR,stroke="\"black\""):
    chaine="<path d=\"\n"
    chaine=chaine+"M"+str(transfo(debut[0]))+" "+str(transfo(debut[1]))+"\n"
    chaine=chaine+"A"+str(echelle(rayon))+" "+str(echelle(rayon))+" 0 0 1"+str(transfo(fin[0]))+" "+str(transfo(fin[1]))+"\"  id="+id+" fill=\"none\" stroke="+stroke+"   stroke-width=\""+str(largeur)+"\" />\n"
    return chaine

def inter(theta,x):
    """
    Intersection d'une droite passant par le pole de l'ecliptique et un point de
    l'equateur avec le cercle de l'ecliptique
    theta : angle du point sur le cercle de l'equateur
    x: rayon de l'equateur
    """
    # Rayon de l'equateur
    Req=x
    # Le tropique du Capricorne
    rayoncap=x*tan(angle((90+23.45)/2))
    # Le tropique du Cancer
    rayoncan=x*tan(angle((90-23.45)/2))
    # Rayon de l'ecliptique
    R1=(rayoncap+rayoncan)/2
    # Distance du centre de l'astrolabe au centre de l'ecliptique
    d0=-x*tan(angle(23.45))
    # abscisse du centre de l'ecliptique
    p0=-x*tan(angle(23.45/2))
    xb=x*cos(angle(theta))
    yb=x*sin(angle(theta))

    A=(p0-yb)
    B=(yb-d0)
    delta=(A*B-xb*xb)*(A*B-xb*xb)-(xb*xb+A*A)*(B*B-R1*R1+xb*xb)
    alpha1=(xb*xb-A*B-sqrt(delta))/(xb*xb+A*A)
    alpha2=(xb*xb-A*B+sqrt(delta))/(xb*xb+A*A)
    return min(alpha1,alpha2)

def tympan(x):
    """
    x est le rayon de la sphere celeste
    """
    entete="<svg viewBox=\"0 0 "+str(TAILLE)+" "+str(TAILLE)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    image=open("tympan"+str(int(PHI))+".svg","w")
    image.write(entete)
    image.write(cercle(0,0,x, id="\"sphereceleste\""))
    #image.write(texte("Sphere celeste","sphereceleste"))
    # Le tropique du Capricorne
    rayoncap=x*tan(angle((90+23.45)/2))
    image.write(cercle(0,0,rayoncap, id="\"capricorne\""))
    #image.write(texte("Tropique du Capricorne","capricorne"))
    image.write(texte("Latitude "+str(round(PHI,2)),"capricorne",offset=23))
    
    # Un petit cercle au dessus du Capricorne
    rp=1.05*rayoncap
    image.write(cercle(0,0,rp, id="\"cercleexterne\""))
    #image.write(texte("Sud","capricorne",offset=74.4))

    # Un petit cercle invisible pour que le texte ne touche pas le tropique du Capricorne
    rp2=1.015*rayoncap
    image.write(cercleinvisible(0,0,rp2, id="\"cercleinvisible\""))
    image.write(texte("230","cercleinvisible",offset=decalsup[PHI][0]))
    image.write(texte("220","cercleinvisible",offset=decalsup[PHI][1]))
    image.write(texte("210","cercleinvisible",offset=decalsup[PHI][2]))
    image.write(texte("200","cercleinvisible",offset=decalsup[PHI][3]))
    image.write(texte("190","cercleinvisible",offset=decalsup[PHI][4]))
    image.write(texte("Sud","cercleinvisible",offset=decalsup[PHI][5]))
    image.write(texte("170","cercleinvisible",offset=decalsup[PHI][6]))
    image.write(texte("160","cercleinvisible",offset=decalsup[PHI][7]))
    image.write(texte("150","cercleinvisible",offset=decalsup[PHI][8]))
    image.write(texte("140","cercleinvisible",offset=decalsup[PHI][9]))
    image.write(texte("130","cercleinvisible",offset=decalsup[PHI][10]))
    
    
    
    # Le tropique du Cancer
    rayoncan=x*tan(angle((90-23.45)/2))
    image.write(cercle(0,0,rayoncan,id="\"cancer\""))
    #image.write(texte("Tropique du Cancer","cancer",offset=12))
    print(x," ",rayoncap," ",rayoncan)



         

    # le centre de la carte
    image.write(cercle(0,0,0.003,stroke="\"black\""))
    
    # Tracé du point zénithal et de l'horizon
    zenith=x*tan((angle((90-PHI)/2)))
    #---image.write(cercle(0,-zenith,0.01,stroke="\"blue\""))
    # Tracé de l'horizon
    # Projection gauche
    u=x*tan(angle((180-PHI)/2))
    # Projection coté droite
    up=x*tan(angle(PHI/2))
    rayonhor=(u+up)/2
    centre=rayonhor-up
    # un deuxieme cercle fantome pour bien positionner le texte
    rayonhorlarge=rayonhor*1.04
    #image.write(cercle(0,-centre,rayonhor,stroke="\"blue\"",  id="\"horizon0\"" ))
    
    #image.write(texte("Horizon pour la latitude "+str(PHI),"horizon0",offset=15))
    # En fait l'horizon doit s'arreter aux bords du Tropique du Capricorne
    # Les points de contact calcul
   
    v=(rayoncap*rayoncap-rayonhor*rayonhor+centre*centre)/(2*centre)
    u=sqrt(rayoncap*rayoncap-v*v)
    vp=(rayoncap*rayoncap-rayonhorlarge*rayonhorlarge+centre*centre)/(2*centre)
    up=sqrt(rayoncap*rayoncap-vp*vp)
    # Point gauche
    #image.write(cercle(-u,-v,0.01,stroke="\"blue\"" ))
    # Point droite
    #image.write(cercle(u,-v,0.01,stroke="\"blue\"" ))
    #image.write(arc((-u,-v),(u,-v),rayonhor,id="\"horizon\""))
    #image.write(arcgeneral((u,-v),(-u,-v),rayonhor,id="\"horizon\"",motif="0 0 0"))
    image.write(arc((-u,-v),(u,-v),rayonhor,id="\"horizon\""))
    #image.write(arcinvisible((-up,-vp),(up,-vp),rayonhorlarge,id="\"horizonlarge\""))
    if PHI==60:
     image.write(arc2((-u,-v),(u,-v),rayonhor,id="\"horizon\""))
     image.write(arcinvisible2((-up,-vp),(up,-vp),rayonhorlarge,id="\"horizonlarge\""))
    else:
     image.write(arcinvisible((-up,-vp),(up,-vp),rayonhorlarge,id="\"horizonlarge\""))
     image.write(arc((-u,-v),(u,-v),rayonhor,id="\"horizon\""))
    image.write(texte("250","horizonlarge",offset=decalages[PHI][0]))
    image.write(texte("Ouest","horizonlarge",offset=decalages[PHI][1]))
    image.write(texte("300","horizonlarge",offset=decalages[PHI][2]))
    image.write(texte("330","horizonlarge",offset=decalages[PHI][3]))
    image.write(texte("Nord","horizonlarge",offset=decalages[PHI][4]))
    image.write(texte("30","horizonlarge",offset=decalages[PHI][5]))
    image.write(texte("60","horizonlarge",offset=decalages[PHI][6]))
    image.write(texte("Est","horizonlarge",offset=decalages[PHI][7]))
    image.write(texte("110","horizonlarge",offset=decalages[PHI][8]))
    
    
    
   
    
    # Tracé des almucantarats
    k=0
    for i in range(5,90,5):
      k=k+1
    
      if (i<PHI):
        # Quand la hauteur est inferieure à la latitude
        alpha=(180-(PHI+i))/2
        alphap=(PHI-i)/2
        ax=x*tan(angle(alpha))
        axp=x*tan(angle(alphap))
        radi=(ax+axp)/2
        centre=radi-axp
       
          
       
        if centre+radi>rayoncap:
         #image.write(cercle(0,-centre,radi,stroke="\"blue\"" ))
         # Les points de contact calcul
         v=(rayoncap*rayoncap-radi*radi+centre*centre)/(2*centre)
         u=sqrt(rayoncap*rayoncap-v*v)
         # Point gauche
         #image.write(cercle(-u,-v,0.01,stroke="\"blue\"" ))
         # Point droite
         #image.write(cercle(u,-v,0.01,stroke="\"blue\"" ))
         #image.write(arc2((-u,-v),(u,-v),radi))
         # Les premiers arcs sont bizarres, selon la latitude
         # La modif courante ci-dessous ne marchent que distinguer les latitudes 44 et 50
         # (les intersections avec le tropique sont bonnes, mais on ne selectionne pas le bon arc)
         # L'arc suivant devient faux lui aussi pour PHI=30
         # Un gros todo
         
         if(i==5):
          if (PHI>45):   
           image.write(arc2((-u,-v),(u,-v),radi,largeur=LARGEUR/2)) 
          else:
           image.write(arc((-u,-v),(u,-v),radi,largeur=LARGEUR/2))  
          print(i)
         else:
          print("********--->",i)   
          if i%10!=0:   
           image.write(arc2((-u,-v),(u,-v),radi,largeur=LARGEUR/2))
          else:
           print("-->",i)    
           #image.write(arc2((-u,-v),(u,-v),radi,id="\""+str(i)+"\""))
           if (PHI!=30) or (i!=10):
              
            image.write(arc3((u,-v),(-u,-v),radi,id="\""+str(i)+"\""))
            image.write(texte(str(i),str(i),offset=decaldroit[PHI][(k-1)//2]))
            image.write(texte(str(i),str(i),offset=decalgauche[PHI][(k-1)//2]))
           
        else:
         
         if i%10!=0:
             image.write(cercle(0,-centre,radi,largeur=LARGEUR/2))
         else:
             image.write(cercle(0,-centre,radi,id="\""+str(i)+"\""))
             image.write(texte(str(i),str(i),offset=decaldroit[PHI][(k-1)//2]))
             image.write(texte(str(i),str(i),offset=decalgauche[PHI][(k-1)//2]))
      else:
       
        # Quand la hauteur est superieure à la latitude
        alpha=(180-(PHI+i))/2
        alphap=(i-PHI)/2
        ax=x*tan(angle(alpha))
        axp=x*tan(angle(alphap))
        radi=(ax-axp)/2
        centre=radi+axp
        if(i%10!=0):
         image.write(cercle(0,-centre,radi,largeur=LARGEUR/2 ))
        else:
         image.write(cercle(0,-centre,radi,id="\""+str(i)+"\"" ))
         if(i<=50):
          image.write(texte(str(i),str(i),offset=decaldroit[PHI][(k-1)//2]))
          image.write(texte(str(i),str(i),offset=decalgauche[PHI][(k-1)//2]))
        # Sauvegarde de l'almucantarat de 80°  
        if i==80:
         sauvegarde=((0,-centre),radi)
     
    # Tracé de l'almucantarat -18 degrés
    alpha=(180-(PHI-18))/2
    alphap=(PHI+18)/2
    ax=x*tan(angle(alpha))
    axp=x*tan(angle(alphap))
    rayon=(ax+axp)/2
    centre=rayon-axp
    #image.write(cercle(0,-centre,rayon,stroke="\"blue\"",  id="\"moins18\"" ))
    #image.write(texte("moins 18","moins18"))
    v=(rayoncap*rayoncap-rayon*rayon+centre*centre)/(2*centre)
    u=sqrt(rayoncap*rayoncap-v*v)
    # Point gauche
    #image.write(cercle(-u,-v,0.01,stroke="\"blue\"" ))
    # Point droite
    #image.write(cercle(u,-v,0.01,stroke="\"blue\"" ))
    image.write(arc((-u,-v),(u,-v),rayon ,  id="\"moins18\""))
    # l'arc invisible juste un peu plus petit pour pas que le texte touche la ligne
    rp=0.995*rayon
    vp=(rayoncap*rayoncap-rp*rp+centre*centre)/(2*centre)
    up=sqrt(rayoncap*rayoncap-vp*vp)
    image.write(arcinvisible((-up,-vp),(up,-vp),rp ,  id="\"moins18p\""))
    image.write(texte("-18","moins18p",offset=2))
    image.write(texte("-18","moins18p",offset=95))

       
    # les meridiens
    # Le premier vertical
    # cercle passant par le zenith et dont le centre est sur l'axe vertical de du tympan
    ax=x*tan(angle((90-PHI)/2))
    axp=x*tan(angle((90+PHI)/2))
    rayon=(ax+axp)/2
    #image.write(cercle(0,rayon-ax,rayon,stroke="\"orange\"" ))
    t,u=intersection(((0,rayon-ax),rayon),((0,-(rayonhor-x*tan(angle(PHI/2)))),rayonhor))
    #todo : deux arcs pour ne pas rentrer dans le cercle de 85
    image.write(arc(t,u,rayon))  


    # les autres cercles
    for i in range(5,90,5):
        distanceAuFoyer=rayon*tan(angle(i))
        radius=sqrt(rayon*rayon+distanceAuFoyer*distanceAuFoyer)
        #image.write(cercle(distanceAuFoyer,rayon-ax,radius,stroke="\"blue\"" ))
        #image.write(cercle(-distanceAuFoyer,rayon-ax,radius,stroke="\"red\"" ))
       
        # On commence a regarder pour les intersections
        # Cercle 1 : centre (distanceAuFoyer, rayon-ax), rayon radius
        # cercle 2 : cercle de l'horizon (0,-(rayonhor-x*tan(angle(PHI/2)),rayon rayonhor
       
        t,u=intersection(((distanceAuFoyer,rayon-ax),radius),((0,-(rayonhor-x*tan(angle(PHI/2)))),rayonhor))
        X1m=t[0]
        Y1m=t[1]
        X1mp=u[0]
        Y1mp=u[1]

        # Pareil avec le cercle du Capricorne
        t,u=intersection(((distanceAuFoyer,rayon-ax),radius),((0,0),rayoncap))
        X1c=t[0]
        Y1c=t[1]
        X1cp=u[0]
        Y1cp=u[1]

        #Intersection avec l'almucantarat de latitude 80 
        r,v=intersection(((distanceAuFoyer,rayon-ax),radius),sauvegarde)
        U1a=r[0]
        V1a=r[1]
        U1d=v[0]
        V1d=v[1]
        etapeArrivee=(U1a,V1a)
        etapeDepart=(U1d,V1d)

        
        if(X1c*X1c+Y1c*Y1c)>(X1m*X1m+Y1m*Y1m):
            depart=(X1m,Y1m)
            #image.write(cercle(X1m,Y1m,0.01,stroke="\"black\"" ))
        else:
            depart=(X1c,Y1c)
            #image.write(cercle(X1c,Y1c,0.01,stroke="\"black\"" ))
         
            
        if(X1cp*X1cp+Y1cp*Y1cp)<(X1mp*X1mp+Y1mp*Y1mp):
            arrivee=(X1cp,Y1cp)
            #image.write(cercle(X1cp,Y1cp,0.01,stroke="\"black\"" ))
        else:
            arrivee=(X1mp,Y1mp)
            #image.write(cercle(X1mp,Y1mp,0.01,stroke="\"black\"" ))
        if (i%10!=0):
         #todo : deux arcs pour ne pas rentrer dans le cercle de 85   
         #image.write(arc(depart,arrivee,radius,largeur=LARGEUR/2))
         image.write(arc(depart,etapeArrivee,radius,largeur=LARGEUR/2))
         image.write(arc(etapeDepart,arrivee,radius,largeur=LARGEUR/2))  
         print()
        else:
         #todo : deux arcs pour ne pas rentrer dans le cercle de 85   
         #image.write(arc(depart,arrivee,radius))
         image.write(arc(depart,etapeArrivee,radius))
         image.write(arc(etapeDepart,arrivee,radius))  
            
         # On commence a regarder pour les intersections
        # Cercle 1 : centre (distanceAuFoyer, rayon-ax), rayon radius
        # cercle 2 : cercle de l'horizon (0,-(rayonhor-x*tan(angle(PHI/2)),rayon rayonhor
        
        t,u=intersection(((-distanceAuFoyer,rayon-ax),radius),((0,-(rayonhor-x*tan(angle(PHI/2)))),rayonhor))
        X1m=t[0]
        Y1m=t[1]
        X1mp=u[0]
        Y1mp=u[1]

        #Intersection avec l'almucantarat de latitude 80 
        r,v=intersection(((-distanceAuFoyer,rayon-ax),radius),sauvegarde)
        U1a=r[0]
        V1a=r[1]
        U1d=v[0]
        V1d=v[1]
        etapeArrivee=(U1a,V1a)
        etapeDepart=(U1d,V1d)

        t,u=intersection(((-distanceAuFoyer,rayon-ax),radius),((0,0),rayoncap))
        X1c=t[0]
        Y1c=t[1]
        X1cp=u[0]
        Y1cp=u[1]
        
        if(X1c*X1c+Y1c*Y1c)>(X1m*X1m+Y1m*Y1m):
            depart=(X1m,Y1m)
            #image.write(cercle(X1m,Y1m,0.01,stroke="\"black\"" ))
        else:
            depart=(X1c,Y1c)
            #image.write(cercle(X1c,Y1c,0.01,stroke="\"black\"" ))
         
            
        if(X1cp*X1cp+Y1cp*Y1cp)<(X1mp*X1mp+Y1mp*Y1mp):
            arrivee=(X1cp,Y1cp)
            #image.write(cercle(X1cp,Y1cp,0.01,stroke="\"black\"" ))
        else:
            arrivee=(X1mp,Y1mp)
            #image.write(cercle(X1mp,Y1mp,0.01,stroke="\"black\"" ))
            
        if (i%10!=0):
         #todo : deux arcs pour ne pas rentrer dans le cercle de 85   
         #image.write(arc(depart,arrivee,radius,largeur=LARGEUR/2))
         image.write(arc(depart,etapeArrivee,radius,largeur=LARGEUR/2))
         image.write(arc(etapeDepart,arrivee,radius,largeur=LARGEUR/2))  
         print()   
            
        else:
         #todo : deux arcs pour ne pas rentrer dans le cercle de 85   
         #image.write(arc(depart,arrivee,radius))
         image.write(arc(depart,etapeArrivee,radius))
         image.write(arc(etapeDepart,arrivee,radius))  
    
      
    #Il manque une petite droite verticale
    image.write(ligne((0,-rayoncap),(0,rayoncan)))
    # TODO : cette partie peut constituer un anneau à part dans lequel s'inserera le tympan (voir schema dsn un cahier quelque part)
    #image.write(ligne((-rayoncap*1.2,0),(rayoncap*1.2,0)))
    #Graduation des angles horaires
    swip=-0.27
    minhor=rayoncap*(5.3/4.6)
    image.write(cercle(0,0,minhor,stroke="\"red\""))
    image.write(cercleinvisible(0,0,minhor*1.014,id="\"basechiffre\""))
    maxhor=rayoncap*(5.6/4.6)
    image.write(cercle(0,0,maxhor,stroke="\"red\""))
    image.write(texte("06","basechiffre",offset=0+swip))
    image.write(texte("0","basechiffre",offset=99.65))
    for i in range(1,24):
        dec=(30-i)%24
        if dec==0:
            dec=24
        chaine=str(dec)
        if dec<10:
            chaine="0"+chaine
       
        image.write(texte(chaine,"basechiffre",offset=swip+(i*100)/24))
    for i in range(0,96):
         cosy=cos(2*pi*i/96)
         siny=sin(2*pi*i/96)
         if (i%4==0):
          image.write(ligne((cosy*minhor,siny*minhor),(cosy*maxhor,siny*maxhor)))
         else:
          image.write(ligne((cosy*minhor,siny*minhor),(cosy*(minhor*1.02),siny*(minhor*1.02))))


    maxhor=rayoncap*(5.6/4.6)
    # trou de la vis / pour une taille exterieure de 20 cm
    image.write(cercle(0,0,0.02*maxhor,stroke="\"red\""))      
    image.write(pied)
    image.close()

   

"""
Tympan seul sans le tour
"""
def tympanseul(x):
    """
    x est le rayon de la sphere celeste
    """
    entete="<svg viewBox=\"0 0 "+str(TAILLE)+" "+str(TAILLE)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    image=open("tympan"+str(int(PHI))+"seul.svg","w")
    image.write(entete)
    image.write(cercle(0,0,x, id="\"sphereceleste\""))
    #image.write(texte("Sphere celeste","sphereceleste"))
    # Le tropique du Capricorne
    rayoncap=x*tan(angle((90+23.45)/2))
    image.write(cercle(0,0,rayoncap, id="\"capricorne\""))
    #image.write(texte("Tropique du Capricorne","capricorne"))
    image.write(texte("Latitude "+str(round(PHI,2)),"capricorne",offset=23))
    
    # Un petit cercle au dessus du Capricorne
    rp=1.05*rayoncap
    image.write(cercle(0,0,rp, id="\"cercleexterne\""))
    #image.write(texte("Sud","capricorne",offset=74.4))

    # Un petit cercle invisible pour que le texte ne touche pas le tropique du Capricorne
    rp2=1.015*rayoncap
    image.write(cercleinvisible(0,0,rp2, id="\"cercleinvisible\""))
    image.write(texte("230","cercleinvisible",offset=decalsup[PHI][0]))
    image.write(texte("220","cercleinvisible",offset=decalsup[PHI][1]))
    image.write(texte("210","cercleinvisible",offset=decalsup[PHI][2]))
    image.write(texte("200","cercleinvisible",offset=decalsup[PHI][3]))
    image.write(texte("190","cercleinvisible",offset=decalsup[PHI][4]))
    image.write(texte("Sud","cercleinvisible",offset=decalsup[PHI][5]))
    image.write(texte("170","cercleinvisible",offset=decalsup[PHI][6]))
    image.write(texte("160","cercleinvisible",offset=decalsup[PHI][7]))
    image.write(texte("150","cercleinvisible",offset=decalsup[PHI][8]))
    image.write(texte("140","cercleinvisible",offset=decalsup[PHI][9]))
    image.write(texte("130","cercleinvisible",offset=decalsup[PHI][10]))
    
    
    
    # Le tropique du Cancer
    rayoncan=x*tan(angle((90-23.45)/2))
    image.write(cercle(0,0,rayoncan,id="\"cancer\""))
    #image.write(texte("Tropique du Cancer","cancer",offset=12))
    print(x," ",rayoncap," ",rayoncan)



         

    # le centre de la carte
    image.write(cercle(0,0,0.003,stroke="\"black\""))
    
    # Tracé du point zénithal et de l'horizon
    zenith=x*tan((angle((90-PHI)/2)))
    #---image.write(cercle(0,-zenith,0.01,stroke="\"blue\""))
    # Tracé de l'horizon
    # Projection gauche
    u=x*tan(angle((180-PHI)/2))
    # Projection coté droite
    up=x*tan(angle(PHI/2))
    rayonhor=(u+up)/2
    centre=rayonhor-up
    # un deuxieme cercle fantome pour bien positionner le texte
    rayonhorlarge=rayonhor*1.04
    #image.write(cercle(0,-centre,rayonhor,stroke="\"blue\"",  id="\"horizon0\"" ))
    
    #image.write(texte("Horizon pour la latitude "+str(PHI),"horizon0",offset=15))
    # En fait l'horizon doit s'arreter aux bords du Tropique du Capricorne
    # Les points de contact calcul
   
    v=(rayoncap*rayoncap-rayonhor*rayonhor+centre*centre)/(2*centre)
    u=sqrt(rayoncap*rayoncap-v*v)
    vp=(rayoncap*rayoncap-rayonhorlarge*rayonhorlarge+centre*centre)/(2*centre)
    up=sqrt(rayoncap*rayoncap-vp*vp)
    # Point gauche
    #image.write(cercle(-u,-v,0.01,stroke="\"blue\"" ))
    # Point droite
    #image.write(cercle(u,-v,0.01,stroke="\"blue\"" ))
    #image.write(arc((-u,-v),(u,-v),rayonhor,id="\"horizon\""))
    #image.write(arcgeneral((u,-v),(-u,-v),rayonhor,id="\"horizon\"",motif="0 0 0"))
    image.write(arc((-u,-v),(u,-v),rayonhor,id="\"horizon\""))
    #image.write(arcinvisible((-up,-vp),(up,-vp),rayonhorlarge,id="\"horizonlarge\""))
    if PHI==60:
     image.write(arc2((-u,-v),(u,-v),rayonhor,id="\"horizon\""))
     image.write(arcinvisible2((-up,-vp),(up,-vp),rayonhorlarge,id="\"horizonlarge\""))
    else:
     image.write(arcinvisible((-up,-vp),(up,-vp),rayonhorlarge,id="\"horizonlarge\""))
     image.write(arc((-u,-v),(u,-v),rayonhor,id="\"horizon\""))
    image.write(texte("250","horizonlarge",offset=decalages[PHI][0]))
    image.write(texte("Ouest","horizonlarge",offset=decalages[PHI][1]))
    image.write(texte("300","horizonlarge",offset=decalages[PHI][2]))
    image.write(texte("330","horizonlarge",offset=decalages[PHI][3]))
    image.write(texte("Nord","horizonlarge",offset=decalages[PHI][4]))
    image.write(texte("30","horizonlarge",offset=decalages[PHI][5]))
    image.write(texte("60","horizonlarge",offset=decalages[PHI][6]))
    image.write(texte("Est","horizonlarge",offset=decalages[PHI][7]))
    image.write(texte("110","horizonlarge",offset=decalages[PHI][8]))
    
    
    
   
    
    # Tracé des almucantarats
    k=0
    for i in range(5,90,5):
      k=k+1
    
      if (i<PHI):
        # Quand la hauteur est inferieure à la latitude
        alpha=(180-(PHI+i))/2
        alphap=(PHI-i)/2
        ax=x*tan(angle(alpha))
        axp=x*tan(angle(alphap))
        radi=(ax+axp)/2
        centre=radi-axp
       
          
       
        if centre+radi>rayoncap:
         #image.write(cercle(0,-centre,radi,stroke="\"blue\"" ))
         # Les points de contact calcul
         v=(rayoncap*rayoncap-radi*radi+centre*centre)/(2*centre)
         u=sqrt(rayoncap*rayoncap-v*v)
         # Point gauche
         #image.write(cercle(-u,-v,0.01,stroke="\"blue\"" ))
         # Point droite
         #image.write(cercle(u,-v,0.01,stroke="\"blue\"" ))
         #image.write(arc2((-u,-v),(u,-v),radi))
         # Les premiers arcs sont bizarre, selon la latitude
         # La modif courante ci-dessous ne marchent que distinguer les latitudes 44 et 50
         # (les intersections avec le tropique sont bonnes, mais on ne selectionne pas le bon arc)
         # L'arc suivant devient faux lui aussi pour PHI=30
         # Un gros todo
         
         if(i==5):
          if (PHI>45):   
           image.write(arc2((-u,-v),(u,-v),radi,largeur=LARGEUR/2)) 
          else:
           image.write(arc((-u,-v),(u,-v),radi,largeur=LARGEUR/2))  
          print(i)
         else:
          if i%10!=0:   
           image.write(arc2((-u,-v),(u,-v),radi,largeur=LARGEUR/2))
          else:
           #image.write(arc2((-u,-v),(u,-v),radi,id="\""+str(i)+"\""))
           image.write(arc3((u,-v),(-u,-v),radi,id="\""+str(i)+"\""))
           image.write(texte(str(i),str(i),offset=decaldroit[PHI][(k-1)//2]))
           image.write(texte(str(i),str(i),offset=decalgauche[PHI][(k-1)//2]))
           
        else:
         
         if i%10!=0:
             image.write(cercle(0,-centre,radi,largeur=LARGEUR/2))
         else:
             image.write(cercle(0,-centre,radi,id="\""+str(i)+"\""))
             image.write(texte(str(i),str(i),offset=decaldroit[PHI][(k-1)//2]))
             image.write(texte(str(i),str(i),offset=decalgauche[PHI][(k-1)//2]))
      else:
       
        # Quand la hauteur est superieure à la latitude
        alpha=(180-(PHI+i))/2
        alphap=(i-PHI)/2
        ax=x*tan(angle(alpha))
        axp=x*tan(angle(alphap))
        radi=(ax-axp)/2
        centre=radi+axp
        if(i%10!=0):
         image.write(cercle(0,-centre,radi,largeur=LARGEUR/2 ))
        else:
         image.write(cercle(0,-centre,radi,id="\""+str(i)+"\"" ))
         if(i<=50):
          image.write(texte(str(i),str(i),offset=decaldroit[PHI][(k-1)//2]))
          image.write(texte(str(i),str(i),offset=decalgauche[PHI][(k-1)//2]))
        # Sauvegarde de l'almucantarat de 80°  
        if i==80:
         sauvegarde=((0,-centre),radi)
     
    # Tracé de l'almucantarat -18 degrés
    alpha=(180-(PHI-18))/2
    alphap=(PHI+18)/2
    ax=x*tan(angle(alpha))
    axp=x*tan(angle(alphap))
    rayon=(ax+axp)/2
    centre=rayon-axp
    #image.write(cercle(0,-centre,rayon,stroke="\"blue\"",  id="\"moins18\"" ))
    #image.write(texte("moins 18","moins18"))
    v=(rayoncap*rayoncap-rayon*rayon+centre*centre)/(2*centre)
    u=sqrt(rayoncap*rayoncap-v*v)
    # Point gauche
    #image.write(cercle(-u,-v,0.01,stroke="\"blue\"" ))
    # Point droite
    #image.write(cercle(u,-v,0.01,stroke="\"blue\"" ))
    image.write(arc((-u,-v),(u,-v),rayon ,  id="\"moins18\""))
    # l'arc invisible juste un peu plus petit pour pas que le texte touche la ligne
    rp=0.995*rayon
    vp=(rayoncap*rayoncap-rp*rp+centre*centre)/(2*centre)
    up=sqrt(rayoncap*rayoncap-vp*vp)
    image.write(arcinvisible((-up,-vp),(up,-vp),rp ,  id="\"moins18p\""))
    image.write(texte("-18","moins18p",offset=2))
    image.write(texte("-18","moins18p",offset=95))

       
    # les meridiens
    # Le premier vertical
    # cercle passant par le zenith et dont le centre est sur l'axe vertical de du tympan
    ax=x*tan(angle((90-PHI)/2))
    axp=x*tan(angle((90+PHI)/2))
    rayon=(ax+axp)/2
    #image.write(cercle(0,rayon-ax,rayon,stroke="\"orange\"" ))
    t,u=intersection(((0,rayon-ax),rayon),((0,-(rayonhor-x*tan(angle(PHI/2)))),rayonhor))
    #todo : deux arcs pour ne pas rentrer dans le cercle de 85
    image.write(arc(t,u,rayon))  


    # les autres cercles
    for i in range(5,90,5):
        distanceAuFoyer=rayon*tan(angle(i))
        radius=sqrt(rayon*rayon+distanceAuFoyer*distanceAuFoyer)
        #image.write(cercle(distanceAuFoyer,rayon-ax,radius,stroke="\"blue\"" ))
        #image.write(cercle(-distanceAuFoyer,rayon-ax,radius,stroke="\"red\"" ))
       
        # On commence a regarder pour les intersections
        # Cercle 1 : centre (distanceAuFoyer, rayon-ax), rayon radius
        # cercle 2 : cercle de l'horizon (0,-(rayonhor-x*tan(angle(PHI/2)),rayon rayonhor
       
        t,u=intersection(((distanceAuFoyer,rayon-ax),radius),((0,-(rayonhor-x*tan(angle(PHI/2)))),rayonhor))
        X1m=t[0]
        Y1m=t[1]
        X1mp=u[0]
        Y1mp=u[1]

        # Pareil avec le cercle du Capricorne
        t,u=intersection(((distanceAuFoyer,rayon-ax),radius),((0,0),rayoncap))
        X1c=t[0]
        Y1c=t[1]
        X1cp=u[0]
        Y1cp=u[1]

        #Intersection avec l'almucantarat de latitude 80 
        r,v=intersection(((distanceAuFoyer,rayon-ax),radius),sauvegarde)
        U1a=r[0]
        V1a=r[1]
        U1d=v[0]
        V1d=v[1]
        etapeArrivee=(U1a,V1a)
        etapeDepart=(U1d,V1d)

        
        if(X1c*X1c+Y1c*Y1c)>(X1m*X1m+Y1m*Y1m):
            depart=(X1m,Y1m)
            #image.write(cercle(X1m,Y1m,0.01,stroke="\"black\"" ))
        else:
            depart=(X1c,Y1c)
            #image.write(cercle(X1c,Y1c,0.01,stroke="\"black\"" ))
         
            
        if(X1cp*X1cp+Y1cp*Y1cp)<(X1mp*X1mp+Y1mp*Y1mp):
            arrivee=(X1cp,Y1cp)
            #image.write(cercle(X1cp,Y1cp,0.01,stroke="\"black\"" ))
        else:
            arrivee=(X1mp,Y1mp)
            #image.write(cercle(X1mp,Y1mp,0.01,stroke="\"black\"" ))
        if (i%10!=0):
         #todo : deux arcs pour ne pas rentrer dans le cercle de 85   
         #image.write(arc(depart,arrivee,radius,largeur=LARGEUR/2))
         image.write(arc(depart,etapeArrivee,radius,largeur=LARGEUR/2))
         image.write(arc(etapeDepart,arrivee,radius,largeur=LARGEUR/2))  
         print()
        else:
         #todo : deux arcs pour ne pas rentrer dans le cercle de 85   
         #image.write(arc(depart,arrivee,radius))
         image.write(arc(depart,etapeArrivee,radius))
         image.write(arc(etapeDepart,arrivee,radius))  
            
         # On commence a regarder pour les intersections
        # Cercle 1 : centre (distanceAuFoyer, rayon-ax), rayon radius
        # cercle 2 : cercle de l'horizon (0,-(rayonhor-x*tan(angle(PHI/2)),rayon rayonhor
        
        t,u=intersection(((-distanceAuFoyer,rayon-ax),radius),((0,-(rayonhor-x*tan(angle(PHI/2)))),rayonhor))
        X1m=t[0]
        Y1m=t[1]
        X1mp=u[0]
        Y1mp=u[1]

        #Intersection avec l'almucantarat de latitude 80 
        r,v=intersection(((-distanceAuFoyer,rayon-ax),radius),sauvegarde)
        U1a=r[0]
        V1a=r[1]
        U1d=v[0]
        V1d=v[1]
        etapeArrivee=(U1a,V1a)
        etapeDepart=(U1d,V1d)

        t,u=intersection(((-distanceAuFoyer,rayon-ax),radius),((0,0),rayoncap))
        X1c=t[0]
        Y1c=t[1]
        X1cp=u[0]
        Y1cp=u[1]
        
        if(X1c*X1c+Y1c*Y1c)>(X1m*X1m+Y1m*Y1m):
            depart=(X1m,Y1m)
            #image.write(cercle(X1m,Y1m,0.01,stroke="\"black\"" ))
        else:
            depart=(X1c,Y1c)
            #image.write(cercle(X1c,Y1c,0.01,stroke="\"black\"" ))
         
            
        if(X1cp*X1cp+Y1cp*Y1cp)<(X1mp*X1mp+Y1mp*Y1mp):
            arrivee=(X1cp,Y1cp)
            #image.write(cercle(X1cp,Y1cp,0.01,stroke="\"black\"" ))
        else:
            arrivee=(X1mp,Y1mp)
            #image.write(cercle(X1mp,Y1mp,0.01,stroke="\"black\"" ))
            
        if (i%10!=0):
         #todo : deux arcs pour ne pas rentrer dans le cercle de 85   
         #image.write(arc(depart,arrivee,radius,largeur=LARGEUR/2))
         image.write(arc(depart,etapeArrivee,radius,largeur=LARGEUR/2))
         image.write(arc(etapeDepart,arrivee,radius,largeur=LARGEUR/2))  
         print()   
            
        else:
         #todo : deux arcs pour ne pas rentrer dans le cercle de 85   
         #image.write(arc(depart,arrivee,radius))
         image.write(arc(depart,etapeArrivee,radius))
         image.write(arc(etapeDepart,arrivee,radius))  
    
      
    #Il manque une petite droite verticale
    image.write(ligne((0,-rayoncap),(0,rayoncan)))
    # TODO : cette partie peut constituer un anneau à part dans lequel s'inserera le tympan (voir schema dsn un cahier quelque part)
    #image.write(ligne((-rayoncap*1.2,0),(rayoncap*1.2,0)))
    #Graduation des angles horaires
    swip=-0.27
    minhor=rayoncap*(5.3/4.6)
    image.write(cercle(0,0,minhor,stroke="\"red\""))
    """
    image.write(cercleinvisible(0,0,minhor*1.014,id="\"basechiffre\""))
    maxhor=rayoncap*(5.6/4.6)
    image.write(cercle(0,0,maxhor,stroke="\"red\""))
    image.write(texte("06","basechiffre",offset=0+swip))
    image.write(texte("0","basechiffre",offset=99.65))
    for i in range(1,24):
        dec=(30-i)%24
        if dec==0:
            dec=24
        chaine=str(dec)
        if dec<10:
            chaine="0"+chaine
       
        image.write(texte(chaine,"basechiffre",offset=swip+(i*100)/24))
    for i in range(0,96):
         cosy=cos(2*pi*i/96)
         siny=sin(2*pi*i/96)
         if (i%4==0):
          image.write(ligne((cosy*minhor,siny*minhor),(cosy*maxhor,siny*maxhor)))
         else:
          image.write(ligne((cosy*minhor,siny*minhor),(cosy*(minhor*1.02),siny*(minhor*1.02))))

    """
    maxhor=rayoncap*(5.6/4.6)
    # trou de la vis / pour une taille exterieure de 20 cm
    image.write(cercle(0,0,0.02*maxhor,stroke="\"red\""))      
    image.write(pied)
    image.close()
   
    
    
debutsmois=[0,30.575,58.192,88.767,118.356,148.931,178.520,209.096,239.671,269.260,299.836,329.425]
nomsmois=["JANVIER","FEVRIER","MARS","AVRIL","MAI","JUIN","JUILLET","AOUT","SEPTEMBRE","OCTOBRE","NOVEMBRE","DECEMBRE"]
calendrier=[(5,3.945),(10,8.877),(15,13.808),(20,18.74),(25,23.671),(30,28.601),
            (5,34.52),(10,39.452),(15,44.383),(20,49.315),(25,54.246),
            (5,62.137),(10,67.068),(15,72.0),(20,76.931),(25,81.863),(30,86.794),
            (5,92.712),(10,97.644),(15,102.575),(20,107.507),(25,112.438),(30,117.37),
            (5,122.301),(10,127.233),(15,132.164),(20,137.096),(25,142.027),(30,146.959),
            (5,152.877),(10,157.808),(15,162.74),(20,167.671),(25,172.603),(30,177.534),
            (5,182.466),(10,187.397),(15,192.329),(20,197.26),(25,202.292),(30,207.123),
            (5,213.041),(10,217.973),(15,222.904),(20,227.836),(25,232.767),(30,237.699),
            (5,243.616),(10,248.548),(15,253.479),(20,258.411),(25,263.342),(30,268.274),
            (5,273.205),(10,278.137),(15,283.068),(20,288.0),(25,292.931),(30,297.863),
            (5,303.781),(10,308.712),(15,313.644),(20,318.575),(25,323.507),(30,328.438),
            (5,333.37),(10,338.301),(15,343.233),(20,348.164),(25,353.096),(30,358.027)]
# 28 etoiles remarquables
# Pour chacune : son nom, l'angle par rapport au point vernal, sa distance au centre de
# l'astrolabe si la sphère celeste a un rayon de 5cm
etoiles=[("Sirrah",2.744,2.924),("Schedir",10.845,1.49),("Deneb",11.521,6.846),("Menkar",46.225,4.639),("Mirfak",51.981,1.818),
         ("Aldebaran",69.698,3.726),("Rigel",79.236,5.767),("Capella",80.097,2.018),("Arneb",83.734,6.855),("Betelgeuse",89.470,4.392),
         ("Sirius",101.846,6.729),("Castor",114.448,2.784),("Procyon",115.489,4.573),("Alphard",142.511,5.842),
         ("Alkes",165.561,6.954),("Dubbe",166.695,1.271),("Denebola",177.909,3.886),("L\'Epi",201.959,6.111),
         ("Arcturus",214.502,3.570),("Zuben",229.928,5.913),("Gemma",234.2,3.091),("Unuk",236.682,4.481),
         ("Ras Alhague",264.313,4.011),("Vega",269.654,2.394),("Altaïr",298.298,4.270),("Gredi",305.205,6.217),
         ("Scheddih",327.444,6.622),("Markab",346.813,3.804)]
"""


                                                                    RETE

"""
def rete(x):
    entete="<svg viewBox=\"0 0 "+str(TAILLE)+" "+str(TAILLE)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    image=open("astrolabe_rete.svg","w")
    image.write(entete)
    #rayon du tropique du Capricorne
    rayoncap=x*tan(angle((90+23.45)/2))
    #image.write(cercle(0,0,rayoncap,stroke="\"red\"", id="\"capricorne\""))
    # Une copie pour le trace du rete
    #image.write(cercle(0,0,rayoncap,stroke="\"green\""))
    # rayon du tropique du Cancer
    rayoncan=x*tan(angle((90-23.45)/2))
    #image.write(cercle(0,0,rayoncan,stroke="\"red\"", id="\"cancer\""))
    #image.write(texte("Tropique du Cancer","cancer",offset=12))
    # le centre de la carte
    image.write(cercle(0,0,0.003,stroke="\"black\""))
    # cercle auxiliaire pour fabriquer le rete (petit cercle central)
    petitrayon=0.05
    image.write(cercle(0,0,petitrayon,stroke="\"green\""))
    # L'ecliptique
    rayonecli=(rayoncap+rayoncan)/2
    centre=x*tan(angle(23.45))
    print(centre)
    image.write(cercle(0,-centre,rayonecli,stroke="\"black\"", id="\"ecliptique\""))
    # Une copie qui sera modifiee
    #image.write(cercle(0,-centre,rayonecli,stroke="\"green\""))
    # Un cercle interne plus petit
    image.write(cercle(0,-centre,rayonecli*0.94,stroke="\"black\""))
    # Une copie qui sera modifiee
    #image.write(cercle(0,-centre,rayonecli*0.94,stroke="\"green\""))
    image.write(cercleinvisible(0,-centre,rayonecli*0.95, id="\"ecliptiqueinterne\""))
    
    # Ajouter des arcs pour relier les cercles verts, et pouvoir y mettre des pointes pour les etoiles

    # Entre l'eliptique et le centre de l'appareil
    angleEcliptique=3*pi/2
    rayonEcliptique=rayonecli*0.94
    anglePetit=3*pi/2
    da=0.65
    de=0.1
    # A droite vers le haut
    image.write(arc4((rayonEcliptique*cos(angleEcliptique),rayonEcliptique*sin(angleEcliptique)-centre),(petitrayon*cos(anglePetit) ,petitrayon*sin(anglePetit) ),0.5,stroke="\"green\""))
    image.write(arc4((rayonEcliptique*cos(angleEcliptique+de),rayonEcliptique*sin(angleEcliptique+de)-centre),(petitrayon*cos(anglePetit+da) ,petitrayon*sin(anglePetit+da) ),0.5,stroke="\"green\""))
    # A gauche vers le haut
    image.write(arc((rayonEcliptique*cos(angleEcliptique),rayonEcliptique*sin(angleEcliptique)-centre),(petitrayon*cos(anglePetit) ,petitrayon*sin(anglePetit) ),0.5,stroke="\"green\""))
    image.write(arc((rayonEcliptique*cos(angleEcliptique-de),rayonEcliptique*sin(angleEcliptique-de)-centre),(petitrayon*cos(anglePetit-da) ,petitrayon*sin(anglePetit-da) ),0.5,stroke="\"green\""))
    # A droite sur le cote
    eclip=0.72 # 0.45
    de=0.075
    radiogougou=0.4
    image.write(arc((rayonEcliptique*cos(eclip),rayonEcliptique*sin(eclip)-centre),(petitrayon*cos(anglePetit+da) ,petitrayon*sin(anglePetit+da) ),radiogougou,stroke="\"green\""))
    image.write(arc((rayonEcliptique*cos(eclip+de),rayonEcliptique*sin(eclip+de)-centre),(petitrayon*cos(anglePetit+2*da) ,petitrayon*sin(anglePetit+2*da) ),radiogougou,stroke="\"green\""))
    # A gauche sur le cote
    image.write(arc4((rayonEcliptique*cos(pi-eclip),rayonEcliptique*sin(pi-eclip)-centre),(petitrayon*cos(pi-anglePetit-da) ,petitrayon*sin(pi-anglePetit-da) ),radiogougou,stroke="\"green\""))
    image.write(arc4((rayonEcliptique*cos(pi-eclip-de),rayonEcliptique*sin(pi-eclip-de)-centre),(petitrayon*cos(pi-anglePetit-2*da) ,petitrayon*sin(pi-anglePetit-2*da) ),radiogougou,stroke="\"green\""))

    # On recommence pour les arches entre l'ecliptique et le cercle du tropique du Capricorne
    # A droite en haut
    de=0.19
    dcap=0.42
    zipe=0.05
    zipc=0.05
    rayoninternecal=1.06*rayoncap
   
    # A droite en haut
    image.write(arc4((rayonecli*cos(-de),rayonecli*sin(-de)-centre),(rayoninternecal*cos(-dcap) ,rayoninternecal*sin(-dcap) ),0.5,stroke="\"green\""))
    image.write(arc4((rayonecli*cos(-de+zipe),rayonecli*sin(-de+zipe)-centre),(rayoninternecal*cos(-dcap+zipc) ,rayoninternecal*sin(-dcap+zipc) ),0.5,stroke="\"green\""))

    # A gauche en haut
    image.write(arc((rayonecli*cos(pi+de),rayonecli*sin(pi+de)-centre),(rayoninternecal*cos(pi+dcap) ,rayoninternecal*sin(pi+dcap) ),0.5,stroke="\"green\""))
    image.write(arc((rayonecli*cos(pi+de-zipe),rayonecli*sin(pi+de-zipe)-centre),(rayoninternecal*cos(pi+dcap-zipc) ,rayoninternecal*sin(pi+dcap-zipc) ),0.5,stroke="\"green\""))

    de=0.75
    dcap=0.35
    zipe=0.05
    zipc=0.05
    rapy=0.97
    # Au milieu a droite
    image.write(arc((rayonecli*cos(rapy*de),rayonecli*sin(de*rapy)-centre),(rayoninternecal*cos(dcap) ,rayoninternecal*sin(dcap) ),0.5,stroke="\"green\""))
    image.write(arc((rayonecli*cos(de+zipe),rayonecli*sin(de+zipe)-centre),(rayoninternecal*cos(dcap+zipc) ,rayoninternecal*sin(dcap+zipc) ),0.5,stroke="\"green\""))

    # Au milieu a gauche
    image.write(arc4((rayonecli*cos(pi-de*rapy),rayonecli*sin(pi-de*rapy)-centre),(rayoninternecal*cos(pi-dcap) ,rayoninternecal*sin(pi-dcap) ),0.5,stroke="\"green\""))
    image.write(arc4((rayonecli*cos(pi-de-zipe),rayonecli*sin(pi-de-zipe)-centre),(rayoninternecal*cos(pi-dcap-zipc) ,rayoninternecal*sin(pi-dcap-zipc) ),0.5,stroke="\"green\""))

    de=pi/4
    rapy=1.07
    # et puis l'arche du milieu en bas
    image.write(arc4((rayoninternecal*cos(pi-de),rayoninternecal*sin(pi-de)),(rayoninternecal*cos(de) ,rayoninternecal*sin(de) ),1.7,stroke="\"green\""))
    image.write(arc4((rayoninternecal*cos(pi-de*rapy),rayoninternecal*sin(pi-de*rapy)),(rayoninternecal*cos(de*rapy) ,rayoninternecal*sin(de*rapy)),1.7,stroke="\"green\""))
    
   
    
    # Pole de l'ecliptique
    pole=x*tan(angle(23.45/2))
    p0=-pole
    #image.write(cercle(0,-pole,0.003,stroke="\"green\""))
    # le centre de l'ecliptique
    image.write(cercle(0,-centre,0.003,stroke="\"blue\""))
    # Tracés auxiliaires pour graduer l'ecliptique (page 9)
    #image.write(cercle(0,0,x,stroke="\"red\"", id="\"sphereceleste\""))
    #image.write(texte("equateur","sphereceleste"))
    for theta in range(0,360,5):
        alpha=inter(theta,x)
        point=((1-alpha)*x*cos(angle(theta)),alpha*p0+(1-alpha)*x*sin(angle(theta)))
        #image.write(cercle(x*cos(angle(theta)),x*sin(angle(theta)),0.0015,stroke="\"black\""))
        #image.write(cercle(point[0],point[1],0.0015,stroke="\"red\""))
        if theta%10==0:
         image.write(ligne(point,(0.965*point[0],0.965*point[1])))
        else:
         image.write(ligne(point,(0.98*point[0],0.98*point[1])))  
        # Bien placer les graduations
        if(theta%30==0):
         alpha=(atan2(point[1]+centre,point[0])/pi*180)/360*100
         decal=0
         if (theta>10):
             decal=199.5
         if(theta>=100):
             decal=199
         image.write(texte(str(theta),"ecliptiqueinterne",offset=((alpha+100+decal)%100)))

    # Traçage du calendrier
    rayoninternecal=1.06*rayoncap
    rayonexternecal=1.14*rayoncap
    rayoninvisible=1.005*rayoninternecal
    rinv2=0.97*rayonexternecal
    image.write(cercle(0,0,rayoninternecal))
    image.write(cercle(0,0,rayonexternecal))
    image.write(cercleinvisible(0,0,rayoninvisible,id="\"calendar\""))
    image.write(cercleinvisible(0,0,rinv2,id="\"graduations\""))
    # tracé des démarcations entre les mois et des noms des mois
    # TODO : ajuster le centrage du nom des mois en fonction de la longueur du mot
    for i in range(0,12):
        ang=280+debutsmois[i]
        cosy=cos(angle(ang))
        siny=sin(angle(ang))
        haut=(rayonexternecal*cosy,rayonexternecal*siny)
        bas=(rayoninternecal*cosy,rayoninternecal*siny)
        image.write(ligne(haut,bas))
        if(i!=11):
         center=280+(debutsmois[i]+debutsmois[(i+1)%12])/2
        else :
         center=280+(debutsmois[i]+debutsmois[(i+1)%12]+360)/2
        decal=(center/360*100+99)%100
        image.write(texte(nomsmois[i],"calendar",offset=decal))
        print(nomsmois[i]," ",decal)
    # Graduations quinquennales    
    for obj in calendrier:
        ang=280+obj[1]
        cosy=cos(angle(ang))
        siny=sin(angle(ang))
        haut=(rayonexternecal*cosy,rayonexternecal*siny)
        if obj[0]%10!=0:
         bas=(0.98*rayonexternecal*cosy,0.98*rayonexternecal*siny)
        else:
         bas=(0.99*rayonexternecal*cosy,0.99*rayonexternecal*siny)
         decal=((280+obj[1])/360*100+99.7)%100
         image.write(texte(str(obj[0]),"graduations",offset=decal))
        image.write(ligne(haut,bas))

    # Placer les étoiles
    for item in etoiles:
        u=item[2]/5*x*cos(angle(item[1]))
        v=item[2]/5*x*sin(angle(item[1]))
        image.write(cercle(u,v,0.003,stroke="\"black\""))
        
        
    
        
    image.write(pied)
    image.close()

def dos(x):
    entete="<svg viewBox=\"0 0 "+str(TAILLE)+" "+str(TAILLE)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    image=open("arriere.svg","w")
    image.write(entete)
   
    #rayon du tropique du Capricorne
    rayoncap=x*tan(angle((90+23.45)/2))
    #Auxiliaire mais inutile a la fin
    image.write(cercle(0,0,rayoncap, id="\"capricorne\""))
    #image.write(cercleinvisible(0,0,rayoncap*1.01,id="\"capricornebis\""))
    image.write(cercleinvisible(0,0,rayoncap*1.02,id="\"capricornebis\""))
    # le centre de la carte
    image.write(cercle(0,0,0.003,stroke="\"black\""))
    # Traçage du calendrier
    # On a besoin des mois pour l'equation du temps
    rayoninternecal=1.06*rayoncap
    rayonexternecal=1.14*rayoncap
    rayoninvisible=1.005*rayoninternecal
    rinv2=0.97*rayonexternecal
    image.write(cercle(0,0,rayoninternecal))
    image.write(cercle(0,0,rayonexternecal))
    image.write(cercleinvisible(0,0,rayoninvisible,id="\"calendar\""))
    image.write(cercleinvisible(0,0,rinv2,id="\"graduations\""))
    # tracé des démarcations entre les mois et des noms des mois
    # TODO : ajuster le centrage du nom des mois en fonction de la longueur du mot
    for i in range(0,12):
        ang=280+debutsmois[i]
        cosy=cos(angle(ang))
        siny=sin(angle(ang))
        haut=(rayonexternecal*cosy,rayonexternecal*siny)
        bas=(rayoninternecal*cosy,rayoninternecal*siny)
        image.write(ligne_large(haut,bas,2))
        if(i!=11):
         center=280+(debutsmois[i]+debutsmois[(i+1)%12])/2
        else :
         center=280+(debutsmois[i]+debutsmois[(i+1)%12]+360)/2
        decal=(center/360*100+99)%100
        image.write(texte(nomsmois[i],"calendar",offset=decal))
        print(nomsmois[i]," ",decal)
    # Graduations quinquennales    
    for obj in calendrier:
        ang=280+obj[1]
        cosy=cos(angle(ang))
        siny=sin(angle(ang))
        haut=(rayonexternecal*cosy,rayonexternecal*siny)
        if obj[0]%10!=0:
         bas=(0.98*rayonexternecal*cosy,0.98*rayonexternecal*siny)
        else:
         bas=(0.99*rayonexternecal*cosy,0.99*rayonexternecal*siny)
         decal=((280+obj[1])/360*100+99.7)%100
         image.write(texte(str(obj[0]),"graduations",offset=decal))
        image.write(ligne_large(haut,bas,2))
   
    # le haricot de l'equation du temps
    valises=equationdutemps(2020)
   
    u=max(valises)
    k=valises.index(u)
    print(k)
    minutes=int(u)//60
    secondes=int(u)%60
        
    if minutes<0:
     minutes=minutes+1
     secondes=60-secondes
    print("Max  ",u," ",minutes," ",secondes)
    v=min(valises)
    k=valises.index(v)
    print(k)
    minutes=int(v)//60
    secondes=int(v)%60
        
    if minutes<0:
     minutes=minutes+1
     secondes=60-secondes
    print("Min  ",v," ",minutes," ",secondes)
    
    epsilon=0.1
    ca=1/(u-v)
    cb=-v*ca+epsilon
    zoom=1.5
    ca=ca/zoom
    cb=cb/zoom
    punkts=[(0,0) for i in range(366)]
    for i in range(366):
     anglex=i/(366.0)*2*pi+(280.0/180*pi)
     punkts[i]=((ca*valises[i]+cb)*cos(anglex),(ca*valises[i]+cb)*sin(anglex))
    # point du premier janvier // verification ok
    #image.write(cercle(punkts[0][0],punkts[0][1],0.003,stroke="\"black\""))
    for i in range(366):
        image.write(ligne_large(punkts[i],punkts[(i+1)%366],2))
    #OK : todo : graduer la reglette qui permet de lire l'equation du temps (l'alidade)

    # Les heures inegales
    B=rayoncap/2
    BB=B*B
    for i in range(5):
        rayon=sqrt(BB+tan(angle(15+i*15))*tan(angle(15+i*15))*BB)
        rond=((0,-rayon),rayon)
        #image.write(cercle(0,-rayon,rayon))
        # Pareil avec le cercle du Capricorne
        t,u=intersection(rond,((0,0),rayoncap))
        X1c=t[0]
        Y1c=t[1]
        X1cp=u[0]
        Y1cp=u[1]
        if i<=2:
         image.write(arc2(u,t,rayon,id="\""+str(i+1)+"\""))
        else: 
         image.write(arc(u,t,rayon,id="\""+str(i+1)+"\""))
    # et le cercle de la sixieme heure
    image.write(cercle(0,-B,B,id="\"0\"",largeur=0.5))
    # et la ligne horizontale
    image.write(ligne((rayoncap,0),(-rayoncap,0)))
    # les graduations
    decalage=[49.8,54,58.2,62.3,66.4,70.7,75,79.1,83.3,87.2,91.2,95.5,99.45]
    for i in range(13):
        image.write(texte(str(i),"capricornebis",offset=decalage[i]))
    # cartouche
    image.write(cartouche(0,-25*x/20.0,"Francesco De Comite Fecit"))
    image.write(cartouche(0,-25*x/20.0+0.04,"Anno MMXXI"))
    image.write(rect_cartouche(-0.24,-25*x/20.0-0.04,114,21,largeur=0.5,rx=8,ry=8))

    # Le carré des ombres
    cote=x
    image.write(ligne((cote,0),(cote,cote)))
    image.write(ligne((0,cote),(cote,cote)))
    image.write(ligne((0,cote),(0,0)))
    image.write(ligne((-cote,0),(-cote,cote)))
    image.write(ligne((0,cote),(-cote,cote)))

    e1=0.014
    cote1=cote-e1
    image.write(ligne((cote1,0),(cote1,cote1)))
    image.write(ligne((0,cote1),(cote1,cote1)))
   
    image.write(ligne((-cote1,0),(-cote1,cote1)))
    image.write(ligne((0,cote1),(-cote1,cote1)))

    e2=0.025
    cote2=cote1-e2
    image.write(ligne((cote2,cote2),(cote2,0)))
    image.write(ligne((cote2*0.992,cote2),(cote2*0.992,0),id="\"verticaldroit\"",stroke="\"none\""))
    image.write(ligne((0,cote2),(cote2,cote2)))
    image.write(ligne((0,cote2*0.992),(cote2*0.992,cote2*0.992),id="\"horizontaldroit\"",stroke="\"none\""))
    image.write(texte("Umbra versa","verticaldroit",offset=25))
    image.write(texte("Umbra recta","horizontaldroit",offset=35))

    image.write(ligne((-cote2,cote2),(-cote2,0)))
    image.write(ligne((-cote2*0.992,0),(-cote2*0.992,cote2),id="\"verticalgauche\"",stroke="\"none\""))
    image.write(ligne((0,cote2),(-cote2,cote2)))
    image.write(ligne((-cote2*0.992,cote2*0.992),(0,cote2*0.992),id="\"horizontalgauche\"",stroke="\"none\""))
    image.write(texte("Umbra versa","verticalgauche",offset=35))
    image.write(texte("Umbra recta","horizontalgauche",offset=35))
     
    e3=0.03
    cote3=cote2-e3
    image.write(ligne((cote3,0),(cote3,cote3)))
    image.write(ligne((0,cote3),(cote3,cote3)))
    image.write(ligne((-cote3,0),(-cote3,cote3)))
    image.write(ligne((0,cote3),(-cote3,cote3)))

    # les intersections des angles avec les verticales de cote et cote1
    int_cote=[0.0 for i in range(13)]
    int_cote1=[0.0 for i in range(13)]
    for i in range(13):
         int_cote[i]=i*cote/12.0
         int_cote1[i]=i*cote1/12.0
         image.write(ligne((cote,int_cote[i]),(cote1,int_cote1[i])))

    rempli=["\"none\"","\"black\""]
    for i in range(12):
         image.write(polygone([(cote,int_cote[i]),(cote1,int_cote1[i]),(cote1,int_cote1[i+1]),(cote,int_cote[i+1])] ,fill=rempli[(i+1)%2],stroke="\"none\""))
         image.write(polygone([(int_cote[i],cote),(int_cote1[i],cote1),(int_cote1[i+1],cote1),(int_cote[i+1],cote)] ,fill=rempli[(i)%2],stroke="\"none\""))
         image.write(polygone([(-cote,int_cote[i]),(-cote1,int_cote1[i]),(-cote1,int_cote1[i+1]),(-cote,int_cote[i+1])] ,fill=rempli[(i+1)%2],stroke="\"none\""))
         image.write(polygone([(-int_cote[i],cote),(-int_cote1[i],cote1),(-int_cote1[i+1],cote1),(-int_cote[i+1],cote)] ,fill=rempli[(i)%2],stroke="\"none\""))


    """
         Un anneau exterieur avec des valeurs 
    """

    #Graduation des angles horaires
    swip=49.7
    minhor=rayoncap*(5.3/4.6)
    image.write(cercle(0,0,minhor))
    image.write(cercleinvisible(0,0,minhor*1.007,id="\"basechiffre\""))
    maxhor=rayoncap*(5.6/4.6)
    print("-->",maxhor)
    # trou de la vis / pour une taille exterieure de 20 cm
    image.write(cercle(0,0,0.02*maxhor,stroke="\"red\""))
    image.write(cercle(0,0,maxhor,stroke="\"red\""))
    # les chiffres de la partie haute
    image.write(texte("0","basechiffre",offset=0.035))
     # Les deux mots 'hauteur' et 'distance zenithale'    
    image.write(texte("Hauteur","basechiffre",offset=61.5))
    image.write(texte("Distance zenithale","basechiffre",offset=85))
    for i in range(10):
       
        chaine=str(10*i)
        if i==0:
            chaine="0"+chaine
        if(i!=4) and (i!=5):
         image.write(texte(chaine,"basechiffre",offset=swip+(i*100)/36))
        if (i!=0)and(i!=4) and (i!=5):
         image.write(texte(chaine,"basechiffre",offset=swip+(i*100)/36+25))
    for i in range(0,180):
         cosy=cos(2*pi*i/360)
         siny=-sin(2*pi*i/360)
         if (i%10==0):
          image.write(ligne_large((cosy*maxhor,siny*maxhor),(cosy*maxhor*0.97,siny*maxhor*0.97),2))
         elif (i%5==0):
          image.write(ligne_large((cosy*maxhor,siny*maxhor),(cosy*(maxhor*0.96),siny*(maxhor*0.96)),2))  
         else:
          image.write(ligne_large((cosy*maxhor,siny*maxhor),(cosy*(maxhor*0.988),siny*(maxhor*0.988)),2))
    image.write(ligne_large((-maxhor,0),(-maxhor*0.97,0),2))
    # les chiffres de la partie basse
    valeurs=["","3","6","9","12","9","6","3","00","3","6","9","12","9","6","3"]
    decal=[0.1 for i in range(len(valeurs))]
    decal[4]=-0.52
    decal[8]=-0.52
    decal[12]=-0.52
    # def arc2(debut,fin,rayon,id="\" \"",largeur=LARGEUR,stroke="\"black\""):
    image.write(arc2((-maxhor*0.993,0),(maxhor*0.993,0),maxhor*0.993,id="\"basic\"",stroke="\"none\""))
    for i in range(48):
         cosy=cos(2*pi*i/96)
         siny=sin(2*pi*i/96)
         image.write(ligne_large((cosy*maxhor,siny*maxhor),(cosy*maxhor*0.97,siny*maxhor*0.97),2))
         if(i%3)==0:
          image.write(texte(valeurs[i//3],"basic",offset=2*(i*100)/96+decal[i//3]))
         
    image.write(pied)
    image.close()

def texttry(x):
    entete="<svg viewBox=\"0 0 "+str(TAILLE)+" "+str(TAILLE)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    image=open("textalongpath.svg","w")
    image.write(entete)
    image.write(cercle(0,0,x,stroke="\"red\"", id="\"sphereceleste\""))
    image.write(texte("equateur","sphereceleste"))
    image.write(pied)
    image.close()


def ostenseur(x):
    # Et maintenant l'ostenseur
    entete="<svg viewBox=\"0 0 "+str(TAILLE)+" "+str(TAILLE)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    image=open("ostenseur.svg","w")
   
    image.write(entete)
    # le centre de la carte
    #image.write(cercle(0,0,0.003,stroke="\"black\""))
    for i in range(12):
         val=10*i-30
         rayon=x*tan(angle((90-val)/2))
        
    radiogougou=0.075
    #image.write(cercle(0,0,radiogougou,stroke="\"black\""))
    image.write(arc2((0,-radiogougou),(radiogougou,0),radiogougou,stroke="\"red\""))
    image.write(ligne((0,-radiogougou),(x*tan(angle((90-(-27))/2)) , -radiogougou),stroke="\"red\""))
    image.write(ligne((radiogougou,0),( x*tan(angle((90-(-33))/2)),0),stroke="\"red\""))
    eps=-0.02
    image.write(ligne((radiogougou,eps),( x*tan(angle((90-(-33))/2)),eps),stroke="\"none\"", id="\"ostenseur\""))
    image.write(ligne((x*tan(angle((90-(-27))/2)),-radiogougou),( x*tan(angle((90-(-33))/2)),0),stroke="\"red\""))
    # les graduations
    afficher=[-20,-10,0,20,40,60]
    decalos=[-1.4,-1.65,-0.8,-1.3,-1.6,-1.8]
    for i in range(22):
         val=5*i-30
         rayon=x*tan(angle((90-val)/2))
         percent=(rayon-radiogougou)/(x*tan(angle((90-(-30))/2)))*100
         print(i," ",val," ",percent)
         if (i%2!=0):
          image.write(ligne((rayon,0),(rayon,-0.015)))
         else:
          image.write(ligne((rayon,0),(rayon,-0.025)))   
         if(val in afficher):
          decal=decalos[afficher.index(val)]
          if (val==0):
           image.write(texte("00","ostenseur",offset=percent+decal))
          else:
           image.write(texte(str(val),"ostenseur",offset=percent+decal))
           
    rayoncap=x*tan(angle((90+23.45)/2)) 
    maxhor=rayoncap*(5.6/4.6)
    # trou de la vis / pour une taille exterieure de 20 cm
    image.write(cercle(0,0,0.02*maxhor,stroke="\"red\""))       
    image.write(pied)
    image.close()
    return # ostenseur

def alidade(x):
    # Et maintenant l'alidade
    entete="<svg viewBox=\"0 0 "+str(TAILLE)+" "+str(TAILLE)+"\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    pied="</svg>\n"
    image=open("alidade.svg","w")
   
    image.write(entete)
    rayoncap=x*tan(angle((90+23.45)/2))
    # le centre de la carte
    image.write(cercle(0,0,0.003,stroke="\"black\""))
    for i in range(12):
         val=10*i-30
         rayon=x*tan(angle((90-val)/2))
        
    radiogougou=0.1
    #image.write(cercle(0,0,radiogougou,stroke="\"black\""))
    image.write(arc((0,-radiogougou),(-radiogougou,0),radiogougou,stroke="\"red\""))
    image.write(arc((0,radiogougou),(radiogougou,0),radiogougou,stroke="\"red\""))
    image.write(ligne((0,-radiogougou),(x*tan(angle((90-(-27))/2)) , -radiogougou),stroke="\"red\""))
    image.write(ligne((radiogougou,0),( x*tan(angle((90-(-33))/2)),0),stroke="\"red\""))
    image.write(ligne((x*tan(angle((90-(-27))/2)),-radiogougou),( x*tan(angle((90-(-33))/2)),0),stroke="\"red\""))

    image.write(ligne((-radiogougou,0),( -x*tan(angle((90-(-33))/2)),0),stroke="\"red\""))
    image.write(ligne((0,radiogougou),(-x*tan(angle((90-(-27))/2)) , radiogougou),stroke="\"red\""))
    image.write(ligne((-x*tan(angle((90-(-27))/2)),radiogougou),(-x*tan(angle((90-(-33))/2)),0),stroke="\"red\""))

   
    """
    Calcul de l'equation du temps pour graduer l'alidade
    """
    valises=equationdutemps(2020)
   
    u=max(valises)
    k=valises.index(u)
    print(k)
    minutes=int(u)//60
    secondes=int(u)%60
        
    if minutes<0:
     minutes=minutes+1
     secondes=60-secondes
    print("Max  ",u," ",minutes," ",secondes)
    v=min(valises)
    k=valises.index(v)
    print(k)
    minutes=int(v)//60
    secondes=int(v)%60
        
    if minutes<0:
     minutes=minutes+1
     secondes=60-secondes
    print("Min  ",v," ",minutes," ",secondes)
    epsilon=0.1
    ca=1/(u-v)
    cb=-v*ca+epsilon
    zoom=1.5
    ca=ca/zoom
    cb=cb/zoom
    #epsy=0.03
    for i in range(-17,16):
     punkt=ca*(i*60)+cb
     if i%5==0:
          epsy=0.03
     else:
          epsy=0.015
     image.write(ligne((punkt,0),(punkt,-epsy))) 
     image.write(ligne((-punkt,0),(-punkt,epsy)))
    valeurs=["-15","-10","-5","0","5","10","15"]
    decal=[3,18,34.5,51,66.74,81,96.26]
    # Deux lignes invisibles pour poser les valeurs des graduations
    weps=0.035
    image.write(ligne((ca*(-17*60)+cb,-weps),( rayoncap,-weps),stroke="\"none\"",id="\"droite\""))
    image.write(ligne((-(ca*(-17*60)+cb),weps),( -rayoncap,weps),stroke="\"none\"",id="\"gauche\""))
    # Deux petites lignes noires pour faire joli
    image.write(ligne((ca*(-17*60)+cb,0),( radiogougou,0),stroke="\"black\""))
    image.write(ligne((-(ca*(-17*60)+cb),0),( -radiogougou,0),stroke="\"black\""))
    # les graduations de l'equation du temps
    for i in range(len(valeurs)):
         image.write(texte(valeurs[i],"droite",offset=decal[i]))
         image.write(texte(valeurs[i],"gauche",offset=decal[i]))
         
    maxhor=rayoncap*(5.6/4.6)
    # trou de la vis / pour une taille exterieure de 20 cm
    image.write(cercle(0,0,0.02*maxhor,stroke="\"red\""))
    image.write(pied)
    image.close()
    return # alidade
     
    

if __name__=="__main__":
   #alidade(R/2)  
   #ostenseur(R/2)
   #dos(R/2)
   tympan(R/2)
   tympanseul(R/2)
   #rete(R/2)
   #texttry(R/2) 
  

    
