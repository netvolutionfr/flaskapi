from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flaskext.mysql import MySQL

mysql = MySQL()

app = Flask(__name__)
api = Api(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'api'
mysql.init_app(app)

todos = {}

class TodoList(Resource):
    def get(self):
        cur = mysql.connect().cursor()
        cur.execute('''select * from my_database.my_table''')
        r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        return jsonify({'myCollection': r})


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoList, '/')
api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run()
