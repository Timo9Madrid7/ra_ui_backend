import io
import logging

from flask_smorest import abort
from virtualenv.config.convert import ListType

from app.models import Export
from app.models.Simulation import Simulation
from config import DefaultConfig
import os

from app.factory.export_factory.export_helper import ExportHelper
from app.factory.export_factory.strategy import ExportStrategy

# Create logger for this module
logger = logging.getLogger(__name__)


class ExportParameters(ExportStrategy):
    def export(self, export_type: str, params: ListType, simulationIds: ListType, zip_buffer: io.BytesIO) -> io.BytesIO:
        try:
            if params:
                for id in simulationIds:
                    simulation: Simulation = Simulation.query.filter_by(id=id).first()
                    export: Export = simulation.export
                    xlsx_file_name: str = export.name

                    if not xlsx_file_name:
                        logger.error("Parameters export with simulation is " + str(id) + "does not exists!")
                        abort(400, message="Excel file doesn't exists!")

                    xlsx_path = os.path.join(DefaultConfig.UPLOAD_FOLDER_NAME, xlsx_file_name)

                    zip_buffer = ExportHelper.extract_from_xlsx_to_csv_to_zip_binary(
                        xlsx_path, {export_type: params}, zip_buffer, id
                    )

            return zip_buffer

        except Exception as e:
            logger.error("Error while writing parameters csv file to zip buffer: " + str(e))
            abort(400, message="Error while writing parameters csv file to zip buffer: " + str(e))
