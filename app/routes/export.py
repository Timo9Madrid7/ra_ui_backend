from flask.views import MethodView
from flask_smorest import Blueprint
from flask import send_from_directory

from app.services import export_service

blp = Blueprint("Export", __name__, description="Export API")


@blp.route("/exports/<int:simulation_id>")
class ExportList(MethodView):
    @blp.response(200, content_type="application/zip")
    def get(self, simulation_id):
        zip_path = export_service.get_zip_path_by_sim_id(simulation_id)
        return send_from_directory(zip_path.parent, zip_path.name, as_attachment=True)
