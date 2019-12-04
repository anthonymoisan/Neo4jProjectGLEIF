import csv
import codecs
import time
import os

#Permet de convertir le fichier XML de niveau 1 en fichier CSV en recuperant uniquement les elements interessants
def ConvertFichierNiveau1(filenameIn, filenameOut):
    
    print("--- Import Fichier de niveau 1 : " + filenameIn + "---")
    startTime=time.time()
    
    
    
    dictCodeLEI = {} 
    dictCodeError = {}

    # supprimer le fichier 
    if os.path.isfile(filenameOut):
        os.remove(filenameOut)
    
    lineToAppend = ""
    insert = False
    # Ouverture des fichiers
    with open(filenameIn, 'r',encoding ='utf-8') as inFile :
        with open(filenameOut, 'w' , encoding ='utf-8') as outFile :
            outFile.write("Code_LEI;Legal_Name;Country_Code;Status_Actif;Last_Update_Date")
            
            for line in inFile:
                
                if "<lei:LEI>" in line:
                    carad = line.find('<lei:LEI>') # carad = caractere de depard
                    caraf = line.find('</lei:LEI>') #caraf = caractere de fin
                    LEI = line[carad+9:caraf] 
                    if (LEI in dictCodeLEI):
                        dictCodeError[LEI] = 1
                        insert = False
                    else:
                        dictCodeLEI[LEI]= 1 #Insertion dans un dictionnaire
                        if(lineToAppend != ""):
                            #Insertion du precedent Code LEI
                            outFile.write(lineToAppend)
                        lineToAppend = (';\n')+LEI + (';')
                        insert = True
                        nbpays = 0
                        #outFile.write( (';\n')+LEI + (';'))  
            
                if (insert):
                    if ("<lei:LegalName" in line):
                        caradd1 = line.find('<lei:LegalName') #+1 => +1 car > Ex: <lei:LegalName>
                        caradd2 = line.find('<lei:LegalName xml:lang=') #+5 => Ex: <lei:LegalName xml:lang="en">
               
                        # si on est sur un cas de balise <lei:LegalName>
                        if caradd2 == -1: #-1 non trouve <lei:LegalName xml:lang='
                            c = caradd1 + 15
                        else :
                            c = caradd2 + 29 #
                            #Fin du if sur le caractere de depart
               
                        caraff = line.find('</lei:LegalName>')
                
                        #Traitement sur la raison sociale car on a observe des guillemets et des ;
                        resu = line[c:caraff].replace(';','')
                        resu = resu.replace('"','')
                        if len(resu) != 0:
                            #outFile.write(resu + (';'))
                            lineToAppend += resu + (';')     
                    
                    if ("<lei:Country" in line):
                        carad = line.find('<lei:Country')
                        caraf = line.find('</lei:Country')
                        nbpays = nbpays + 1
                        # On ne veut afficher que le 1er country pour une entite legale
                        if nbpays == 1:
                            #outFile.write(line[carad+13:caraf] + (";"))
                            lineToAppend += line[carad+13:caraf] + (';')
                    # Fin du if sur pays = 1
                
                    if ("<lei:EntityStatus>" in line):
                        carad = line.find('<lei:EntityStatus')
                        caraf = line.find('</lei:EntityStatus')
                        #outFile.write(line[carad+18:caraf] + (";") )
                        lineToAppend += line[carad+18:caraf] + (";")
            
                    if ("<lei:LastUpdateDate>" in line):
                        carad = line.find('<lei:LastUpdateDate>')
                        #outFile.write(line[carad+20:carad+30] ) # +30 car on prend uniquement les 10first car
                        lineToAppend += line[carad+20:carad+30]
            
    endTime =time.time()
    print("* Nombre de codes LEI importes :" + str(len(dictCodeLEI)))
    print("* Nombre de codes LEI dupliques : " +str(len(dictCodeError)))
    print ("* Temps d'execution = %f" %(endTime-startTime))
    return dictCodeLEI


#Permet de convertir le fichier XML de niveau 2 en fichier CSV en recuperant uniquement les elements interessants
def ConvertFichierNiveau2(filenameIn, filenameOut, dictCodeLEI):
    
    print("--- Import Fichier de niveau 2 : " + filenameIn + "---")
    
    startTime=time.time()
    
    nberreur = 0 
    nbRelation = 0
    conditionValidationLigne = True

    # supprimer le fichier 
    if os.path.isfile(filenameOut):
        os.remove(filenameOut)
    
    # Ouverture des fichiers
    with open(filenameIn, 'r',encoding ='utf-8') as inFile :
        with open(filenameOut, 'w' , encoding ='utf-8') as outFile :
            outFile.write("Start_Node;End_Node;Relation_ShipeType")

            TagLine = 0

            for line in inFile:
        
                # Gestion des Start Node
                if ((TagLine == 1) or (TagLine == 2)) :
                    carad = line.find('<rr:NodeID>') # carad = caractere de depard
                    caraf = line.find('</rr:NodeID>') #caraf = caractere de fin
                    nb = len("<rr:NodeID>")
                    
                    #C'est seulement dans le cas ou il y a un Start Node qu'on fait un saut de ligne (\n)
                    #En revanche dans le cas d'un EndNode on n'en fait pas
                    if TagLine == 1 :
                        conditionValidationLigne = True
                        # Si le codeLEI n'est pas present dans le dictionnaire de code LEI de niveau 1
                        # c'est problematique
                        CodeLEIDepart = line[carad+nb:caraf]
                        if CodeLEIDepart not in dictCodeLEI :
                            nberreur += 1
                            
                    if TagLine ==2 :
                        # Si le codeLEI n'est pas present dans le dictionnaire de code LEI de niveau 1
                        # c'est problematique
                        CodeLEIFin = line[carad+nb:caraf]
                        
                        if CodeLEIFin not in dictCodeLEI :
                            nberreur += 1
                            conditionValidationLigne = False
                            
                        if CodeLEIFin in dictCodeLEI :
                            #outFile.write( ('\n') + CodeLEIDepart + (';')) 
                            #outFile.write(CodeLEIFin + (';'))
                            #inversion pour le parcours
                            outFile.write( ('\n') + CodeLEIFin + (';')) 
                            outFile.write(CodeLEIDepart + (';'))
                            nbRelation += 1
                            
                    
                    TagLine = 0
                              
                if "<rr:StartNode>" in line:
                    TagLine = 1
                         
                if "<rr:EndNode>" in line:
                    TagLine = 2
                
                if (conditionValidationLigne) :
                    if ("<rr:RelationshipType" in line):
                        carad2 = line.find('<rr:RelationshipType')
                        caraf2 = line.find('</rr:RelationshipType')
                        nb2 = len("<rr:RelationshipType>")
                        outFile.write(line[carad2+nb2:caraf2] + (";"))
        
                    if ("<rr:LastUpdateDate>" in line):
                        carad3 = line.find('<rr:LastUpdateDate>')
                        nb3 = len("<rr:LastUpdateDate>")
                        outFile.write(line[carad3+nb3:carad3+nb3+10] + (";"))

    print ("* Nombre de relations importees : ", nbRelation)
    print ("* Nombre d'erreurs dans le fichier de niveau 2 avec des problemes de code LEI : ", nberreur)
    
    
    endTime =time.time()
    print ("* Temps d'execution = %f" %(endTime-startTime))


if __name__== "__main__":
    dictCodeLEI = ConvertFichierNiveau1("../../data/niveau1.xml","../../output/Niveau1.csv")
    ConvertFichierNiveau2("../../data/niveau2.xml","../../output/Niveau2.csv", dictCodeLEI)