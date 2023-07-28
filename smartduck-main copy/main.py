from flask import Flask, render_template, request
from database import engine, getPeriodicTableDataset, use_physics
from sqlalchemy import text

app = Flask(__name__)


def el_import(id):
  with engine.connect() as conn:
    info = conn.execute(text("select * from elementsinfo"))
  info_dict = []
  for el_row in info.all():
    info_dict.append(({
      "Atomic Number": el_row.atomic_no,
      "Symbol": el_row.symbol,
      "Name": el_row.name,
      "Valency": el_row.valency,
      "Group Number": el_row.group_no,
      "Period Number": el_row.period_no,
      "State(Room temp.)": el_row.state_rt,
      "Element Type": el_row.eType
    }))
  return info_dict

def acc_import(id):
  with engine.connect() as conn:
    acc = conn.execute(text("select * from logins"))
  acc_dict = []
  for acc_row in acc.all():
    acc_dict.append(({
      "id": acc_row.id,
      "fullname": acc_row.fullname,
      "username": acc_row.username,
      "password": acc_row.password,
      "email": acc_row.user_email
    }))
  return acc_dict

def load_element_from_db(id):
  with engine.connect() as conn:
    info = conn.execute(text(f"SELECT * FROM elementsinfo WHERE id ={id}"))
    rows = []
    for row in info.all():
      rows.append(({
      "Atomic Number": row.atomic_no,
      "Symbol": row.id,
      "Name": row.name,
      "Valency": row.valency,
      "Group Number": row.group_no,
      "Period Number": row.period_no,
      "State(Room temp.)": row.state_rt,
      "Element Type": row.eType
      }))
    if len(rows) == 0:
      return None
    else:
      return row
    
def add_account_to_db(data):
  data = request.form
  with engine.connect() as conn:
    query = text(f"INSERT INTO logins (fullname, username, email, password) VALUES('{request.form['fullname']}', '{request.form['username']}',  '{request.form['email']}', '{request.form['password']}')") 
    conn.execute(query)


@app.route('/')
def home_screen():
  return render_template('home.html', site_name="SmartDuck")


@app.route('/login', methods=['post', 'get'])
def login():
  data = request.form
  add_account_to_db(data)
  return render_template('login.html', site_name="SmartDuck")


@app.route('/signup', methods=['post', 'get'])
def signup():
  return render_template('signup.html', site_name="SmartDuck")


@app.route('/about_us')
def about_us():
  return render_template('about_us.html', site_name="SmartDuck")


@app.route('/dashboard')
def dashboard():
  return render_template('dashboard.html', site_name="SmartDuck")


@app.route('/chem_periodic_table')
def periodic_table():
  pTable = getPeriodicTableDataset()
  el_import(id)
  return render_template(
    'chem2_table.html',
    site_name="SmartDuck",
    pTable=pTable,
    id = id
  )

@app.route('/physics')
def physics_stuff():
  return render_template('physics.html', site_name="SmartDuck")

@app.route('/quantities')
def phypage():
  phyTable = use_physics()
  return render_template('phypage.html', site_name="SmartDuck", phyTable = phyTable)

@app.route('/constants')
def physics_constants():
  return render_template('constants.html', site_name = "SmartDuck")

@app.route('/formulas/basic')
def physics_formulas():
  return render_template('formulas.html', site_name = "SmartDuck")

@app.route('/el_information/<id>')
def info_show(id):
    importer = acc_import(id)
    return importer

app.run(host='0.0.0.0', port=81, debug=True)
