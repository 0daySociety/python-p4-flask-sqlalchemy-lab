#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    
    if not animal:
        response_body = "<h1>404 pet not found</h1>"
        response = make_response(response_body, 404)
        return response
    
    zookeeper = Zookeeper.query.filter_by(id=animal.zookeeper_id).first()
    my_enclosure=Enclosure.query.filter_by(id=animal.enclosure_id).first()
    
    response_body = f'''
        <ul>
            <li>ID: {animal.id}</li>
            <li>Name: {animal.name}</li>
            <li>Species: {animal.species}</li>
            <li>Zookeeper: {zookeeper.name if zookeeper else 'Unknown'}</li>
            <li>Enclosure:{my_enclosure.environment}</li>
        </ul>'''
    
    response = make_response(response_body, 200)
    return response
    
@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    def animal():
        animals = Animal.query.filter(Animal.zookeeper_id == id).all()
        
        animal_list = []
        for animal in animals:
            animal_list.append(f"<li>Animal : {animal.name}</li>")
        return "\n".join(animal_list) 
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
   
    if not zookeeper:
        response = "<h1>Error 404 page not found.<h1>"
        return make_response(response, 404)

    animal_names = animal()  

    response = f'''
        <h1>Zookeeper Details</h1>
        <ul>
            <li>ID: {zookeeper.id}</li>
            <li>Name: {zookeeper.name}</li>
            <li>Birthday: {zookeeper.birthday}</li>
            Animal :{animal_names}
        </ul>
    '''

    return make_response(response, 200)
@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure=Enclosure.query.filter(Enclosure.id==id).first()
 
    def animal():
        animals=Animal.query.filter(Animal.enclosure_id==id).all()
        animal_list=[]
       
        for animal in animals:
            print(animal.name)
            animal_list.append(f"<li>Animal :{animal.name}</li>")
        return "\n".join(animal_list)        


        


    enclosure_animal_name=animal()
    response =f'''
                <li>ID:{enclosure.id}</li>
                <li>Enviroment:{enclosure.environment}</li>
                <li>Open to Visitors :{enclosure.open_to_visitors}</li>
                {enclosure_animal_name}
                 '''
    
    return make_response(response,200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
