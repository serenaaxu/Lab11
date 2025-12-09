from database.DB_connect import DBConnect
from model.rifugio import Rifugio


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO
    @staticmethod
    def get_all_rifugi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * FROM rifugio"""
        cursor.execute(query)

        for row in cursor:
            result.append(Rifugio(
                row["id"],
                row["nome"],
                row["localita"],
                row["altitudine"],
                row["capienza"],
                bool(row["aperto"])
            ))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_edges_by_year(year):
        """
        Recupera le connessioni (id_rifugio1, id_rifugio2)
        dove l'anno del sentiero è <= all'anno passato.
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
                    SELECT id_rifugio1, id_rifugio2 
                    FROM connessione 
                    WHERE anno <= %s
                    """
        cursor.execute(query, (year,))

        for row in cursor:
            result.append((row["id_rifugio1"], row["id_rifugio2"]))

        cursor.close()
        cnx.close()
        return result


