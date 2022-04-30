import json
from pathlib import Path
import io
import uuid

def read_geojson(data):
    suported_file_types = ['.geojson']
    if isinstance(data, str):
        try:
            p = Path(data)
            pass
        except OSError as e:
            p = Path(str(uuid.uuid4()))
        if p.exists():
            if p.suffix not in suported_file_types:
                raise TypeError('Data file must be a suported file type')
            with open(p, 'r') as f:
                data = f.read()
                return json.loads(data)
        else:
            return json.loads(data)
    elif isinstance(data, io.IOBase):
        data = data.read()
        return json.loads(data)
    elif isinstance(data, dict):
        return data
    else:
        raise TypeError('Invalid input data')