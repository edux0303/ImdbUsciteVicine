from database.DB_connect import DBConnect
from model.movie import Movie

class DAO:
    @staticmethod
    def getGeneri():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT genre AS nome
                   FROM genre
                   ORDER BY genre"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["nome"])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT year AS anno
                   FROM movie
                   ORDER BY year"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getNodi(genere, anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT m.id AS id, m.title AS titolo, m.date_published AS data,
                          r.avg_rating AS voto, r.total_votes AS voti
                   FROM movie m, genre g, ratings r
                   WHERE m.id = g.movie_id
                     AND m.id = r.movie_id
                     AND g.genre = %s
                     AND m.year = %s
                     AND r.total_votes >= 5000"""
        cursor.execute(query, (genere, anno))
        for row in cursor:
            result.append(Movie(row["id"], row["titolo"], row["data"],
                                float(row["voto"]), row["voti"]))
        cursor.close()
        cnx.close()
        return result


