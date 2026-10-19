from csv import reader

class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = superficie
        self.padiglione = padiglione
        self.prezzo_base = prezzo_base
        self.tipo = "Standard"
        self.disponibile = True
        self.espositore = None

    def calcola_prezzo(self):
        return self.prezzo_base

    def __str__(self):
        if self.disponibile:
            stato = "Disponibile"
        else:
            stato = f"Assegnato a {self.espositore.codice} - {self.espositore.nome} {self.espositore.cognome}"

        return (
            f"{self.codice}: {self.tipo} | {self.superficie} mq - Padiglione {self.padiglione} - "
            f"Prezzo {self.calcola_prezzo():.2f} euro - {stato}"
        )

class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
        # Uso super() per inizializzare gli attributi comuni a tutti gli stand
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.tipo = "Prese Extra"
        self.numero_prese = numero_prese

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.numero_prese)

    def __str__(self):
        return super().__str__() + f" - Prese aggiuntive: {self.numero_prese}"

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __str__(self):
        if self.stand is None:
            return f"{self.codice} - {self.nome} {self.cognome} - Nessuno stand assegnato"

        return f"{self.codice} - {self.nome} {self.cognome} - Stand {self.stand.codice}"

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.stand = []
        self.espositori = []

    def __str__(self):
        return f"{self.nome} - Stand: {len(self.stand)} - Espositori: {len(self.espositori)}"

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            lettore = reader(csvfile, delimiter=',')
            for riga in lettore:
                if not riga:
                    continue

                codice = riga[0].strip()
                if codice[:2] == "ST":
                    presente = False
                    for stand in self.stand:
                        if stand.codice == codice:
                            presente = True
                            break

                    # Se ricarico il file mantengo gli stand e le assegnazioni già presenti
                    if presente:
                        continue

                    superficie = float(riga[1])
                    padiglione = int(riga[2])
                    prezzo_base = float(riga[3])

                    if len(riga) == 4:
                        nuovo_stand = Stand(codice, superficie, padiglione, prezzo_base)
                    else:
                        try:
                            numero_prese = int(riga[4])
                            nuovo_stand = StandPreseExtra(codice, superficie, padiglione, prezzo_base, numero_prese)
                        except ValueError:
                            nuovo_stand = StandPremium(codice, superficie, padiglione, prezzo_base, riga[4].strip())

                    self.stand.append(nuovo_stand)

                elif codice[:2] == "ES":
                    presente = False
                    for espositore in self.espositori:
                        if espositore.codice == codice:
                            presente = True
                            break

                    if not presente:
                        nuovo_espositore = Espositore(codice, riga[1].strip(), riga[2].strip())
                        self.espositori.append(nuovo_espositore)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand_trovato = None
        for stand in self.stand:
            if stand.codice == codice_stand:
                stand_trovato = stand
                break

        if stand_trovato is None:
            raise Exception("Stand non presente nel sistema.")

        espositore_trovato = None
        for espositore in self.espositori:
            if espositore.codice == codice_espositore:
                espositore_trovato = espositore
                break

        if espositore_trovato is None:
            raise Exception("Espositore non presente nel sistema.")

        if not stand_trovato.disponibile:
            raise Exception("Stand già assegnato a un espositore.")

        if espositore_trovato.stand is not None:
            raise Exception("L'espositore ha già uno stand assegnato.")

        # Salvo i riferimenti agli oggetti per ritrovare l'associazione da entrambi
        stand_trovato.espositore = espositore_trovato
        stand_trovato.disponibile = False
        espositore_trovato.stand = stand_trovato

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for espositore in self.espositori:
            print(espositore)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        stand_ordinati = []
        for stand in self.stand:
            stand_ordinati.append(stand)

        # Ogni tipologia calcola il proprio prezzo, compreso l'eventuale sovrapprezzo
        stand_ordinati.sort(key=lambda stand: stand.calcola_prezzo())
        return stand_ordinati
