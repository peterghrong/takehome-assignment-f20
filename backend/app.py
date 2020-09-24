from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message


    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/shows", methods=['GET'])
def get_all_shows():
    # this part is Bonus question 6
    minEpisodes = request.args.get('minEpisodes')
    if minEpisodes is not None:
        new_list = []
        for item in db.get('shows'):
            if item["episodes_seen"] >= int(minEpisodes):
                new_list.append(item)
        if len(new_list) == 0:
            return create_response(status=404, message="no shows matching the param")
        else:
            return create_response({"shows": new_list})
    # below is function one
    else:
        return create_response({"shows": db.get('shows')})


@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!

@app.route("/shows/<id>", methods=['GET'])
def get_show(id):
    if (db.getById('shows', int(id)) is None):
        return create_response(status=404, message="No show with this id exists")
    else:
        return create_response(db.getById('shows', int(id)))


@app.route("/shows", methods=['POST'])
def new_show():
    # this part returns value in Postman, refresh browser to see server update
    package = request.get_json()
    if ("episodes_seen" not in package or "name" not in package):
        return create_response(status=404, message="Faulty input")

    else:
        apd = db.create('shows', package)
        new_id = apd["id"]
        return create_response(db.getById('shows', int(new_id)), status=201)


@app.route("/shows/<id>", methods=["PUT"])
def update_show(id):
    update_package = request.get_json()
    result = db.updateById('shows', int(id), update_package)
    if result is None:
        return create_response(status=404, message="No show with this id exists")
    else:
        return create_response(db.getById('shows', int(id)), status=201)


# """
# ~~~~~~~~~~~~ END API ~~~~~~~~~~~~
# """
if __name__ == "__main__":
    app.run(port=8080, debug=True)
