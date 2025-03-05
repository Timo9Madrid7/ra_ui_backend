import logging
import io
from flask_smorest import abort

from app.models.Export import Export
from app.models.Simulation import Simulation

from app.factory.export_factory.factory import ExportFactory
from config import CustomExportParametersConfig as CustomExportParameters

# Create Logger for this module
logger = logging.getLogger(__name__)


def execute_export(export_dict) -> io.BytesIO:
    try:
        zip_buffer = io.BytesIO()
        exportFactory = ExportFactory()

        simulationIds = export_dict[CustomExportParameters.key_simulationId]

        for key in CustomExportParameters.keys:
            params = export_dict[key]
            if params is None:
                abort(400, message=f"Parameters for {key} is missing.")

            zip_buffer = exportFactory.get_exporter(key, params, simulationIds, zip_buffer)

        return zip_buffer

    except Exception as ex:
        abort(400, message=f"Error while getting the zip file path: {ex}")
        return None
