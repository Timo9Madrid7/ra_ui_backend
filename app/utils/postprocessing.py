from typing import Dict, List, Optional
import json
import zipfile
import pandas as pd
import logging

# Create Logger for this module
logger = logging.getLogger(__name__)


class ExcelExportHelper:
    def __init__(self, load_path: str, save_path: str, export_separate_csvs: bool = True) -> None:
        """`ExcelExportHelper` is for converting simulation results to an Excel file

        Args:
            load_path (str): the path to the JSON file containing the simulation results, extension included.
            save_path (str): the path to save the Excel file, extension included.
            export_separate_csvs (bool, optional): whether **also** convert results to
                csv files separately. Defaults to True.
        """
        self.load_path = load_path
        self.save_path = save_path
        self.export_separate_csvs = export_separate_csvs

    def export(self) -> bool:
        """Convert simulation results to an Excel file

        Returns:
            bool: conversion success or not
        """
        data: Optional[Dict] = self.__load_json__()
        if data is None:
            return False

        return self.__save_as_xlsx__(data)

    def make_zip(self) -> bool:
        """zip the Excel file and the separate csv files

        Returns:
            bool: zipping success or not
        """
        try:
            with zipfile.ZipFile(self.save_path.replace('.xlsx', '.zip'), 'w') as zipf:
                zipf.write(self.save_path)
                if self.export_separate_csvs:
                    zipf.write(self.save_path.replace('.xlsx', '_parameters.csv'))
                    zipf.write(self.save_path.replace('.xlsx', '_edc.csv'))
                    zipf.write(self.save_path.replace('.xlsx', '_pressure.csv'))
        except Exception as e:
            logger.error(f'Error zipping files: {e}')
            return False

        return True

    def __load_json__(self) -> Optional[Dict]:
        try:
            with open(self.load_path, 'r') as file:
                data: Dict = json.load(file)
        except FileNotFoundError as e:
            logger.error(f'File not found: {e}')
            return None

        return data

    def __save_as_xlsx__(self, data: Dict) -> bool:
        try:
            # TODO: Multiple sources and multiple receivers
            receiver_results: List[Dict[str, List[int]]] = data['results'][0]['responses'][0]['receiverResults']
            parameters: Dict[str, List[int]] = data['results'][0]['responses'][0]['parameters']

            parameter_sheet = pd.DataFrame(parameters)
            edc_sheet = pd.DataFrame()
            pressure_sheet = pd.DataFrame()

            # fill in edc_sheet and pressure_sheet
            time = receiver_results[0]['t']
            edc_sheet['t'] = time
            pressure_sheet['t'] = time
            for result in receiver_results:
                edc_sheet[str(result['frequency']) + 'Hz'] = result['data']
                pressure_sheet[str(result['frequency']) + 'Hz'] = result['data_pressure']

            with pd.ExcelWriter(self.save_path) as writer:
                parameter_sheet.to_excel(writer, sheet_name='Parameters', index=False)
                edc_sheet.to_excel(writer, sheet_name='EDC', index=False)
                pressure_sheet.to_excel(writer, sheet_name='Pressure', index=False)

            if self.export_separate_csvs:
                parameter_sheet.to_csv(self.save_path.replace('.xlsx', '_parameters.csv'), index=False)
                edc_sheet.to_csv(self.save_path.replace('.xlsx', '_edc.csv'), index=False)
                pressure_sheet.to_csv(self.save_path.replace('.xlsx', '_pressure.csv'), index=False)

        except Exception as e:
            logger.error(f'Error saving data to xlsx: {e}')
            return False

        return True
