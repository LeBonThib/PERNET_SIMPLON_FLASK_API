from crawlerino import create_app
from crawlerino.api_funcs import api_get_url_from_db, api_yeet, scraperino
from flask_restful import Api, Resource

app = create_app()
api = Api(app)

class api_get_test(Resource):
    def get(self, get_id): 
        result_id_from_get_id,result_url_from_get_id, result_content_from_get_id = api_get_url_from_db(get_id)
        return {"id": result_id_from_get_id, "url": result_url_from_get_id, "content":result_content_from_get_id}

class api_post_test(Resource):
    def post(self, post_url):
        url = "https://fr.wikipedia.org/wiki/" + post_url
        scraperino(url)
        eastereggerino = "https://www.youtube.com/watch?v=5r06heQ5HsI"
        return {"message": eastereggerino}

class api_delete_test(Resource):
    def delete(self, delete_id):
        api_yeet(delete_id)
        eastereggerino = "https://www.youtube.com/watch?v=5r06heQ5HsI"
        return {"message": eastereggerino}

api.add_resource(api_get_test, "/api/get/<int:get_id>")
api.add_resource(api_post_test, "/api/post/<string:post_url>")
api.add_resource(api_delete_test, "/api/delete/<int:delete_id>")

# enable debugging mode
app.config["DEBUG"] = True

if __name__ == '__main__': #prevents web server starting without running main.py (e.g: can't import it and run it from another file)
    app.run()