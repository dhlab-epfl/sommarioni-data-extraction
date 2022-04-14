#%%
import json
import re
import spacy



import sys
sys.path.append("../../src")
sys.path.append("../../scripts")
sys.path.append("../../scripts/s0_list_of_terms")

from data_filepaths import s0_raw_sommarioni
from data_filepaths import s0_scripts

#from sys import from_sommarioni_to_countedTronqued
#from sys import from_countedTronqued_listByTypes


listDePrenoms = ['Abondio','Abram','Abramo','Adelajde','Agostin',
    'Agostino','Agnese','Alberto',
    'Alessandro','Allessandro',
    'Almorò','Alvise','Ambrogio',
    'Andrea','Andreina','Andriana','Angela','Angelo',
    'Anna','Anselmo','Antonia','Antonio','Apolonio','Ascanio','Aurelio','Baldassare',
    'Bartolomeo','Basilio','Battista','Benedeto','Benedetto',
    'Bernardino','Bernardo','Bertolo','Bertucci','Bertazzi','Bertuzzi','Benizio',
    'Biaggio','Bianca','Bortolameo',
    'Bortolo','Bortolomeo','Bortolomio','Camilla','Camillo',
    'Carlo','Cattarin','Caterina','Catterina','Cecilia','Cesare',
    'Chiara','Contarina','Coriolano','Cornelia','Costantin',
    'Costantino','Cristoforo','Daniel','Daniele','David','Davide',
    'Domenica','Domenico','Elena',
    'Elisabetta','Elisabeta','Elisazio','Ellena',
    'Emanuel','Enrico','Fabio','Faustino',
    'Federico','Federigo','Felice','Ferdinando','Filippo',
    'Flaminio','Fortunato','Francesca',
    'Francesco','Gabriel','Gabriele','Gabriella','Gaetano','Gaspare','Gasparo','Gerolamo',
    'Giacinto','Giacomo','Gio.Batta','Gioachino',
    'Giorgio','Giovanna','Giovanni','GIrolamo','Girolamo','Giulia','Giulio',
    'Giuseppe','Giuiseppe','Giustina','Giustiniana','Giusto','Ignazio','Illustrissimo','Isabella','Laura','Lauro',
    'Lazaro','Laonardo','Leonardo','Leone','Lin','Livio',
    'Lodovica','Lodovico','Loredana',
    'Lorenzo','Luca','Lucca','Lucia','Lugrezia','Luigi',
    'Maddalena','Madalena','Marcello','Marianna','MarcAntonio',
    'Marco','Maria','Mariana','Mario','Marin','Marina','Marino',
    'Margarita','Margherita','Marta','Matteo','Mattio','Michiel',
    'Michele','Michielle','Nicoleto','Niccolò','Nicolò','Onorio','Orsola','Ottaviano','Ottavio',
    'Orazio','Osvaldo','Paolina','Paolo','Pasin','Pasquale','Pasqualino',
    'Paulo','Pietro','Pisana','Polisena','Polissena','Raffaele',
    'Regina','Rinaldo','Rizzardo','Roberto',
    'Rocco','Rosa','Salamone','Salomon','Salomone','Salvador','Samuele','Santo','Sebastian',
    'Sebastiano','Serafina','Silvestro','Simeone','Simon','Simone',
    'Soranzo','Stanislao','Stefano','Steffano','Teodoro',
    'Teresa','Tomaso','Tommaso','Valentin','Valentino','Vettor',
    'Vettore','Vido','Vincenzo','Vita','Vitale','Vittoria',
    'Vittore','Vivante','Zaccaria','Zuanne']
#primo ??? moisè Raffaele(surtout pour l'ange, 2-3 fois prenom) soranzo ?(bcp + souvent nom)
#lin?? Marcello??
#gio batta
#agostin = agostino ? renier bernardin = bernardino (1 seul fois)
#GIrolamo => essayer de réunir avec Girolamo
#attention Santo

#arret à 20
#en faire des sets
listDeFamille = set([
    'Acciajoli','Acerbi','ACQUISTI','Acquisti','Aglina','AGOSTINI', 'ALBEREGNO',
    'Alberghetti','ALBRIZZI','Albrizzi','ALESSANDRI','ALIPRANDI','AMADEI','AMOROSI',
    'ANCILLO','ANCILOTTO','Andrighetti','Andrioli','ANDRIUZZI','ANGARAN','Angaran',
    'ANGELONI','Angeloni','ANSAIZIO','Ansorsio','ANTONELLI','ARMANI','ARMATI','ARME','Aron',
    'ARRIGONI','ARTELLI','Artiga','ASTORI','Astori',
    'ASTORIE','AVANZETTI', 'AVESANI', 'Arrigoni', 'BACANELLO','Bacchi','BACCOLO','Bachi',
    'BADAELI','BADIN', 'BADOER','BADOVER','Bagatella','BAGLIONI','BAGOLIN',
    'BALBI','Balbi','BALDI','Baldi','BALLOTTA','Bana','BARBARIA','BARBARIGO','Barbarigo',
    'BARBARO','Barbaro','BARBERI','BARCELLI','Bardini','BARETINI', 'BARONCELLI','BARONCELLO','Barsella',
    'BASINELLO','Bassaglia','BASSI','BASTON','BATAJA','Bataglia','BATTAGLIA','BEGNIA',
    'Belfi','Bellati','Bellemo','BELLI','Beloto','Beltrame',
    'BELTRAMELLI','BELUVICH','BEMBO','BENEDETTI','Benetti','Benzon','BERABO','BERCO','BERETELLO',
    'BERENGO','BERLENDIS','Berlendis','Berlevi', 'BERNARDI','Bernardi', 'BERNARDO','Bertacina','BERTI','BERTOTTI',
    'BETTINI','Bettini','BIANCARDI','Bianchini','BIANCONI','BIASIUTI','Biasuti',
    'Bigaglia', 'BISCHUCHIA',
    'BISCUCCIA','BISSANO','BOCCHIALI','BOCHI','BOLANI','Bolani','BOLDU',"BOLDU'",'BOLINI',
    'Bolini','BOLLANI','Bollani','Bollini','BOMBA','Bonagrazia','BONE','BONETTI','BONFADINI',
    'BONLINI','BONVECCHIATO','Boraleri','BORGHESALI','BORINA','BORINI','BORIO','BOSIO','BOSSI','BOZZO',
    'BRAGADIN','Brandolina','Braoeti','Braveti','Brazzi','BRESCIANI','BRUSACERAME','BRUNELLO',
    'BULI','BUSETTO','BUSI', 'BUSIDA','Bustasi','Butacalize', 'Bembo', 'Bevilacqua',
    'Bolani','Boloni','Bon','Bontempi','Borina','Bortoli', 'Bragadin','Braider','Branchini',
    'Burati','Busacherin', 'Businello','CABIANCA', 'CABRINI','Cadorin','CAFFARI','Cagliari','CAGNINI',
    'CALBO','CALICHIOPOLI','CALVI','CAMOZZO','CAMPEIS','CANAL','CANALE','CANESTRARI',
    'CANNAL','Cannal','CANSIAN','CANZIANI','CAOTORTA','CAPELLAN', 'CAPELLO',
    'Capello','Capitanachi','CAPRA','Capretta','Capuzzo','Caretti',
    'Caricchiopoli','Caripimi','CARISSIMI','CARLI',
    'CARMINATI','CARRISSIMI','CARTELLI','Carvaglio','CASATTI', 'CASSETTI','CASTELLI','CATTARI',
    'CAVALLARI','CAVALLARO','CAVALLI','CAVOCO','CAZZATI','CENTENARI','CERONI',
    'CESER','CHERUBINI','CHINCHIO','CHINETTI','CHIRIBIRI','CHRICH','CIATTO',
    'CITTELLO','CLEMENTI','CODEMO','COLADARO','COLALTO','COLEDANI','COLETTI','COLLEDANI',
    'COLOMBO','COLONDA','COLOTTI','COMELLO','COMICCIOLI', 'COMINOTTO', 'CONDULMER','CONFURTUNATI',
    'CONOMO','CONTARINI','CONTI', 'CONTINI', 'COOK','COREDANO','CORNELIA', 'CORNER',
    'CORNERA','CORONA','CORRER','COSTANTINI','COTTONI', 'CRIVELARI','CROTTA','Calvi',
    'Capelari', 'Cardazzo', 'Casolo',
    'Catullo', 'Cavallaro', 'Compagnia', 'Contarini', 'Contini','CRUCIS','CURNIS', 'DALASTA', "DALL'ASTA",
    'DALLASTA', 'DANDOLO', 'DARIVA', 'DIEDO', 'DOLFIN', 'DOLZE', 'DRIUZZI', 'DUODO',
    'Diedo', 'Driuzzi', 'Emo', 'FOSCARINI', 'FOSCARINI', 'FRANCESCHI', 'FRANCOVICH',
    'FRANCOVIK', 'Foscari', 'Francesconi', 'GIOVANELLI', 'GIUSTINIAN', 'GRADENIGA',
    'GRADENIGO', 'GRIMANI', 'GRIPUTO', 'GRITTI', 'Gambillo', 'Garganego', 'Gazato',
    'Ghidoni', 'Girardi', 'Giuradelli', 'Grandis', 'Grassi', 'Grimani',
    'Griti', 'Guerra', 'Guidoni', 'LABIA', 'LIPOMANO', 'LISCHIUTA', 'LOREDAN',
    'LUCCATELLI', 'Loschi', 'Lucatello', 'Luzzato', 'MAFFEI', 'MAINARDI',
    'MANOLESSO', 'MARCONI', 'MARINI', 'MARTINENGO', 'MEMO', 'MICHELI', 'MOLIN',
    'MORA', 'MORETTI', 'MOROSINI', 'MOROSINI', 'MOZENIGA', 'Magno', 'Malipiero',
    'Manca', 'Manfrin', 'Marzan', 'Mazzuccato', 'Mensurati', 'Michieli', 'Minelli',
    'Mocenigo', 'Mora', 'Morosini', 'NANI', 'Namias', 'Ottoboni', 'PERAZZO', 'PESARO',
    'PISANI', 'PORTO', 'PRIULI', 'Parenzo', 'Perlasca', 'Pisani', 'Pizzamano', 'Poro',
    'RAZINI', 'RENIER', 'RIGONI', 'RIVA', 'Rampinetti', 'Renier', 'Rezzonico', 'Rizzi',
    'Rotta', 'Rubelli', 'Rucini', 'SALLA', 'SANDI', 'SANTONINI', 'SAVARDINA', 'SAVOLDELLO',
    'SODERINI', 'SOLARI', 'SORANZO', 'SPIGA', 'SPINELLI', 'SUDARINI', 'Sandi', 'Sansoni',
    'Sapella', 'Savaldello', 'Solari', 'Stella', 'Sulam', 'TASCA', 'TODESCHINI', 'Tiepolo',
    'Toderini', 'Todeschini', 'VALARESSO', 'VALIER', 'VENDRAMIN', 'VENIER', 'VISCOVICH',
    'Valvason', 'Vendramin', 'Vitturi', 'Widman', 'ZAMFERMO', 'ZAMPIERI', 'ZANFERMO', 'ZEN',
    'ZENOBIO', 'ZINELLI', 'ZOLIO', 'ZOLIO', 'ZON', 'ZUCCATO', 'Zamparo', 'Zampiceli','Zanchi', 'Zanbelli',
    'Zechinato', 'Zon', 'Zuanne'
    'Castelli','Catani','Cavazza','Ceponi','Cera','Cerotti','Chiaraba','Chichisiola','Chimotto',
    'Chioelolo','Cisi','Ciuran','Civran','Clario','Clementi','Clementi','Coen','PORTO','Porto',
    'Colombo','Combi','Comello','Comina','Contarini','Contarini','Conti','Contin','Cornelio','Corner',
    'Cornioli', 'Correggio','Correr','Corticelli','Cossovik','Costantin','Costantini','Cressini',
    "D'ALEZE","D'Altin",'DABEMI','DALEZE','DAMEZZO','DARDI','DARIGO','DARIN','DATORTA','DELASIA',
    'DELOTTO','DENTE','DEPORTES','DESANDOVIK','DESERPOS','DIAMANTINI','DIEDO','DOLCE',"DONA'",
    'DONADA','DONADONI','DORIA','DOSMO',"DOZERA'",'DUJA','Dabonte','Dalpeder','Danieli','Daponte',
    'Darin','Dario','Dente','Deventura','Diedo','Dipieri','Dolfin'
])
#STURM ? prénom ? n'apparait qu'une fois, Eurasia ?
#pasini ? prenom ?
#fabian maria

"""
'ABIS','ANDREGHETTI','ANGELI','ANSOISSIO','ARMENI','AZAMAR','Albengo','Alberti',
'Avanzi','BALLARINI','BANE','BARBIERI','BASEGGIO','BASEGIO','BATAGLIA','BELLOTO',
'BENZON','BERTANI','BERTEN','BEVILACQUA','BONADEI','BONI','BONTEMPI','BORELLA',
'BORGHETTI','BOTOLI',"BRACHE'",'BRAGATTO','BUTACALIZE','Baroncelli','Battaglia',
'Beltramelli','Berti','Biasiuti','Bonicelli','Borin','Bosio','Bossi','Breda',
'Bulo','CANNONICI','CARESANA','CARETTA','CAROBOLI','CARRARA','CASSINI','CATTANEO',
'CIATO','CICELLI','CIVRAN','COCO','COLUZZI','COMAROLO','COMBI','CORNOLDI','CRIVILIER',
'CRUCIJ','Canal','Caotorta','Carer','Castelli','Celini','Cenagin','Ceriman','Ciatto',
'Cobres','Coledani','Corregio','Curiel','DADA','DAMULA',"DARI'",'DATOSCHI','DAVIDE',
'DEBEI','DELAI',"Dall'Asta",'Damiani','Donadoni','Duce','Duodo','EMO','ERIZO','ERIZZO',
'Erizo','Erizzo','FABRIIS','FABRIS','FALLIER','FARINELLA','FARSETTI','FAVRETTI',
'FEDRIGO','FELTRONI','FERRARI','FERRETTI','FERRI','FILIPPI','FILIPPINI','FILLIPPI',
'FINI','FIOLETTI','FIOLOSSO','FLANGINI','FLORIAN','FOGAROLI','FONDA','FONTANA',
'FONTANELLA','FORATI','FORESTI','FORLICHE','FORMENTELLO','FORTUNATI','FOSCARI',
'FOSCOLO','FOSSATI','FRANCESCONI','FRANCHI','FRANCHINI','FRANCO','FRANGINI',
'FRATTINI','FRUCCO','FUMAGALLI','FURLANETTO','Fabian','Fabris','Fabro','Falier',
'Faoretto','Fassioli','Faustini','Ferrari','Ferri','Ferro','Filetto','Filippo',
'Fini','Florian','Foker','Fontana','Foscarini','Fovel','Fracassetti','Fracassetti',
'Franceschi','Franchini','Franzini','Franzo','Franzoni','Frisan','Furian','GABRIELI',
'GALANTE','GALAZZi','GALINO','GALIUTI','GALLI','GALLINO',"GALLIU'",'GALLO','GAMBELLO',
'GAMBILLO','GARGANEGO','GARLATA','GARLATO','GARZONI','GASPARI','GASPARINI','GASTALDI',
'GAUDIO','GELMA','GENARO','GHEDINI','GHERARDINI','GHERO','GHESI','GHEZI','GIANDOLINI',
'GIANOTTI','GIDONI','GIORDANI','GIOVICH','GIRARDI','GIULI','GIULLI','GIURICH',
'GIUSTINIANI','GOTTONI','GRANDIS','GRAPIGLIA','GRAPUTO','GRASSI','GRIFALCONI','GRIS',
'GROLA','GUARNIERI','GUAZZO','GUELLACASA','GUERINO','GUERRA','GUERRA','GUIZZETI',
'GUIZZETTI','Galante','Galdi','Galizzo','Gambino','Garbin','Garlata','Garzador',
'Gaspari','Gavardini','Gavazzi','Gedin','Gennaro','Gentili','Ghero','Ghezzi',
'Ghislanzoni','Gianzik','Giarca','Giavallin','Gieppi','Giovanelli','Gislanzoni',
'Giupponi','Giustinian','Giustiniani','Gobbi','Gradenigo','Grapini','Gratarol',
'Grava','Greco','GriFalconi','Gripogono','Gritti','Guarinoni','Guarnieri','Guidoti',
'Guizzetti','INSON','IVANOVICH','Indri','LABBIA','LAMBERTI','LANFRANCHI','LANFRITO',
'LANFRITTO','LANTERNA','LANZA','LAVEZARI','LAVEZZI','LEANDRI','LEZZE','LICINI','LIO',
'LODOVICI','LOGIATO','LOMBARDI','LOMBARDO','LONGO','LOREDANO','LORENZON','LORIS',
'LOVISONI','LUCATELLI','LUCATELLO','LUCCATELLO','LUDOVICI','LUGO','LUZZATO','LUZZO',
'Labia','Lanterna','Latacchi','Licini',['Licini','Lioni','Lipamano','Lollo','Longo',
'Loredan','Lovisoni','Lucatelli','Luisello','Luvisello','Luzato','Luzzo','MACARUZZI',
'MADERNI','MAFEI','MAGNO','MAGRO','MAISETTE','MALANOTI','MALANOTTI','MALIPIERO',
'MAMBRIM','MANDER','MANETTA','MANETTI',"MANFRE'","MANFRE'",'MANFREDINI','MANOLEZZO',
'MANTOVANI','MANZOLI','MANZONI','MARCATI','MARCELLA','MARCELLO','MARCELO','MARCHESINI',
'MARCHI','MARCOVIK','MARIN','MARIONI','MARTIN','MARTINELLI','MARTINOLI','MARTINUSSI',
'MARUZZI','MASCAROL','MASTINI','MATTIUZZI','MEDUN','MERLINI','MERLO','MICHIELI',
'MILESI','MINIA','MINIO','MINOTTI','MIPRANDI','MISSANA','MIZZANA','MOCCHI','MOCENIGO',
'MOLARI','MOLINARI','MOLINI','MONDINI',"MONFERA'",'MONICI','MORO','MORONI','MOZENIGO',
'MOZZI','MUSITELLI','MUSOLO','MUZZATO','Macaruzzi','Macer','Maderini','Maderni',
'MaestRizzi','Magrini','Majer','Malimpiero','Malta','Malveti','Manasangue','Manezzi',
'Manin','Manolesso','Manzoni','Maratti','Marcalion','Marchesani','Marchesini',
'Marchetti','Marchi','Marcovik','Marin','Marinello','Marini','Marioni','Marsili',
'Martello','Martinelli','Martini','Maruzzi','Marzello','Marzola','Massa','Mastini',
'Melchiori','Meneguzzi','Mestre','Milik','Milla','Minich','Minotto','Mizzana','Molena',
'Moleti','Moli','Molin','Monti','Morati','Moro','Moroni','Mozenigo','Mozzi','Murer',
'NADALI','NADO','NALON','NANETTI','NARDI','NARDINI','NASOLIN','NEGRELLO','NEGRI',
'NENNI','NICOLI','NINFA','NODOLI','NOSADINI','NOVELLO','Nani','Nani', 'Giuseppe'], ['Negrelli', 'Antonio'], ['Negri', 'Giuseppe'], ['Negri', 'Teresa'], ['Negroni', 'Allessandro'], ['Nerini', 'Nicolò'], ['Nicoli', 'Filippo'], ['Nicoli', 'Vittoria'], ['Nosadini', 'Angelo'], ['Nosadini', 'Leonardo'], ['Novello', 'Antonio'], ['OGLIENI', 'Giovanni'], ['OLIVI', 'Sebastiano'], ['OLIVO', 'Angelo'], ['OLMO', 'Antonio'], ['ORIO', 'Angelo'], ['ORIO', 'Pisana'], ['ORLANDI', 'Paulo'], ['ORTALLI', 'Pietro'], ['Olivi', 'Sebastiano'], ['Olivieri', 'Giuseppe'], ['Olmo', 'Antonio'], ['Olmo', 'Domenico'], ['Olmo', 'Margarita'], ['Omigoni', 'Andrea'], ['Orio', 'Andriana'], ['Orio', 'Marina'], ['Orsoni', 'Francesco'], ['Ottolin', 'Alessandro'], ['PADOVAN', 'Girolamo'], ['PADOVANI', 'Gerolamo'], ['PAGAN', 'Marco'], ['PAGANELLO', 'Giuseppe'], ['PAGANI', 'Antonio'], ['PAGINI', 'Pietro'], ['PANAGIOTTO', 'Paolo'], ['PANEINFORNI', 'Andrea'], ['PANIGAI', 'Bortolameo'], ['PANZIERA', 'Giacomo'], ['PAOLINI', 'Pietro'], ['PAPETTE', 'Antonio'], ['PAPETTE', 'Giovanni'], ['PAPETTE', 'Pasqualino'], ['PASETTE', 'Giovanni'], ['PASOTTI', 'Lorenzo'], ['PASQUALIGO', 'Antonio'], ['PASQUALIGO', 'Benedetto'], ['PASQUALIGO', 'Francesco'], ['PASQUALIGO', 'Giovanni'], ['PASQUALIN', 'Giuseppe'], ['PASSAMANER', 'Giacomo'], ['PASSI', 'Enrico'], ['PASTA', 'Lodovica'], ['PASTORI', 'Lorenzo'], ['PAVAZZA', 'Domenico'], ['PAVOLI', 'Francesco'], ['PAZINI', 'Antonio'], ['PAZZI', 'Enrico'], ['PEDROCCHI', 'Cristoforo'], ['PEDROCCHI', 'Giovanni'], ['PEDROSIN', 'Carlo'], ['PELANDINA', 'Catterina'], ['PENERINI', 'Marco'], ['PERAZOLLO', 'Antonio'], ['PERINI', 'Pietro'], ['PERSEGO', 'Pietro'], ['PERSICO', 'Faustino'], ['PERSICO', 'Pietro'], ['PERUCHIN', 'Giacomo'], ['PETROGALLI', 'Giuseppe'], ['PETROVICH', 'Gasparo'], ['PETROVICH', 'Pietro'], ['PETROVICH', 'Tomaso'], ['PEZZANA', 'Catterina'], ['PEZZATO', 'Domenico'], ['PEZZI', 'Carlo'], ['PEZZOLI', 'Tomaso'], ['PIANELLA', 'Antonio'], ['PIANELLA', 'Giovanna'], ['PIASENTI', 'Andrea'], ['PIATI', 'Marta'], ['PIATTI', 'Sebastiano'], ['PICAZZO', 'Antonio'], ['PICCARDI', 'Maria'], ['PICCIOLI', 'Teresa'], ['PICCOLI', 'Michielle'], ['PISONI', 'Giuseppe'], ['PIZONI', 'Giuseppe'], ['PIZZAMANO', 'Agostino'], ['PIZZORDINI', 'Andrea'], ['PLATEO', 'Gerolamo'], ['POCCOBELLI', 'Francesco'], ['POLESE', 'Giuseppe'], ['POLICE', 'Giuseppe'], ['POLICI', 'Giuseppe'], ['POLISE', 'Giuseppe'], ['POLLI', 'Angela'], ['PONTE', 'Giovanni'], ['PORTA', 'Giovanni'], ['POZZI', 'Enrico'], ['PREMUDA', 'Francesco'], ['PREZZATO', 'Giovanni'], ['PROVEDAN', 'Catterina'], ['PUGNALETTO', 'Antonio'], ['PUGNALIN', 'Giuseppe'], ['PUZZETTI', 'Tomaso'], ['Pace', 'Angelo'], ['Pacifico', 'Abramo'], ['Padovan', 'Francesco'], ['Paganello', 'Filippo'], ['Palazzi', 'Domenico'], ['Palese', 'Giuseppe'], ['Panciera', 'Domenico'], ['Panocchia', 'Maria'], ['Pantanali', 'Domenico'], ['Papafava', 'Andriana'], ['Paseti', 'Antonio'], ['Pasqualigo', 'Giovanni'], ['Peccenini', 'Teresa'], ['Pedrocchi', 'Gaspare'], ['Pedrocchi', 'Giuseppe'], ['Pelegrini', 'Francesco'], ['Perasciuti', 'Giovanni'], ['Perosa', 'Bortolo'], ['Piaja', 'Giacomo'], ['Piatti', 'Sebastian'], ['Pico', 'Giuseppe'], ['Pignola', 'Giacomo'], ['Pilizioli', 'Vincenzo'], ['Pinaffo', 'Pietro'], ['Pinato', 'Pietro'], ['Pizioli', 'Giovanni'], ['Plendini', 'Elena'], ['Polacco', 'Tomaso'], ['Polaco', 'Francesco'], ['Polese', 'Giuseppe'], ['Poli', 'Cristoforo'], ['Poli', 'Margarita'], ['Pora', 'Paolo'], ['Pori', 'Antonio'], ['Pori', 'Lorenzo'], ['Porta', 'Giovanni'], ['Posani', 'Domenico'], ['Potima', 'Giacomo'], ['Pretti', 'Giovanni'], ['Prezzato', 'Giovanni'], ['Priuli', 'Mariana'], ['Priuli', 'Marianna'], ['Priuli', 'Pietro'], ['Pugiato', 'Giovanni'], ['Pugnaletto', 'Antonio'], ['Pupilli', 'Giacomo'], ['QUERINI', 'Alvise'], ['QUERINI', 'Benedetto'], ['QUERINI', 'Giovanni'], ['QUERINI', 'Lauro'], ['QUERINI', 'Luigi'], ['QUERINI', 'Teresa'], ['QUERINI', 'Vincenzo'], ['QUONDANSI', 'Giorgio'], ['Querini', 'Alvise'], ['Querini', 'Andrea'], ['Querini', 'Ellena'], ['RAFFAI', 'Filippo'], ['RASPI', 'Francesco'], ['RASPI', 'Gasparo'], ['REALI', 'Giuseppe'], ['REGIO', 'Antonio'], ['REMONDINI', 'Giuseppe'], ['REMPS', 'Antonio'], ['REZZONICO', 'Abondio'], ['RICCOBONI', 'Antonio'], ['RIGAMONTI', 'Carlo'], ['RIGHI', 'Nicolò'], ['RIGO', 'Giovanni'], ['RIGO', 'Giuseppe'], ['RINALDI', 'Giuseppe'], ['RINALDO', 'Domenico'], ['RISEGATI', 'Antonio'], ['RIZZARDI', 'Giuseppe'], ['RIZZETTI', 'Antonio'], ['RIZZETTI', 'Giacomo'], ['RIZZI', 'Antonio'], ['RIZZI', 'Francesco'], ['RIZZI', 'Pietro'], ['RIZZO', 'Francesco'], ['RIZZO', 'Sebastiano'], ['ROBINI', 'Pietro'], ['ROBUSTELLO', 'Luigi'], ['ROCCHETTA', 'Anna'], ['ROGGIA', 'Francesco'], ['ROSADA', 'Angelo'], ['ROSADA', 'Fortunato'], ['ROSADA', 'Pasquale'], ['ROSSI', 'Antonio'], ['ROSSI', 'Bernardo'], ['ROSSI', 'Enrico'], ['ROSSI', 'Francesco'], ['ROSSI', 'Giovanni'], ['ROSSI', 'Giuseppe'], ['ROSSI', 'Lucia'], ['ROVELLI', 'Domenico'], ['ROVI', 'Catterina'], ['RUBBI', 'Cesare'], ['RUBBI', 'Giacomo'], ['RUBELLI', 'Francesco'], ['RUGGIA', 'Antonio'], ['Raffai', 'Filippo'], ['Ragazzi', 'Giacomo'], ['Rampinelli', 'Domenico'], ['Raspi', 'Giovanni'], ['Raspi', 'Margarita'], ['Ratti', 'Bernardo'], ['Reali', 'Francesco'], ['Reali', 'Giuseppe'], ['Regolise', 'Marco'], ['Ricane', 'Margherita'], ['Rigo', 'Giuseppe'], ['Riscetti', 'Giacomo'], ['Rizzardini', 'Elisabetta'], ['Rizzo', 'Antonia'], ['Rizzo', 'Francesco'], ['Robustello', 'Giusto'], ['Robustello', 'Luigi'], ['Roggia', 'Francesco'], ['Rogia', 'Francesco'], ['Romanello', 'Giorgio'], ['Rombenghi', 'Gabriel'], ['Rosada', 'Angelo'], ['Rossetti', 'Antonio'], ['Rossi', 'Carlo'], ['Rossi', 'Francesco'], ['Rossi', 'Pietro'], ['Rubini', 'Ambrogio'], ['Rumieri', 'Domenico'], ['SACATO', 'Antonio'], ['SADALI', 'Antonio'], ['SAGRAMORA', 'Bernardino'], ['SAGRAMORA', 'Girolamo'], ['SAGRAMORA', 'Giuseppe'], ['SAGREDO', 'Agostino'], ['SAGREDO', 'Angelo'], ['SAGREDO', 'Francesco'], ['SAGREDO', 'Giovanni'], ['SALAROL', 'Giacomo'], ['SALERALI', 'Giacomo'], ['SALVI', 'Luigi'], ['SANFEROMO', 'Girolamo'], ['SANUDO', 'Francesco'], ['SAPELLA', 'Orsola'], ['SARTORI', 'Antonio'], ['SARTORI', 'Domenico'], ['SASSELLO', 'Antonio'], ['SASSO', 'Girolamo'], ['SASSO', 'Giuseppe'], ['SCAGIO', 'Giacomo'], ['SCALABRINI', 'Giovanni'], ['SCALFAROTTO', 'Antonio'], ['SCARELLO', 'Carlo'], ['SCOFFA', 'Giuseppe'], ['SCORELLA', 'Carlo'], ['SCOTTI', 'Lorenzo'], ['SCUDELARI', 'Giuseppe'], ['SCUDELARI', 'Matteo'], ['SEDEA', 'Pasquale'], ['SEGATTI', 'Bernardino'], ['SELICH', 'Vincenzo'], ['SEMITECOLO', 'Alessandro'], ['SEMITECOLO', 'Giovanni'], ['SEORDIGLI', 'Giorgio'], ['SERA', 'Antonio'], ['SERATO', 'Matteo'], ['SERIMAN', 'Maria'], ['SERO', 'Giovanni'], ['SERPE', 'Osvaldo'], ['SERRA', 'Antonio'], ['SIEDEA', 'Pasqualino'], ['SILVESTRINI', 'Pietro'], ['SIMIONATO', 'Domenico'], ['SIRMEN', 'Madalena'], ['SOARDI', 'Domenico'], ['SOPERCHI', 'Francesco'], ['SPIRITO', 'Giuseppe'], ['SPONZA', 'Giovanni'], ['SQUADRONI', 'Pietro'], ['STAE', 'Gabriele'], ['STAVIGNONI', 'Antonia'], ['STECHINI', 'Antonio'], ['STEFFANI', 'Giacomo'], ['STEFFANI', 'Stefano'], ['STELLA', 'Antonio'], ['STELLA', 'Simon'], ['STRATI', 'Giacomo'], ['STRUCA', 'Francesco'], ['SVARIO', 'Francesco'], ['Sabbia', 'Marco'], ['Sacerdote', 'David'], ['Sagramora', 'Domenico'], ['Sagramora', 'Gerolamo'], ['Sagredo', 'Giovanni'], ['Sala', 'Giuseppe'], ['Salaman', 'Alvise'], ['Salci', 'Antonio'], ['Salla', 'Allessandro'], ['Salvadori', 'Antonio'], ['Salvadori', 'Giovanni'], ['Salvini', 'Luigi'], ['Sanchi', 'Giovanna'], ['Sansonio', 'Antonio'], ['Sanzonio', 'Antonio'], ['Saraval', 'Anselmo'], ['Sardi', 'Valentino'], ['Sartori', 'Antonio'], ['Sartori', 'Vincenzo'], ['Scalabrin', 'Pietro'], ['Schiantarello', 'Nicolò'], ['Sedea', 'Pasqualino'], ['Sepora', 'Andrea'], ['Serafini', 'Valentino'], ['Seraval', 'Anselmo'], ['Seriman', 'Giacomo'], ['Seriman', 'Vittoria'], ['Serno', 'Anna'], ['Sesia', 'Domenico'], ['Settimini', 'Giacomo'], ['Settini', 'Pietro'], ['Simoni', 'Niccolò'], ['Sisconi', 'Andrea'], ['Sorari', 'Antonio'], ['Spinelli', 'Domenico'], ['Stai', 'Gabriele'], ['Stefani', 'Giacomo'], ['Steffani', 'Giacomo'], ['Sullam', 'Benedetto'], ['Svario', 'Francesco'], ['TACCO', 'Elisabetta'], ['TAMBELLI', 'Giacomo'], ['TAOLIN', 'Giovanni'], ['TARABOCCHIA', 'Giovanni'], ['TENESCHI', 'Domenico'], ['TERAZZINA', 'Benedetto'], ['TETTAMASI', 'Giuseppe'], ['TIEPOLLO', 'Giovanni'], ['TIEPOLO', 'Almorò'], ['TIEPOLO', 'Alvise'], ['TIEPOLO', 'Nicolò'], ['TIOSSI', 'Giuseppe'], ['TIRINKAN', 'Andrea'], ['TOBIA', 'Giuseppe'], ['TODARINI', 'Alvise'], ['TODARINI', 'Teodoro'], ['TODERINI', 'Alvise'], ['TODERINI', 'Antonio'], ['TODERINI', 'Ferdinando'], ['TODERINI', 'Gaetano'], ['TOGNANA', 'Giovanni'], ['TOLOMEO', 'Bernardo'], ['TOMASINI', 'Angelo'], ['TOMASINI', 'Antonio'], ['TOMASINI', 'Tomaso'], ['TOMMASINI', 'Antonio'], ['TOMMASINI', 'Tommaso'], ['TONCI', 'Catterina'], ['TONETTI', 'Michielle'], ['TONIATO', 'Giovanni'], ['TONINI', 'Francesco'], ['TONON', 'Bortolomeo'], ['TORRACULI', 'Teresa'], ['TREMIGNORI', 'Paulo'], ['TRENTINI', 'Gerolamo'], ['TREVISAN', 'Allessandro'], ['TREVISAN', 'Davide'], ['TREVISAN', 'Domenico'], ['TREVISAN', 'Giacomo'], ['TREVISANI', 'Giacomo'], ['TROMBE', 'Marco'], ['TROMBETA', 'Marco'], ['TRON', 'Nicolò'], ['TRUSIS', 'Regina'], ['TURBIN', 'Francesco'], ['TaManina', 'Contarina'], ['Tabacchi', 'Nicolò'], ['Tabacchi', 'Vincenzo'], ['Tabboga', 'Giuseppe'], ['Tagliapietra', 'Pietro'], ['TamAI', 'Giulio'], ['Tarabocchia', 'Giovanni'], ['Targa', 'Antonio'], ['Tassioli', 'Antonio'], ['Tazzioli', 'Antonio'], ['Terni', 'Marco'], ['Tirabosco', 'Angelo'], ['Tironi', 'Francesco'], ['Tobia', 'Giuseppe'], ['Todesco', 'Giacomo'], ['Toffolutti', 'Giacomo'], ['Tognana', 'Giovanni'], ['Togniana', 'Giovanni'], ['Tomasi', 'Antonio'], ['Tomasini', 'Antonio'], ['Tomasini', 'Tomaso'], ['Ton', 'Angelo'], ['Tonon', 'Giuseppe'], ['Tovanovich', 'Giovanna'], ['Traversi', 'Francesco'], ['Trentin', 'Francesco'], ['Trentini', 'Francesco'], ['Trevisan', 'Alessandro'], ['Trevisan', 'Francesco'], ['Trevisana', 'Paulo'], ['Trevisani', 'Giacomo'], ['Trifoni', 'Leonardo'], ['Tron', 'Vincenzo'], ['Tuschetto', 'Antonio'], ['Usabel', 'Antonio'], ['VACILLI', 'Giorgio'], ['VALENTINI', 'Antonio'], ['VALLIER', 'Gerolamo'], ['VALMARANA', 'Leonardo'], ['VALMARANA', 'Stefano'], ['VARDA', 'Sebastiano'], ['VARISCO', 'Giovanni'], ['VARRINI', 'Chiara'], ['VENDRAMINA', 'Maria'], ['VENDRAMINI', 'Francesco'], ['VENDRAMINI', 'Pietro'], ['VERONA', 'Giovanni'], ['VERONA', 'Niccolò'], ['VERONA', 'Nicolò'], ['VEVRINI', 'Gaetano'], ['VIANELLO', 'Gerolamo'], ['VIANELLO', 'Giuseppe'], ['VIATO', 'Cristoforo'], ['VIDO', 'Giovanni'], ['VIGENTINI', 'Francesco'], ['VIGNOLA', 'Sebastiano'], ['VIOLA', 'Giuseppe'], ['VIRCOVICH', 'Carlo'], ['VISCIUTA', 'Catterina'], ['VISICH', 'Paolo'], ['VISICH', 'Paulo'], ['VISIK', 'Paolo'], ['VISILICH', 'Paulo'], ['VITALI', 'Giovanni'], ['VITALI', 'Margarita'], ['VITALI', 'Pietro'], ['VITTURI', 'Andrea'], ['VIZENTINI', 'Antonio'], ['Valentini', 'Giacomo'], ['Vasilicò', 'Elisabetta'], ['Vecil', 'Domenico'], ['Veludo', 'Giorgio'], ['Venier', 'Angelo'], ['Venier', 'Giovanni'], ['Venier', 'Girolamo'], ['Ventura', 'Giuseppe'], ['Venturali', 'Giuseppe'], ['Verasso', 'Antonio'], ['Verdi', 'Andrea'], ['Vernisi', 'Luigi'], ['Veronese', 'Pietro'], ['Vesci', 'Domenico'], ['Vetturi', 'Giuseppe'], ['Vezzi', 'Antonio'], ['Vianello', 'Gerolamo'], ['Vianni', 'Alessandro'], ['Vidiman', 'Lodovico'], ['Violin', 'Domenico'], ['Violina', 'Domenica'], ['Visentini', 'Antonio'], ['Vitali', 'Pietro'], ['WIDMAN', 'Antonio'], ['WIDMANN', 'Lucia'], ['ZAGARI', 'Marco'], ['ZAGURI', 'Cecilia'], ['ZAGURI', 'Pietro'], ['ZAMBELLI', 'Matteo'], ['ZANI', 'Agnese'], ['ZANIN', 'Francesco'], ['ZANINI', 'Angelo'], ['ZANINI', 'Leonardo'], ['ZANNE', 'Alvise'], ['ZANNE', 'Giorgio'], ['ZANOBRIO', 'Alvise'], ['ZANON', 'Giuseppe'], ['ZAPELLA', 'Orsola'], ['ZAPPELLA', 'Orsola'], ['ZATTI', 'Michele'], ['ZEFIRI', 'Giovanni'], ['ZENARO', 'Agostino'], ['ZENNARO', 'Agostino'], ['ZENOBRIO', 'Alvise'], ['ZIGNO', 'Carlo'], ['ZIGNO', 'Marco'], ['ZIRON', 'Francesco'], ['ZITTI', 'Alvise'], ['ZIUSTO', 'Angelo'], ['ZOCCHI', 'Sebastiano'], ['ZOLA', 'Pietro'], ['ZOPETTI', 'Simone'], ['ZORZI', 'Antonio'], ['ZORZI', 'Francesco'], ['ZORZI', 'Pietro'], ['ZUANICHI', 'Giuseppe'], ['ZUARATA', 'Teresa'], ['ZUCATO', 'Allessandro'], ['ZUSTO', 'Angelo'], ['Zambelli', 'Giacomo'], ['Zambelli', 'Mattio'], ['Zampiceni', 'Bortolomeo'], ['Zampiceni', 'Giacomo'], ['Zampieri', 'Giacomo'], ['Zanchetta', 'Angelo'], ['Zanchini', 'Maddalena'], ['Zane', 'Francesco'], ['Zanetti', 'Gabriele'], ['Zangarofoli', 'Margarita'], ['Zannon', 'Giuseppe'], ['Zanon', 'Giuseppe'], ['Zanuto', 'Giuseppe'], ['Zanutta', 'Maddalena'], ['Zeberlin', 'Giacomo'], ['Zen', 'Alessandro'], ['Zen', 'Antonio'], ['Zen', 'Marco'], ['Zen', 'Pietro'], ['Zino', 'Carlo'], ['Zitti', 'Paolo'], ['Zocchi', 'Domenico'], ['Zorzetto', 'Zuanne'], ['Zuccato', 'Alessandro'], ['Zuliani', 'Maria']

"""




listDeVille = []
listFaconDecrireQuondam = ["quondam",]

# %%


#%%

with open(s0_raw_sommarioni,) as f:
    sommarioni = json.load(f)

countedTronqued = from_sommarioni_to_countedTronqued(sommarioni)
#print(countedTronqued)

# %%
listByType = from_countedTronqued_listByTypes(countedTronqued)

# %%
#Format entrée :

#Juste un nom de famille
ent_nf = [] 
#nom de famille suivi du prénom
ent_nf_pr = []
#deux nom de famille puis un prénom
ent_nf_nf_pr = []
#nom de famille puis deux prénom
ent_nf_pr_pr = []



# %%
#gestion des nom seul
"""
objet personne ? avec : => les envoyer sur json
-nom 1
-nom 2
-prénom 1
-prénom 2
-provenance "di"
-quondam
-sacerdote
-flag le cas (ex nf_pr ou quondam a la fin...)
-boolean : sur à 100% ?
"""

nomProprio1 = []
nomProprio2 = []
nomProprio3 = []
nomProprio4 = []
erediDelFu = []
pasEncoreClasse = []

nomSeul = listByType[0][1]
for i in range(len(nomSeul)):
    decoupe = re.split("\s",nomSeul[i][1])
    taille = len(decoupe)
    if decoupe[taille-1] == '' :
        decoupe.pop()
        taille -= 1
    if taille == 1:
        if decoupe[0] in listDeFamille :
            ent_nf.append((decoupe,nomSeul[i][1]))
            print(nomSeul[i][1])
        else : 
            nomProprio1.append(decoupe)
    elif taille == 2 :
        if (decoupe[0] in listDeFamille) & (decoupe[1] in listDePrenoms):
            ent_nf_pr.append(decoupe)
        elif decoupe[1] in listDePrenoms:
            nomProprio2.append(decoupe) 
        else :
            pasEncoreClasse.append(decoupe)
    elif taille == 3:
        if decoupe[2] in listDePrenoms:
            nomProprio3.append(decoupe)
        #elif (decoupe[1] in listDePrenoms) & (decoupe[2] in ):
        else :
            pasEncoreClasse.append(decoupe)  
    elif taille == 4:
        if ((decoupe[1] in listDePrenoms) & (decoupe[2] == "di")) :
            nomProprio4.append(decoupe)
        else :
            pasEncoreClasse.append(decoupe) 
    else:
           erediDelFu.append(decoupe)
# %%
#stanislao dans eredi??
print(len(nomSeul))
# %%
#gestion des nom avec quondam
nomProprio2_2 = []
nomProprio3_2 = []
nomProprioQuondam = []


nomAvecQuondam = listByType[1][1]
for i in range(len(nomAvecQuondam)):
    decoupe = re.split("\s",nomAvecQuondam[i][1])
    taille = len(decoupe) 
    if taille == 4 :
        print(decoupe)

# %%
#gestion des nom avec famille 
nomAvecFamille = listByType[2][1]
print(nomAvecFamille)

for i in range(len(nomAvecFamille)):
    decoupe = re.split("\s",nomAvecFamille)
    