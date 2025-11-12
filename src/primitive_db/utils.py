import json
import os

from .consts import METAFILE, DATADIR


def delete_table(table_name):
    filepath = f'{DATADIR}{table_name}.json'
    os.remove(filepath)
def load_metadata(filepath=METAFILE):
    """загружает метаинформацию о базе данных"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(data, filepath=METAFILE):
    """обновляет метаинформацию о базе данных"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
def load_table_data(table_name):
    """загружает информацию о таблице"""
    filepath = f'{DATADIR}{table_name}.json'
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def save_table_metadata(data, table_name):
    """обнавляет информацию о таблице"""
    filepath = f'{DATADIR}{table_name}.json'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)