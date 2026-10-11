from operator import attrgetter

class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return f"{self.tipo}, {self.marca}, {self.anno_acquisto}, {self.valore}"


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito: {self.id_prestito}, Data: {self.data}, Cognome: {self.cognome_allievo}, Strumento: {self.id_strumento}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.lista_responsabili=[responsabile]
        self.strumenti=[]
        self.prestiti=[]
        self.count = 1


    def aggiungi_responsabile(self,nuovo_responsabile):
        self.lista_responsabili.append(nuovo_responsabile)


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            f = open(file_path,'r')
            for line in f:
                line = line.strip()
                campo = line.split(",")


                codice=campo[0].strip()
                nome=campo[1].strip()
                marca=campo[2].strip()
                anno=int(campo[3].strip())
                valore=float(campo[4].strip())

                nuovo_strumento=Strumento(codice,nome,marca,anno,valore)
                self.strumenti.append(nuovo_strumento)

            f.close()

        except FileNotFoundError:
            print("Carica file non esistente")
            return None

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore, codice=None):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        nuovo_strumento=Strumento(codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_strumento)
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti, key=attrgetter('marca'))


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        trovato = False
        for elem in self.strumenti:
            if elem.codice == id_strumento:
                trovato = True
                break
        if not trovato:
            raise Exception("Strumento non esistente")

        for p in self.prestiti:
            if p.id_strumento == id_strumento:
                raise Exception("Strumento già in prestito")

        nuovo = Prestito(f"P{self.count}", data, id_strumento, cognome_allievo)
        self.count += 1
        self.prestiti.append(nuovo)
        return nuovo


    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        for p in self.prestiti:
            if p.id_prestito == id_prestito:
                self.prestiti.remove(p)
                return
        raise Exception("Prestito non esistente")

