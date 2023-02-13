from flask import Flask, request, jsonify
from flask.views import MethodView
from db2 import Advertisement, Session
from schema2 import validate_create_advertisement
from errors import HttpError
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

app = Flask('server')
bcrypt = Bcrypt(app)

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response

def get_advertisement(advertisement_id: int, session: Session):
    advertisement = session.query(Advertisement).get(advertisement_id)
    if advertisement is None:
        raise HttpError(404, 'advertisement not found')
    return advertisement

class AdvertisementView(MethodView):

    def get(self, advertisement_id: int):
        with Session() as session:
            advertisement = get_advertisement(advertisement_id, session)
            return jsonify(
                {
                    'id': advertisement.id,
                    'header': advertisement.header,
                    'description': advertisement.description,
                    'creation_time': advertisement.creation_time,
                    'owner': advertisement.owner
                }
            )

    def post(self):
        json_data = validate_create_advertisement(request.json)
        with Session() as session:
            new_advertisement = Advertisement(**json_data)
            session.add(new_advertisement)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'advertisement already exists')
            return jsonify(
                {
                    'id': new_advertisement.id,
                    'description': new_advertisement.description,
                    'owner': new_advertisement.owner
                }
            )

    def patch(self, advertisement_id: int):
        json_data = request.json
        with Session() as session:
            advertisement = get_advertisement(advertisement_id, session)
            for field, value in json_data.items():
                setattr(advertisement, field, value)
            session.add(advertisement)
            session.commit()
        return jsonify({"status": 'succes'})

    def delete(self, advertisement_id: int):
        with Session() as session:
            advertisement = get_advertisement(advertisement_id, session)
            session.delete(advertisement)
            session.commit()
            return jsonify({"status": 'succes'})

app.add_url_rule('/advertisement/<int:advertisement_id>', view_func=AdvertisementView.as_view('advertisement_with_id'),
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/advertisement', view_func=AdvertisementView.as_view('advertisement'), methods=['POST'])

app.run(port=5001)


