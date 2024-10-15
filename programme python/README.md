# Construire un astrolabe
 Le programme

# Si vous n'êtes pas un geek

 *Rendez-vous autour de la ligne 131 du programme, où on fixe la latitude des tympans qu'on veut construire (PHI)
 *Décochez une des latitude prédéfinies. 
 *Les autres fichiers étant fournis et toujours les mêmes, à la fin du programme, décochez les deux appels de fonction *tympan* et/ou tympanseul*
 *Lancez le programme et récupérez les deux nouveaux fichiers SVG *tympanLAT* *tympanLATseul*
 *Ouvrez-les dans Inkscape et modifiez leur échelle.

Vous pouvez aussi reconstruire les fichiers des autres parties de l'astrolabe en décochant les fonctions correspondantes. Attention, reconstruire le rete demande une certaine compétence en Inkscape ou en Illustrator. 

# Si vous êtes un geek

Bon courage pour aller lire le code ! Contactez-moi pour débroussailler. 

Pour créer un tympan pour une nouvelle latitude, il faut définir PHI autour de la ligne 131, puis ajouter une entrée dans chacun des quatre dictionnaires juste en dessous dans le code. 
Ces dictionnaires contiennent les décalages des graduations sur le tympan, qui dépendent de la latitude (voir l'image). On y va un peu à l'intuition et à l'extrapolation. 





Le programme marche sans problème majeur entre 40 et 60 degrés. En dessous de 40, j'ai encore quelques petits problèmes de cercles qui débordent...
