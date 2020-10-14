from flask import Flask, json, request
from movie_recommender import return_cosine_sim, get_recommendations

messages = {"id": 1, "message": "Company One"}

api = Flask(__name__)
cosine_sim, metadata, indices = None, None, None


def run_before_app():
    global cosine_sim, metadata, indices
    cosine_sim, metadata, indices = return_cosine_sim()
    print("Run before method complete")


@api.route('/message', methods=['GET'])
def get_reply():
    in_msg = request.args.get("incoming")
    print(cosine_sim, metadata, indices)
    a = get_recommendations(in_msg, metadata, indices, cosine_sim)
    # msg.append(metadata.loc[a.index]['imdbURL'])
    result = {"message": metadata.loc[a.index]['imdbURL'].tolist()}
    print(result)
    return json.dumps(result)


if __name__ == '__main__':
    run_before_app()
    api.run(port=3000)
