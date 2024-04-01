import json, os

try:
  os.mkdir('data')
except FileExistsError:
  pass

def readJson(filePath: str, defaultReturn = {}, intKeys=False):
  try: 
    with open(filePath, 'r') as f:
      if intKeys:
        return {int(k): v for k, v in json.load(f).items()}
      else:
        return json.load(f)
  except FileNotFoundError:
    return defaultReturn

def writeJson(filePath: str, data: dict):
  with open(filePath, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
