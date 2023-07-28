from sqlalchemy import create_engine, text
from flask import request

engine = create_engine("mysql+pymysql://yzbnn9ec04w04sgqe0d4:pscale_pw_sRgsiln5sNFgn4R8TwpKXEWkGls0bvB7f1HslQ0EvRJ@aws.connect.psdb.cloud/smartduck?charset=utf8mb4",
  connect_args={"ssl": {
    "ssl_ca": "cert.pem"
  }})

def getPeriodicTableDataset():
  _rows = 10
  _cols = 18

  pTable = [['' for x in range(_cols)] for y in range(_rows)]

  for p in range(_rows):
    with engine.connect() as conn:
      periodResult = conn.execute(
        text(f"select * from elementsinfo where posRow={p}"))
    for pr in periodResult:
      pTable[pr.posRow][pr.posCol] = str(pr.atomic_no) +'-'+ pr.symbol +'-'+ pr.name +'-'+ pr.eType + '-'+ str(pr.valency)
  return pTable


# def clicked_element():
#   with engine.connect() as conn:
#     info = conn.execute(text("select * from elementsinfo"))
#   info_dict = []
#   for el_row in info.all():
#     info_dict.append(({
#       "Atomic Number": el_row.atomic_no,
#       "Symbol": el_row.id,
#       "Name": el_row.name,
#       "Valency": el_row.valency,
#       "Group Number": el_row.group_no,
#       "Period Number": el_row.period_no,
#       "State(Room temp.)": el_row.state_rt
#     }))
#   return info_dict

# 


def use_physics():
  with engine.connect() as conn:
    phyTimes = range(5)
    for n in phyTimes:
      for a in range(n):
        phyResult = conn.execute(text(f"select * from physics where id={a}"))
        for xy in phyResult:
          phyTable = [xy.fullname, xy.symbol, xy.unit, str(xy.val), str(xy.charge)]
  return phyTable




