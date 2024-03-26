import json, os

try:
  os.mkdir('data')
except FileExistsError:
  pass

def readJson(filePath: str, defaultReturn = {}):
  try: 
    with open(filePath, 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return defaultReturn

def writeJson(filePath: str, data: dict):
  with open(filePath, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
