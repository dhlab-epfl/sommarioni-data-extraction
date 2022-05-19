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

#%%
listDePrenoms = ['Abondio','Abram','Abramo','adelaide','Adelajde','Agostin',
    'Agostino','Agnese','Alberto',
    'Alessandro','Allessandro',
    'Almorò','Alvise','alteniero','Ambrogio',
    'Andrea','Andreina','Andriana','andrianna','angeglo','Angela','Angelo',
    'Anna','Anselmo','Antonia','Antonio','Apolonio','apollonio','Ascanio','Aurelio','Baldassare',
    'Bartolomeo','Basilio','Battista','Benedeto','Benedetto','benetto','bernardin',
    'Bernardino','Bernardo','Bertolo','Bertucci','Bertazzi','Bertuzzi','Benizio',
    'Biaggio','Bianca','Bortolameo',
    'Bortolo','bartolameo','Bortolomeo','Bortolomio','bartolamio','Camilla','Camillo',
    'Carlo','Cattarin','Caterina','Catterina','Cecilia','Cesare',
    'Chiara','claudio','Contarina','Coriolano','Cornelia','Costantin',
    'Costantino','cristina','Cristoforo','Daniel','Daniele','David','Davide',
    'Domenica','Domenico','eleonora','Elena',
    'Elisabetta','Elisabeta','Elisazio','Ellena','emanuele',
    'Emanuel','Enrico','fabbio','Fabio','Faustino',
    'Federico','Federigo','Felice','Ferdinando','Filippo',
    'Flaminio','Fortunato','Francesca',
    'Francesco','franco','Gabriel','Gabriele','Gabriella','Gaetano','Gaspare','Gasparo','Gerolamo',
    'Giacinto','Giacomo','Gio.Batta','Gioachino',
    'Giorgio','Giovanna','Giovanni','GIrolamo','Girolamo','Giulia','Giulio',
    'Giuseppe','Giuiseppe','Giustina','Giustiniana','Giusto','Ignazio','Illustrissimo','Isabella','Laura','Lauro',
    'Lazaro','Laonardo','Leonardo','Leone','Lin','Livio',
    'Lodovica','Lodovico','Loredana',
    'Lorenzo','Luca','Lucca','lucio','Lucia','Lugrezia','Luigi',
    'Maddalena','Madalena','marcella','Marcello','Marianna','MarcAntonio','marc\'antonio',
    'Marco','Maria','Mariana','marietta','Mario','Marin','Marina','Marino',
    'Margarita','Margherita','Marta','Matteo','Mattio','Michiel','michiele',
    'Michele','Michielle','morella','natalino','Nicoleto','nicoletto',
    'Niccolò','Nicolò','olivo','Onorio','Orsola','Ottaviano','Ottavio',
    'Orazio','Osvaldo','Paolina','Paolo','Pasin','Pasquale','Pasqualino',
    'Paulo','perina','piero','Pietro','Pisana','Polisena','Polissena','Raffaele',
    'Regina','Rinaldo','Rizzardo','Roberto','Rocco','romana',
    'Rosa','sadia','Salamone','Salomon','Salomone','Salvador','salvatore','Samuele','Santo','Sebastian',
    'Sebastiano','Serafina','Silvestro','Simeone','Simon','Simone',
    'Soranzo','Stanislao','Stefano','Steffano','Teodoro',
    'Teresa','Tomaso','Tommaso','Valentin','Valentino','Vettor',
    'Vettore','Vido','Vincenza','Vincenzo','Vita','Vitale','Vittoria','vitore',
    'Vittore','Vivante','Zaccaria','Zuanne','gianfrancesco',
    'reniero','carolina','demetrio','speridion','spiridion','spiridione','capello',
    'sabbato','leonara','lunardo','lavia','zanchi']
#primo ??? moisè Raffaele(surtout pour l'ange, 2-3 fois prenom) soranzo ?(bcp + souvent nom)
#lin?? Marcello??
#gio batta
#agostin = agostino ? renier bernardin = bernardino (1 seul fois)
#GIrolamo => essayer de réunir avec Girolamo
#attention Santo
listDePrenomsLower = [x.lower() for x in listDePrenoms]
setPrenoms = sorted(set(listDePrenomsLower))






#arret à 20
#en faire des sets
listDeFamille = [
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
    'DALLASTA', 'DANDOLO', 'DARIVA', 'DIEDO', 'DOLFIN','dolfini', 'DOLZE', 'DRIUZZI', 'DUODO',
    'Diedo', 'Driuzzi', 'Emo','FABBRO', 'FOSCARINI', 'FOSCARINI', 'FRANCESCHI', 'FRANCOVICH',
    'FRANCOVIK', 'Foscari', 'Francesconi', 'GIOVANELLI', 'GIUSTINIAN', 'GRADENIGA',
    'GRADENIGO', 'GRIMANI', 'GRIPUTO', 'GRITTI', 'Gambillo', 'Garganego', 'Gazato',
    'Ghidoni', 'Girardi','Girardo', 'Giuradelli', 'Grandis', 'Grassi', 'Grimani',
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
    'ZENOBIO', 'ZINELLI', 'ZOLIO', 'ZOLIO', 'ZON', 'ZUCCATO', 'Zamparo', 'Zampiceli', 'Zanbelli',
    'Zechinato', 'Zon', 'Zuanne'
    'Castelli','Catani','Cavazza','Ceponi','Cera','Cerotti','Chiaraba','Chichisiola','Chimotto',
    'Chioelolo','Cisi','Ciuran','Civran','Clario','Clementi','Clementi','Coen','PORTO','Porto',
    'Colombo','Combi','Comello','Comina','Contarini','Contarini','Conti','Contin','Cornelio','Corner',
    'Cornioli', 'Correggio','Correr','Corticelli','Cossovik','Costantin','Costantini','Cressini',
    "D'ALEZE","D'Altin",'DABEMI','DALEZE','DAMEZZO','DARDI','DARIGO','DARIN','DATORTA','DELASIA',
    'DELOTTO','DENTE','DEPORTES','DESANDOVIK','DESERPOS','DIAMANTINI','DIEDO','DOLCE',"DONA'",
    'DONADA','DONADONI','DORIA','DOSMO',"DOZERA'",'DUJA','Dabonte','Dalpeder','Danieli','Daponte',
    'Darin','Dario','Dente','Deventura','Diedo','Dipieri','Dolfin',
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
    'Labia','Lanterna','Latacchi','Licini','Licini','Lioni','Lipamano','Lollo','Longo',
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
    'NENNI','NICOLI','NINFA','NODOLI','NOSADINI','NOVELLO','Nani','Nani','Negrelli','Negri',
    'Negroni','Nerini','Nicoli','Nosadini','Nosadini','Novello','OGLIENI','OLIVI','OLIVO',
    'OLMO','ORIO','ORLANDI','ORTALLI','Olivi','Olivieri','Olmo','Omigoni','Orio','Orsoni',
    'Ottolin','PADOVAN','PADOVANI','PAGAN','PAGANELLO','PAGANI','PAGINI','PANAGIOTTO',
    'PANEINFORNI','PANIGAI','PANZIERA','PAOLINI','PAPETTE','PASETTE','PASOTTI','PASQUALIGO',
    'PASQUALIN','PASSAMANER','PASSI','PASTA','PASTORI','PAVAZZA','PAVOLI','PAZINI','PAZZI',
    'PEDROCCHI','PEDROCCHI','PEDROSIN','PELANDINA','PENERINI','PERAZOLLO','PERINI','PERSEGO',
    'PERSICO','PERSICO','PERUCHIN','PETROGALLI','PETROVICH','PETROVICH','PEZZANA','PEZZATO',
    'PEZZI','PEZZOLI','PIANELLA','PIASENTI','PIATI','PIATTI','PICAZZO','PICCARDI','PICCIOLI',
    'PICCOLI','PISONI','PIZONI','PIZZAMANO','PIZZORDINI','PLATEO','POCCOBELLI','POLESE',
    'POLICE','POLICI','POLISE','POLLI','PONTE','PORTA','POZZI','PREMUDA','PREZZATO','PROVEDAN',
    'PUGNALETTO','PUGNALIN','PUZZETTI','Pace','Pacifico','Padovan','Paganello','Palazzi',
    'Palese','Panciera','Panocchia','Pantanali','Papafava','Paseti','Pasqualigo','Peccenini',
    'Pedrocchi','Pelegrini','Perasciuti','Perosa','Piaja','Piatti','Pico','Pignola','Pilizioli',
    'Pinaffo','Pinato','Pizioli','Plendini','Polacco','Polaco','Polese','Poli','Pora','Pori',
    'Porta','Posani','Potima','Pretti','Prezzato','Priuli','Pugiato','Pugnaletto','Pupilli',
    'QUERINI','QUONDANSI''Querini','RAFFAI','RASPI','REALI','REGIO','REMONDINI','REMPS',
    'REZZONICO','RICCOBONI','RIGAMONTI','RIGHI','RIGO','RINALDI','RINALDO','RISEGATI','RIZZARDI',
    'RIZZETTI','RIZZI','RIZZO','ROBINI','ROBUSTELLO','ROCCHETTA','ROGGIA','ROSADA','ROSADA',
    'ROSSI','ROVELLI','ROVI','RUBBI','RUBELLI','RUGGIA','Raffai','Ragazzi','Rampinelli','Raspi',
    'Ratti','Reali','Regolise','Ricane','Rigo','Riscetti','Rizzardini','Rizzo','Robustello',
    'Roggia','Rogia','Romanello','Rombenghi','Rosada','Rossetti','Rossi','Rubini','Rumieri',
    'SACATO','SADALI','SAGRAMORA','SAGREDO','SALAROL','SALERALI','SALVI','SANFEROMO','SANUDO',
    'SAPELLA','SARTORI','SASSELLO','SASSO','SCAGIO','SCALABRINI','SCALFAROTTO','SCARELLO',
    'SCOFFA','SCORELLA','SCOTTI','SCUDELARI','SEDEA','SEGATTI','SELICH','SEMITECOLO','SEORDIGLI',
    'SERA','SERATO','SERIMAN','SERO','SERPE','SERRA','SIEDEA','SILVESTRINI','SIMIONATO','SIRMEN',
    'SOARDI','SOPERCHI','SPIRITO','SPONZA','SQUADRONI','STAE','STAVIGNONI','STECHINI','STEFFANI',
    'STELLA','STRATI','STRUCA','SVARIO','Sabbia','Sagramora','Sagredo','Sala','Salaman','Salci',
    'Salla','Salvadori','Salvini','Sanchi','Sansonio','Sanzonio','Saraval','Sardi','Sartori',
    'Scalabrin','Schiantarello','Sedea','Sepora','Serafini','Seraval','Seriman','Seriman','Serno',
    'Sesia','Settimini','Settini','Simoni','Sisconi','Sorari','Spinelli','Stai','Stefani','Steffani',
    'Sullam','Svario','TACCO','TAMBELLI','TAOLIN','TARABOCCHIA','TENESCHI','TERAZZINA','TETTAMASI',
    'TIEPOLLO','TIEPOLO','TIOSSI','TIRINKAN','TOBIA','TODARINI','TODERINI','TOGNANA','TOLOMEO',
    'TOMASINI','TOMMASINI','TONCI','TONETTI','TONIATO','TONINI','TONON','TORRACULI','TREMIGNORI',
    'TRENTINI','TREVISAN','TREVISANI','TROMBE','TROMBETA','TRON','TRUSIS','TURBIN','TaManina',
    'Tabacchi','Tabboga','Tagliapietra','TamAI','Tarabocchia','Targa','Tassioli','Tazzioli','Terni',
    'Tirabosco','Tironi','Tobia','Todesco','Toffolutti','Tognana','Togniana','Tomasi','Tomasini',
    'Ton','Tonon','Tovanovich','Traversi','Trentin','Trentini','Trevisan','Trevisan','Trevisana',
    'Trevisani','Trifoni','Tron','Tuschetto','Usabel','VACILLI','VALENTINI','VALLIER','VALMARANA',
    'VALMARANA','VARDA','VARISCO','VARRINI','VENDRAMINA','VENDRAMINI','VERONA','VEVRINI','VIANELLO',
    'VIANELLO','VIATO','VIDO','VIGENTINI','VIGNOLA','VIOLA','VIRCOVICH','VISCIUTA','VISICH','VISICH',
    'VISIK','VISILICH','VITALI','VITTURI','VIZENTINI','Valentini','Vasilicò','Vecil','Veludo','Venier',
    'Ventura','Venturali','Verasso','Verdi','Vernisi','Veronese','Vesci','Vetturi','Vezzi','Vianello',
    'Vianni','Vidiman','Violin','Violina','Visentini','Vitali','WIDMAN','WIDMANN','ZAGARI','ZAGURI',
    'ZAMBELLI','ZANI','ZANIN','ZANINI','ZANNE','ZANOBRIO','ZANON','ZAPELLA','ZAPPELLA','ZATTI','ZEFIRI',
    'ZENARO','ZENNARO','ZENOBRIO','ZIGNO','ZIGNO','ZIRON','ZITTI','ZIUSTO','ZOCCHI','ZOLA','ZOPETTI',
    'ZORZI','ZUANICHI','ZUARATA','ZUCATO','ZUSTO','Zambelli','Zampiceni','Zampiceni','Zampieri',
    'Zanchetta','Zanchini','Zane','Zanetti','Zangarofoli','Zannon','Zanon','Zanuto','Zanutta','Zeberlin',
    'Zen','Zino','Zitti','Zocchi','Zorzetto','Zuccato','Zuliani','QUONDANSI','Querini','condolmer',
    'trieste','farelli','mosini','morosini','barbon','bondoner','bonali',
    'lucchesi','caliari','kromer','gradenigo','fantinelli','zoccolo','stecchini',
    'toffetti','leccini','bonagli','rugeri','filosi','concina','corniani','bovicini',
    'testa','accerboni','pasco','sabioni','lino','giupponi','agazzi','lazzari','malipiero'
    'monticano','piccoli','grimani','pepoli','baldovini','veronesi','giupponi',
    'gritti','foscarini','vacilli','lio','mastini','berengo','belloto',
    'molini','galino','minio','gallino','rinaldo','pagini','magro','caroboli',
    'grifalconi','ancillo','crucij','lio','pisani','venier','guerra','priuli',
    'nani','zaguri','fontanella','steffani','fanelli','bravo','manini','malipiero',
    'vanentgardenn','benzoni','turchetto','riva','miani','giovannelli','grotto','peruli'
    'giuponni','monticano','fisser','gambiosi','marzolo','carminati','terracina','angaran',
    'zustinian','giustinian','recanati','pisana','longo','minelli','rota','mocchi',
    'corner','moroni','fanelli','pussi','brini','lazari','zanenghi','iacour','tassis',
    'formenti','tasca','bao','sulan','fonte','bardese','pinton','fagioto','livan','faliva',
    'fortunio','mazzochi','lio','trevano','pazienti','giviani','zorzi','saloon','pinoli',
    'girardini','bragadini','sopai','rocchi','acerboni','lionello','vanesta','gardinali',
    'savi','sossai','asprea','alcaini','grimani','bertignazza','gasparoni','cavenago',
    'gramolin','gagio','stiore','ponga','tronconi','asprea','penso','degna',
    'volpi','pellegrini','capellis','bordini','cussetti','alghisi','grotta','cremona',
    'ambrosi','fazandella','tanxik','ragasin','lavezzari','capparocca','grollo','luzziato',
    'demezzo','lion','gavazza','dosi','sanudo','monteso','sorzetto','sangian','ranier',
    'widiman','lardoni','zalvani','rede','basadonna','settemini','marangoni','pisella',
    'vituri','savioni','pivoli','versori','pele','trovisan','lambranzi','vivante','leoni',
    'azzoni','calliari','pedretti','modon','gasparotti','rossini','donati','orsato',
    'dabala\'','pelizioli','padoan','fossa','fidati','battagia','deputez','gheltof',
    'dondiorologio','michielli','tranquillo','bagozzi','macacari','bonvicini','paolucci',
    'paulucci','bentivoglio','saler','maffetti'
    ]


    
listDeFamilleLower = [x.lower() for x in listDeFamille]
setFamille = sorted(set(listDeFamilleLower))

# %%
print('giusto' in setFamille)
print('vitore' in setPrenoms)
#print(setPrenoms)


# %%
print(setFamille)
#STURM ? prénom ? n'apparait qu'une fois, Eurasia ?
#pasini ? prenom ?
#fabian maria

# %% 
listdeTitre = ['commisaria','sacerdote','primo']
listDeTitreLower = [x.lower() for x in listdeTitre]
setTitre = sorted(set(listDeTitreLower))

#%%
listdeMembre = ['fratelli','fratello','nipote','nipoti','sorelle','eredi','consorti','vedova','famiglia']
listDeMembreLower = [x.lower() for x in listdeMembre]
setMembre = sorted(set(listDeMembreLower))

listDeVille = []
listFaconDecrireQuondam = ['quondam','q.','q.m.','q.m']
setQuondam = sorted(set(listFaconDecrireQuondam))

# %%


#%%

with open(s0_raw_sommarioni,) as f:
    sommarioni = json.load(f)

countedTronqued_plusNumber = from_sommarioni_to_Tronqued_plus_parcelNumber(sommarioni)
#print(countedTronqued_plusNumber)
#countedTronqued = from_sommarioni_to_countedTronqued(sommarioni)
#print(countedTronqued)

# %%
listByType_plusNumber = from_countedplusnumber_to_listBytype(countedTronqued_plusNumber)
#print(listByType_plusNumber)
#listByType = from_countedTronqued_listByTypes(countedTronqued)

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
#Differentes classes de proprietaires

#une personne simple
class Personne:
    def __init__(self,nm1,pr1=None,pr2=None,nm2=None,di=None,mf=None,titre=None,
            ps=None,pq=None,pf=None,pa = None,pi=None,isqd=False):
        self.prenom1 = pr1
        self.prenom2 = pr2
        
        self.nom1 = nm1
        self.nom2 = nm2
        self.membreFamille = mf
        self.di = di
        self.titre = titre

        self.parcSeul = ps
        self.parcQuond = pq
        self.parcFamille = pf
        self.parcAutre = pa
        self.parIndivi = pi

        self.isAquondam = isqd
        self.lien = []

    def __eq__(self, other):
        self.prenom1 == other.prenom1
        self.prenom2 == other.prenom2
        self.nom1 == other.nom1
        self.nom2 == other.nom2
        self.di == other.di
        self.isAquondam == other.isAquondam

    def __str__(self):
        return 'Nom : ' + self.nom1 + ' Prenom : ' + self.prenom1

    def get_all_parcelles():
        pass

#eglise 
class Chiesa:
    def __init__(self,nom,parcelles,entite=None):
        self.nom = nom
        self.parcelles = parcelles
        self.entite = entite
        self.lien = []

#pretre qui a un benefizio/goduto
class Pretre:
    def __init__(self,nom,parcelles):
        self.nom = nom
        self.parcelles = parcelles
        self.lien = []

def ajouterLien(persA, persB, typeDeLien):
        persA.lien.append((persB, typeDeLien))
        persB.lien.append((persA, typeDeLien))

class Public:
    def __init__(self,nom,parcelles):
        self.nom = nom
        self.parcelles = parcelles

class Parcelle:
    def __init__(self,number, owner):
        self.number = number
        self.owner = owner

def memepersonne(persA, persB):
    return persA.prenom1==persB.prenom1


# %%
#gestion des nom seul
nomSeul = listByType_plusNumber[0][1]

listdePersonne = []
listdeParcelle = []

nomProprio1 = []
nomProprio2 = []
nomProprio3 = []
nomProprio4 = []
erediDelFu = []
pasEncoreClasse = []
nbParcNonClass = 0

#parcours tous les noms seul
for i in range(len(nomSeul)):
    decoupe = re.split("\s",nomSeul[i][0].lower())
    #print(decoupe)
    taille = len(decoupe)
    parcelles = nomSeul[i][1]
    if decoupe[taille-1] == '' :
        decoupe.pop()
        taille -= 1
    if taille == 1:
        #nom de famille
        if decoupe[0] in setFamille:
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0], ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne)) 
        else : 
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    elif taille == 2 :
        #nom-prenom
        if ((decoupe[0] in setFamille) & (decoupe[1] in setPrenoms)):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],decoupe[1],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-membre
        elif ((decoupe[0] in setFamille) & (decoupe[1] in setMembre)):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],mf=decoupe[1],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-titre
        elif ((decoupe[0] in setFamille) & (decoupe[1] in setTitre)):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],titre=decoupe[1],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-nom
        elif ((decoupe[0] in setFamille) & (decoupe[1] in setFamille)):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],nm2=decoupe[1],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        else :
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    elif taille == 3:
        #nom-prenom-prenom
        if (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms) & (decoupe[2] in setPrenoms):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],decoupe[1],decoupe[2],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-nom-prenom
        elif (decoupe[0] in setFamille) & (decoupe[1] in setFamille) & (decoupe[2] in setPrenoms):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],decoupe[2],nm2=decoupe[1],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-prenom-membre
        elif (decoupe[0] in setFamille) & (decoupe[1] in setFamille) & (decoupe[2] in setMembre):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],nm2=decoupe[1],mf=decoupe[2],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-membre-quondam
        elif (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms)&(decoupe[2]=='quondam'):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],decoupe[1],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-membre-indivisi
        elif (decoupe[0] in setFamille) & (decoupe[1] in setMembre)&(decoupe[2]=='indivisi'):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],mf=decoupe[1],ps=parcelles,pi=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))        
        #nom-titre-prenom
        elif (decoupe[0] in setFamille) & (decoupe[1] in setTitre) & (decoupe[2] in setPrenoms):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],decoupe[2],titre=decoupe[1],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-prenom-titre
        elif (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms) & (decoupe[2] in setTitre):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],decoupe[1],titre=decoupe[2],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))  
        else:
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    elif taille == 4:
        #Nom-membre(lien)-di-prenom
        if (decoupe[0] in setFamille) & (decoupe[1] in setMembre) &(decoupe[2] == "di") & (decoupe[3] in setPrenoms):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],decoupe[3],mf=decoupe[1],pq=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-prenom-di-...
        elif (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms) &(decoupe[2] == "di"):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],decoupe[1],di=decoupe[3],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-membre(lien)-di-...
        elif (decoupe[0] in setFamille) & (decoupe[1] in setMembre) &(decoupe[2] == "di"):
            parcelles = nomSeul[i][1]
            personne = Personne(decoupe[0],mf=decoupe[1],di=decoupe[3],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        else:
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    else:
           erediDelFu.append(decoupe)
           pasEncoreClasse.append(decoupe)
           nbParcNonClass += len(parcelles)
# %%
print('entrées classées ',len(listdePersonne))
print('non classées ',len(pasEncoreClasse))
print('total ',len(nomSeul))
print('parcelles classée ',len(listdeParcelle))
print('parcelles non classé ',nbParcNonClass)

#%%
print(erediDelFu)

#%%
print(pasEncoreClasse)

#%%
#test classe
print('ranier' in setFamille)
# %%
#gestion des nom avec quondam
listdePersonne = []
listdeParcelle = []

nomProprio1 = []
nomProprio2 = []
nomProprio3 = []
nomProprio4 = []
erediDelFu = []
pasEncoreClasse = []
nbParcNonClass = 0

nomAvecQuondam = listByType_plusNumber[1][1]

#parcours tout les noms avec quondam
for i in range(len(nomAvecQuondam)):
    decoupe = re.split("\s",nomAvecQuondam[i][0].lower())
    taille = len(decoupe)
    parcelles = nomAvecQuondam[i][1]
    #si termine par quondam, meme cas que nom seul
    if (decoupe[taille-1]in setQuondam):
        taille -= 1
        if taille == 1:
        #nom de famille
            if decoupe[0] in setFamille:
                parcelles = nomAvecQuondam[i][1]
                personne = Personne(decoupe[0], ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne)) 
            else : 
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 2 :
            #nom-prenom
            if (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms):
                parcelles = nomAvecQuondam[i][1]
                personne = Personne(decoupe[0],decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))
            #nom-membre
            elif (decoupe[0] in setFamille) & (decoupe[1] in setMembre):
                parcelles = nomAvecQuondam[i][1]
                personne = Personne(decoupe[0],mf=decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))
            else :
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 3:
            #nom-prenom-prenom
            if (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms) & (decoupe[2] in setPrenoms):
                parcelles = nomAvecQuondam[i][1]
                personne = Personne(decoupe[0],decoupe[1],decoupe[2],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))
            #nom-nom-prenom
            elif (decoupe[0] in setFamille) & (decoupe[1] in setFamille) & (decoupe[2] in setPrenoms):
                parcelles = nomAvecQuondam[i][1]
                personne = Personne(decoupe[0],decoupe[2],nm2=decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))
            #nom-prenom-membre
            elif (decoupe[0] in setFamille) & (decoupe[1] in setFamille) & (decoupe[2] in setMembre):
                parcelles = nomAvecQuondam[i][1]
                personne = Personne(decoupe[0],nm2=decoupe[1],mf=decoupe[2],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))
            #nom-titre-prenom
            elif (decoupe[0] in setFamille) & (decoupe[1] in setTitre) & (decoupe[2] in setPrenoms):
                parcelles = nomAvecQuondam[i][1]
                personne = Personne(decoupe[0],decoupe[2],titre=decoupe[1],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))
            #nom-prenom-titre
            elif (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms) & (decoupe[2] in setTitre):
                parcelles = nomAvecQuondam[i][1]
                personne = Personne(decoupe[0],decoupe[1],titre=decoupe[2],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))  
            else:
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
        elif taille == 4:
            #Nom-membre(lien)-di-prenom
            if (decoupe[0] in setFamille) & (decoupe[1] in setMembre) &(decoupe[2] == "di") & (decoupe[3] in setPrenoms):
                parcelles = nomSeul[i][1]
                personne = Personne(decoupe[0],decoupe[3],mf=decoupe[1],pq=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))
                print("lol")
            #nom-prenom-di-...
            elif (decoupe[0] in setFamille) & (decoupe[1] in setPrenoms) &(decoupe[2] == "di"):
                parcelles = nomSeul[i][1]
                personne = Personne(decoupe[0],decoupe[1],di=decoupe[3],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))
            #nom-membre(lien)-di-...
            elif (decoupe[0] in setFamille) & (decoupe[1] in setMembre) &(decoupe[2] == "di"):
                parcelles = nomSeul[i][1]
                personne = Personne(decoupe[0],mf=decoupe[1],di=decoupe[3],ps=parcelles)
                listdePersonne.append(personne)
                for par in parcelles:
                    listdeParcelle.append(Parcelle(par, personne))
            else :
                pasEncoreClasse.append(decoupe)
                nbParcNonClass += len(parcelles)
    elif taille == 4:
        #nom-prenom-quondam-prenom
        if (decoupe[0] in setFamille)&(decoupe[1]in setPrenoms)&(decoupe[2]in setQuondam)&(decoupe[3]in setPrenoms):
            parcelles = nomAvecQuondam[i][1]
            personneA = Personne(decoupe[0],decoupe[1],pq=parcelles)
            personneB = Personne(decoupe[0],decoupe[3],isqd=True)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personneA))
            ajouterLien(personneA,personneB,'quondam')
        #nom-membre(lien)-quondam-prenom
        elif (decoupe[0] in setFamille)&(decoupe[1]in setMembre)&(decoupe[2]in setQuondam)&(decoupe[3]in setPrenoms):
            parcelles = nomAvecQuondam[i][1]
            personneA = Personne(decoupe[0],mf=decoupe[1],pq=parcelles)
            personneB = Personne(decoupe[0],decoupe[3],isqd=True)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personneA))
            ajouterLien(personneA,personneB,'quondam')
        #nom
        elif (decoupe[0] in setFamille)&(decoupe[1]in setMembre)&(decoupe[2]in setQuondam)&(decoupe[3]in setPrenoms):
            parcelles = nomAvecQuondam[i][1]
            personneA = Personne(decoupe[0],mf=decoupe[1],pq=parcelles)
            personneB = Personne(decoupe[0],decoupe[3],isqd=True)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personneA))
            ajouterLien(personneA,personneB,'quondam')
        else: 
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    elif taille == 5:
        #nom-prenom-prenom-quondam-prenom
        if (decoupe[0] in setFamille)&(decoupe[1]in setPrenoms)&(decoupe[2]in setPrenoms)&(decoupe[3]in setQuondam)&(decoupe[4]in setPrenoms):
            parcelles = nomAvecQuondam[i][1]
            personneA = Personne(decoupe[0],decoupe[1],pr2=decoupe[2],pq=parcelles)
            personneB = Personne(decoupe[0],decoupe[4],isqd=True)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personneA))
            ajouterLien(personneA,personneB,'quondam')
        #nom-titre-prenom-quondam-prenom
        elif (decoupe[0] in setFamille)&(decoupe[1]in setTitre)&(decoupe[2]in setPrenoms)&(decoupe[3]in setQuondam)&(decoupe[4]in setPrenoms):
            parcelles = nomAvecQuondam[i][1]
            personneA = Personne(decoupe[0],titre=decoupe[1],pr1=decoupe[2],pq=parcelles)
            personneB = Personne(decoupe[0],decoupe[4],isqd=True)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personneA))
            ajouterLien(personneA,personneB,'quondam')
        #nom-prenom-quondam-prenom-prenom
        elif (decoupe[0] in setFamille)&(decoupe[1]in setPrenoms)&(decoupe[2]in setQuondam)&(decoupe[3]in setPrenoms)&(decoupe[4]in setPrenoms):
            parcelles = nomAvecQuondam[i][1]
            personneA = Personne(decoupe[0],decoupe[1],pq=parcelles)
            personneB = Personne(decoupe[0],decoupe[3],decoupe[4],isqd=True)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personneA))
            ajouterLien(personneA,personneB,'quondam')    
        else: 
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    else : 
        pasEncoreClasse.append(decoupe)
        nbParcNonClass += len(parcelles)

#%%
print('entrées classées ',len(listdePersonne))
print('non classées ',len(pasEncoreClasse))
print('total ',len(nomAvecQuondam))
print('parcelles classée ',len(listdeParcelle))
print('parcelles non classé ',nbParcNonClass)  
#%%
print(pasEncoreClasse)



#%%
#gestion des nom avec membre de la famille
listdePersonne = []
listdeParcelle = []

nomProprio1 = []
nomProprio2 = []
nomProprio3 = []
nomProprio4 = []
erediDelFu = []
pasEncoreClasse = []
nbParcNonClass = 0

nomAvecFamille = listByType_plusNumber[2][1]
#parcours tous les noms avec famille
for i in range(len(nomAvecFamille)):
    decoupe = re.split("\s",nomAvecFamille[i][0].lower())
    taille = len(decoupe)
    parcelles= nomAvecFamille[i][1]
    if taille == 4:
        #nom-prenom-e-membre(lien)
        if ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3]in setMembre)):
            personne = Personne(decoupe[0],decoupe[1],mf=decoupe[3],ps=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-prenom-e-prenom
        elif ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3] in setPrenoms)):
            personneA= Personne(decoupe[0],decoupe[1],pf=parcelles)
            personneB= Personne(decoupe[0],decoupe[3],pf=parcelles)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, [personneA,personneB]))
            ajouterLien(personneA,personneB,'fratello')
        else: 
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)   
    elif taille == 5:
        #nom-prenom-e-prenom-membre
        if ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3] in setPrenoms)&(decoupe[4]in setMembre)):
            personneA= Personne(decoupe[0],decoupe[1],pf=parcelles)
            personneB= Personne(decoupe[0],decoupe[3],pf=parcelles)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, [personneA,personneB]))
            ajouterLien(personneA,personneB,decoupe[4])
        #nom-prenom-e-membre(lien)-indivisi
        elif ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3]in setMembre)&(decoupe[4]=='indivisi')):
            personne = Personne(decoupe[0],decoupe[1],mf=decoupe[3],ps=parcelles, pi=parcelles)
            listdePersonne.append(personne)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
        #nom-prenom-e-prenom-indivisi
        elif ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3] in setPrenoms)&(decoupe[4]=='indivisi')):
            personneA= Personne(decoupe[0],decoupe[1],pf=parcelles,pi=parcelles)
            personneB= Personne(decoupe[0],decoupe[3],pf=parcelles,pi=parcelles)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, [personneA,personneB]))
            ajouterLien(personneA,personneB,'fratello')
        else: 
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    elif taille == 6:
        #nom-prenom-e-membre(lien)-quondam-prenom
        if ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3]in setMembre)&(decoupe[4] in setQuondam)&(decoupe[5] in setPrenoms)):
            personneA = Personne(decoupe[0],decoupe[1],mf=decoupe[3],pq=parcelles)
            personneB = Personne(decoupe[0],decoupe[5], isqd=True)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
            ajouterLien(personneA,personneB,'quondam')
        #nom-prenom-e-prenom-quondam-prenom
        elif ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3] in setPrenoms)&(decoupe[4]in setQuondam)&(decoupe[5]in setPrenoms)):
            personneA = Personne(decoupe[0],decoupe[1],pq=parcelles,pf=parcelles)
            personneB = Personne(decoupe[0],decoupe[3],pq=parcelles,pf=parcelles)
            personneC = Personne(decoupe[0],decoupe[5],isqd=True)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
            ajouterLien(personneA,personneB,'fratello')
            ajouterLien(personneA,personneC,'quondam')
            ajouterLien(personneB,personneC,'quondam')
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            listdePersonne.append(personneC)
        #nom-prenom-e-prenom-membre(lien)-indivisi
        elif ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3] in setPrenoms)&(decoupe[4]in setMembre)&(decoupe[5]=='indivisi')):
            personneA= Personne(decoupe[0],decoupe[1],pf=parcelles,pi=parcelles)
            personneB= Personne(decoupe[0],decoupe[3],pf=parcelles,pi=parcelles)
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, [personneA,personneB]))
            ajouterLien(personneA,personneB,decoupe[4])
        else: 
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    elif taille == 7:
        #nom-prenom-e-prenom-membre(lien)-quondam-prenom
        if ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3] in setPrenoms)&(decoupe[4]in setMembre)&(decoupe[5]in setQuondam)&(decoupe[6]in setPrenoms)):
            personneA = Personne(decoupe[0],decoupe[1],pq=parcelles,pf=parcelles)
            personneB = Personne(decoupe[0],decoupe[3],pq=parcelles,pf=parcelles)
            personneC = Personne(decoupe[0],decoupe[6],isqd=True)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
            ajouterLien(personneA,personneB,decoupe[4])
            ajouterLien(personneA,personneC,'quondam')
            ajouterLien(personneB,personneC,'quondam')
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            listdePersonne.append(personneC)
        #nom-prenom-e-prenom-quondam-prenom-prenom
        elif ((decoupe[0] in setFamille)&(decoupe[1] in setPrenoms)&((decoupe[2]=='e')|(decoupe[2]=='ed'))
                &(decoupe[3] in setPrenoms)&(decoupe[4]in setQuondam)&(decoupe[5]in setPrenoms)&(decoupe[6]in setPrenoms)):
            personneA = Personne(decoupe[0],decoupe[1],pq=parcelles,pf=parcelles)
            personneB = Personne(decoupe[0],decoupe[3],pq=parcelles,pf=parcelles)
            personneC = Personne(decoupe[0],decoupe[5],pr2=decoupe[6],isqd=True)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, personne))
            ajouterLien(personneA,personneB,'fratello')
            ajouterLien(personneA,personneC,'quondam')
            ajouterLien(personneB,personneC,'quondam')
            listdePersonne.append(personneA)
            listdePersonne.append(personneB)
            listdePersonne.append(personneC)
        else: 
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    else:
        pasEncoreClasse.append(decoupe)
        nbParcNonClass += len(parcelles)
    
# %%
print('entrées classées ',len(listdePersonne))
print('non classées ',len(pasEncoreClasse))
print('total ',len(nomAvecFamille))
print('parcelles classée ',len(listdeParcelle))
print('parcelles non classé ',nbParcNonClass) 
#%%
print(pasEncoreClasse)
    

# %%
#gestion des eglises
listdEglises = []
listdeParcelle = []
listdePretres = []
pasEncoreClasse = []

nomEglise = listByType_plusNumber[3][1]
#parcours tous les noms avec une eglise
for i in range(len(nomEglise)):
    a=1

#%%
print(nomEglise)
# %%
#gestion des prop. public 
listPublic = []
listdeParcelle = []
pasEncoreClasse = []
pasEncoreClasseParcelle = []
nbParcNonClass = 0

nomVenezia = listByType_plusNumber[4][1]

#parcours tous les nom avec venezia
for i in range(len(nomVenezia)):
    decoupe = re.split("\s",nomVenezia[i][0].lower())
    taille = len(decoupe)
    parcelles= nomVenezia[i][1]
    if taille == 3:
        if (decoupe[2] == 'venezia'):
            public = Public(decoupe[0],parcelles)
            listPublic.append(public)
            for par in parcelles:
                listdeParcelle.append(Parcelle(par, public))
        else: 
            pasEncoreClasse.append(decoupe)
            nbParcNonClass += len(parcelles)
    else :  
        pasEncoreClasse.append(decoupe)
        nbParcNonClass += len(parcelles)

# %%
print(nomVenezia)

#%%
print('entrées classées ',len(listPublic))
print('non classées ',len(pasEncoreClasse))
print('total ',len(nomVenezia))
print('parcelles classée ',len(listdeParcelle))
print('parcelles non classé ',nbParcNonClass)

# %%
"""
for x in listPublic:
    print(x.nom)
    print(x.parcelles)
"""
# %%
https://stackoverflow.com/questions/46408051/python-json-load-set-encoding-to-utf-8
with open('keys.json', encoding='utf-8') as fh:
    data = json.load(fh)
