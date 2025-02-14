from typing import Dict

from flask.views import MethodView
from flask_smorest import Blueprint
from flask import send_from_directory

from app.services import auralization_service
from app.schemas.auralization_schema import AudioFileSchema, AuralizationSchema

blp = Blueprint("Auralization", __name__, description="Auralization API")


@blp.route("/auralizations/aduiofiles")
class AudioFileList(MethodView):
    @blp.response(200, AudioFileSchema(many=True))
    def get(self):
        audio_files = auralization_service.get_all_audio_files()
        return audio_files


@blp.route("/auralizations")
class AuralizationTask(MethodView):
    @blp.arguments(AuralizationSchema)
    @blp.response(200, AuralizationSchema)
    def post(self, body_data: Dict):
        result = auralization_service.create_new_auralization(body_data["simulationId"], body_data["audioFileId"])
        return result


@blp.route("/auralizations/<int:auralization_id>/status")
class AuralizationStatus(MethodView):
    @blp.response(200, AuralizationSchema)
    def get(self, auralization_id):
        result = auralization_service.get_auralization_by_id(auralization_id)
        return result
