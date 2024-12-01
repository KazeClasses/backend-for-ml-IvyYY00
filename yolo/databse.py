from flask import Blueprint, request, jsonify, current_app
import psycopg
import psycopg.rows

database_service = Blueprint("database", __name__)

def connect_postgres() -> psycopg.Connection[psycopg.rows.TupleRow]:
    """
    Establish a connection to the PostgreSQL database.
    """
    database_client = psycopg.connect(
        host=current_app.config["POSTGRES_HOST"],
        port=current_app.config["POSTGRES_PORT"],
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],
        dbname=current_app.config["POSTGRES_DB"],
        row_factory=psycopg.rows.dict_row
    )
    return database_client

@database_service.route("/create_table", methods=["POST"])
def create_table():
    """
    API endpoint to create a table named 'classes'.
    """
    with connect_postgres() as client:
        with client.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS classes (id UUID PRIMARY KEY, name TEXT)"
            )
    return jsonify({"message": "Table created successfully"}), 201

@database_service.route("/get_table", methods=["GET"])
def get_table():
    """
    API endpoint to retrieve all rows from the 'classes' table.
    """
    with connect_postgres() as client:
        with client.cursor() as cursor:
            cursor.execute("SELECT * FROM classes")
            rows = cursor.fetchall()
    return jsonify(rows), 200

@database_service.route("/add_class", methods=["POST"])
def add_class():
    """
    API endpoint to add a class to the 'classes' table.
    """
    with connect_postgres() as client:
        with client.cursor() as cursor:
            data = request.form
            class_name = data.get("class")
            if not class_name:
                return jsonify({"error": "Class name is required"}), 400
            cursor.execute(
                "INSERT INTO classes (id, name) VALUES (gen_random_uuid(), %s)",
                (class_name,)
            )
    return jsonify({"message": "Class added successfully"}), 201
