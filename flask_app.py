from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_resume_project'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///delivery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    requests = db.relationship('Task', foreign_keys='Task.requester_id', backref='requester', lazy=True)
    deliveries = db.relationship('Task', foreign_keys='Task.accepter_id', backref='accepter', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    pickup_location = db.Column(db.String(200), nullable=False)
    dropoff_location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="Pending")
    
    vehicle_type = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    accepter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

with app.app_context():
    db.create_all()

# --- AUTHENTICATION ROUTES ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# --- MAIN APP ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    current_user = User.query.get(session['user_id'])

    if request.method == 'POST':
        item = request.form['item_name']
        pickup = request.form['pickup_location']
        dropoff = request.form['dropoff_location']
        vehicle = request.form.get('vehicle_type')
        price = request.form.get('price')
        
        new_task = Task(
            item_name=item, 
            pickup_location=pickup, 
            dropoff_location=dropoff, 
            vehicle_type=vehicle,  
            price=price,           
            requester_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
        
    search_query = request.args.get('search')
    if search_query:
        all_tasks = Task.query.filter(Task.item_name.contains(search_query)).all()
    else:
        all_tasks = Task.query.all()
        
    return render_template('index.html', tasks=all_tasks, current_user=current_user)

@app.route('/accept/<int:task_id>', methods=['POST'])
def accept_task(task_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    task_to_update = Task.query.get_or_404(task_id)
    
    # SECURITY: Prevent accepting your own task
    if task_to_update.requester_id == session['user_id']:
        return redirect(url_for('home'))
        
    task_to_update.status = "Accepted"
    task_to_update.accepter_id = session['user_id']
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    task_to_delete = Task.query.get_or_404(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    current_user = User.query.get(session['user_id'])
    my_requests = Task.query.filter_by(requester_id=current_user.id).all()
    my_deliveries = Task.query.filter_by(accepter_id=current_user.id).all()
    return render_template('profile.html', current_user=current_user, my_requests=my_requests, my_deliveries=my_deliveries)

if __name__ == '__main__':
    app.run(debug=True)