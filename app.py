
import dbcreds
import mariadb
from flask import Flask, request, Response
import json

app = Flask(__name__)
cursor = None
conn = None

try:
    conn=mariadb.connect(
                    user=dbcreds.user,
                    password=dbcreds.password,
                    host=dbcreds.host,
                    port=dbcreds.port,
                    database=dbcreds.database
                    )
    cursor = conn.cursor()

    @app.route('/animals', methods=['GET', 'POST', 'PATCH', 'DELETE'])
    def animal():

        if (request.method =='GET'):
            params = request.args
            cursor.execute("SELECT * FROM animals")
            conn.commit()
            animal_lists = cursor.fetchall()
            print(params)
            return Response (json.dumps(animal_lists),
                            mimetype="application/jason",
                            status=200)

        elif (request.method == 'POST'):
            data = request.json
            print(data)
            posted_animal = data.get('name')
            cursor.execute("INSERT INTO animals(name) VALUES(?)", [posted_animal])
            conn.commit()
            if (posted_animal != None):
                print(posted_animal)
            else:
                print("We can not find that animal")
            return Response (json.dumps(posted_animal),
                            mimetype="application/json",
                            status=200
                            )
        elif (request.method == 'PATCH'):
            data = request.json
            print(data)
            animalId = data.get('id')
            posted_animal = data.get('name')
            cursor.execute("UPDATE animals SET name=? WHERE id=?", [posted_animal, animalId])
            conn.commit()
            return Response (json.dumps(posted_animal),
                            mimetype="application/json",
                            status=200
                            )
        elif (request.method == 'DELETE'):
            data = request.json
            posted_animal = data.get('name')
            cursor.execute("DELETE FROM animals WHERE name=?", [posted_animal])
            conn.commit()
            return Response (json.dumps(posted_animal),
                            mimetype="application/json",
                            status=200
                            )
except mariadb.OperationalError:
    print("There seems to be a connection issue!")
except mariadb.ProgrammingError:
    print("Apparently you do not know how to code")
except mariadb.IntergrityError:
    print("Error with DB integrity, most likely consraint failure")
except:
    print("Opps! Somthing went wrong")
finally:
    if (cursor != None):
        cursor.close()
    else:
        print("No cursor to begin with.")

    if (conn != None):
        conn.rollback()
        conn.close()
    else:
            print("No connection!")