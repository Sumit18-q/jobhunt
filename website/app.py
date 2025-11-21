from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobhunt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# User Profile Model
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    skills = db.Column(db.Text)  # Comma-separated skills
    experience_years = db.Column(db.Integer, default=0)
    resume_filename = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(255))
    location = db.Column(db.String(100))
    current_position = db.Column(db.String(100))
    education = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('profile', uselist=False))

# Job Model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # full-time, part-time, etc.
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    benefits = db.Column(db.Text)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Job Application Model
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, accepted, rejected
    cover_letter = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    applicant = db.relationship('User', backref=db.backref('applications', lazy=True))

# Saved Job Model
class SavedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('saved_jobs', lazy=True))
    job = db.relationship('Job', backref=db.backref('saved_by', lazy=True))

# Message Model for communication system
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_messages', lazy=True))
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref=db.backref('received_messages', lazy=True))

# Conversation Model to group messages between users
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_message_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user1 = db.relationship('User', foreign_keys=[user1_id], backref=db.backref('conversations_as_user1', lazy=True))
    user2 = db.relationship('User', foreign_keys=[user2_id], backref=db.backref('conversations_as_user2', lazy=True))

# Company Model
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    logo_filename = db.Column(db.String(255))
    website = db.Column(db.String(255))
    location = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    creator = db.relationship('User', backref=db.backref('companies', lazy=True))
    jobs = db.relationship('Job', backref='company_rel', lazy=True)
    reviews = db.relationship('CompanyReview', backref='company', lazy=True)

# Company Review Model
class CompanyReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('company_reviews', lazy=True))

# Create database tables
with app.app_context():
    db.drop_all()
    db.create_all()

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return render_template('register.html')

    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')

        # Query jobs based on search
        query = Job.query
        if title:
            query = query.filter(Job.title.ilike(f'%{title}%'))
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))

        jobs_list = query.order_by(Job.created_at.desc()).all()
        return render_template('jobs.html', jobs=jobs_list)

    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/jobs')
def jobs():
    # Get filter parameters
    title = request.args.get('title', '')
    location = request.args.get('location', '')
    job_type = request.args.get('type', '')
    salary_min = request.args.get('salary_min', '')
    salary_max = request.args.get('salary_max', '')
    experience_level = request.args.get('experience', '')
    skills = request.args.get('skills', '')

    # Build query
    query = Job.query

    if title:
        query = query.filter(Job.title.ilike(f'%{title}%'))
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    if job_type:
        query = query.filter(Job.type.ilike(f'%{job_type}%'))
    if salary_min:
        # Assuming salary is stored as string like "50000-70000", parse min
        # For simplicity, filter if salary contains the min value
        query = query.filter(Job.salary.ilike(f'%{salary_min}%'))
    if salary_max:
        query = query.filter(Job.salary.ilike(f'%{salary_max}%'))
    if experience_level:
        # Map experience level to years
        exp_map = {'entry': 0, 'mid': 3, 'senior': 5}
        if experience_level in exp_map:
            # This is simplistic; in real app, jobs might have experience requirements
            pass  # For now, skip as Job model doesn't have experience field
    if skills:
        # Filter jobs where requirements or description contain skills
        skill_list = [s.strip() for s in skills.split(',')]
        for skill in skill_list:
            query = query.filter(
                db.or_(
                    Job.description.ilike(f'%{skill}%'),
                    Job.requirements.ilike(f'%{skill}%')
                )
            )

    jobs_list = query.order_by(Job.created_at.desc()).all()

    # Get saved jobs for logged in user
    saved_job_ids = []
    if 'user_id' in session:
        saved_jobs = SavedJob.query.filter_by(user_id=session['user_id']).all()
        saved_job_ids = [sj.job_id for sj in saved_jobs]

    return render_template('jobs.html', jobs=jobs_list, saved_job_ids=saved_job_ids)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    user = User.query.get(session.get('user_id')) if 'user_id' in session else None
    has_applied = False
    if user:
        has_applied = JobApplication.query.filter_by(job_id=job_id, applicant_id=user.id).first() is not None
    return render_template('job_details.html', job=job, has_applied=has_applied)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        confirm_password = request.form.get('c_pass')

        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        # Create new user
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))

@app.route('/post-job', methods=['GET', 'POST'])
def post_job():
    if 'user_id' not in session:
        flash('Please login to post a job', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        title = request.form.get('title')
        company_option = request.form.get('company_option')  # 'existing' or 'new'
        company_id = request.form.get('company_id')
        new_company_name = request.form.get('new_company_name')
        location = request.form.get('location')
        salary = request.form.get('salary')
        type = request.form.get('type')
        description = request.form.get('description')

        # Validation
        if not all([title, location, salary, type, description]):
            flash('All fields are required', 'error')
            return redirect(url_for('post_job'))

        if company_option == 'existing':
            if not company_id:
                flash('Please select a company', 'error')
                return redirect(url_for('post_job'))
            company = Company.query.get_or_404(company_id)
            company_name = company.name
        elif company_option == 'new':
            if not new_company_name:
                flash('Please enter a company name', 'error')
                return redirect(url_for('post_job'))
            # Check if company already exists
            existing_company = Company.query.filter_by(name=new_company_name).first()
            if existing_company:
                company = existing_company
            else:
                # Create new company
                company = Company(name=new_company_name, created_by=user_id)
                db.session.add(company)
                db.session.commit()
            company_name = company.name
            company_id = company.id
        else:
            flash('Invalid company option', 'error')
            return redirect(url_for('post_job'))

        # Create new job
        job = Job(title=title, company=company_name, company_id=company_id, location=location, salary=salary, type=type, description=description, posted_by=user_id)
        db.session.add(job)
        db.session.commit()

        flash('Job posted successfully!', 'success')
        return redirect(url_for('jobs'))

    # Get user's companies for dropdown
    user_companies = Company.query.filter_by(created_by=user_id).all()

    return render_template('post_job.html', user_companies=user_companies)

@app.route('/account')
def account():
    if 'user_id' not in session:
        flash('Please login to access your account', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        session.clear()
        flash('User not found. Please login again.', 'error')
        return redirect(url_for('login'))

    profile = UserProfile.query.filter_by(user_id=user.id).first()
    applications = JobApplication.query.filter_by(applicant_id=user.id).order_by(JobApplication.applied_at.desc()).all()
    saved_jobs = SavedJob.query.filter_by(user_id=user.id).order_by(SavedJob.saved_at.desc()).all()
    return render_template('account.html', user=user, profile=profile, applications=applications, saved_jobs=saved_jobs)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please login to access your profile', 'error')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    profile = UserProfile.query.filter_by(user_id=user.id).first()

    if request.method == 'POST':
        # Create or update profile
        if not profile:
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)

        # Update profile fields
        profile.phone = request.form.get('phone')
        profile.bio = request.form.get('bio')
        profile.skills = request.form.get('skills')
        profile.experience_years = int(request.form.get('experience_years', 0))
        profile.linkedin_url = request.form.get('linkedin_url')
        profile.portfolio_url = request.form.get('portfolio_url')
        profile.location = request.form.get('location')
        profile.current_position = request.form.get('current_position')
        profile.education = request.form.get('education')

        # Handle resume upload
        if 'resume' in request.files:
            resume_file = request.files['resume']
            if resume_file.filename:
                # Save resume file
                resume_filename = f"{user.id}_{resume_file.filename}"
                resume_path = os.path.join('uploads', 'resumes')
                os.makedirs(resume_path, exist_ok=True)
                resume_file.save(os.path.join(resume_path, resume_filename))
                profile.resume_filename = resume_filename

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user, profile=profile)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    if 'user_id' not in session:
        flash('Please login to apply for jobs', 'error')
        return redirect(url_for('login'))

    job = Job.query.get_or_404(job_id)
    user = User.query.get(session['user_id'])

    # Check if already applied
    existing_application = JobApplication.query.filter_by(job_id=job_id, applicant_id=user.id).first()
    if existing_application:
        flash('You have already applied for this job', 'info')
        return redirect(url_for('job_details', job_id=job_id))

    if request.method == 'POST':
        cover_letter = request.form.get('cover_letter')

        # Create application
        application = JobApplication(
            job_id=job_id,
            applicant_id=user.id,
            cover_letter=cover_letter
        )
        db.session.add(application)
        db.session.commit()

        flash('Application submitted successfully!', 'success')
        return redirect(url_for('account'))

    return render_template('apply_job.html', job=job, user=user)

# API endpoints for AJAX requests
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('pass')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['user_name'] = user.name
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('pass')
    confirm_password = data.get('c_pass')

    if password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'})

    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Email already registered'})

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Registration successful'})

# API for saving/unsaving jobs
@app.route('/api/save-job/<int:job_id>', methods=['POST'])
def save_job(job_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})

    user_id = session['user_id']
    existing_save = SavedJob.query.filter_by(user_id=user_id, job_id=job_id).first()

    if existing_save:
        # Unsave
        db.session.delete(existing_save)
        db.session.commit()
        return jsonify({'success': True, 'saved': False, 'message': 'Job removed from saved jobs'})
    else:
        # Save
        saved_job = SavedJob(user_id=user_id, job_id=job_id)
        db.session.add(saved_job)
        db.session.commit()
        return jsonify({'success': True, 'saved': True, 'message': 'Job saved successfully'})

# Recommendation algorithm
def get_recommended_jobs(user_id, limit=5):
    user = User.query.get(user_id)
    profile = UserProfile.query.filter_by(user_id=user_id).first()

    if not profile or not profile.skills:
        # If no profile or skills, return recent jobs
        return Job.query.order_by(Job.created_at.desc()).limit(limit).all()

    # Get user's skills
    user_skills = [skill.strip().lower() for skill in profile.skills.split(',')]

    # Get jobs user has applied to
    applied_job_ids = [app.job_id for app in JobApplication.query.filter_by(applicant_id=user_id).all()]

    # Score jobs based on skill match
    jobs = Job.query.all()
    scored_jobs = []

    for job in jobs:
        if job.id in applied_job_ids:
            continue  # Skip already applied jobs

        score = 0
        job_text = (job.description + ' ' + (job.requirements or '')).lower()

        for skill in user_skills:
            if skill in job_text:
                score += 1

        if score > 0:
            scored_jobs.append((job, score))

    # Sort by score descending, then by date
    scored_jobs.sort(key=lambda x: (-x[1], x[0].created_at), reverse=True)

    return [job for job, score in scored_jobs[:limit]]

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return render_template('register.html')

    user_id = session['user_id']
    recommended_jobs = get_recommended_jobs(user_id)

    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')

        # Query jobs based on search
        query = Job.query
        if title:
            query = query.filter(Job.title.ilike(f'%{title}%'))
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))

        jobs_list = query.order_by(Job.created_at.desc()).all()
        return render_template('home.html', jobs=jobs_list, recommended_jobs=recommended_jobs)

    return render_template('home.html', recommended_jobs=recommended_jobs)

# Messaging routes
@app.route('/messages')
def messages():
    if 'user_id' not in session:
        flash('Please login to access messages', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Get all conversations for the user
    conversations = db.session.query(Conversation).filter(
        db.or_(Conversation.user1_id == user_id, Conversation.user2_id == user_id)
    ).order_by(Conversation.last_message_at.desc()).all()

    # Get unread message count
    unread_count = Message.query.filter_by(receiver_id=user_id, is_read=False).count()

    return render_template('messages.html', conversations=conversations, unread_count=unread_count)

@app.route('/conversation/<int:other_user_id>', methods=['GET', 'POST'])
def conversation(other_user_id):
    if 'user_id' not in session:
        flash('Please login to access messages', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Check if other user exists
    other_user = User.query.get_or_404(other_user_id)

    # Find or create conversation
    conversation = Conversation.query.filter(
        db.or_(
            db.and_(Conversation.user1_id == user_id, Conversation.user2_id == other_user_id),
            db.and_(Conversation.user1_id == other_user_id, Conversation.user2_id == user_id)
        )
    ).first()

    if not conversation:
        conversation = Conversation(user1_id=user_id, user2_id=other_user_id)
        db.session.add(conversation)
        db.session.commit()

    if request.method == 'POST':
        subject = request.form.get('subject')
        content = request.form.get('content')

        if not content:
            flash('Message content is required', 'error')
            return redirect(url_for('conversation', other_user_id=other_user_id))

        # Create message
        message = Message(
            sender_id=user_id,
            receiver_id=other_user_id,
            subject=subject,
            content=content
        )
        db.session.add(message)

        # Update conversation timestamp
        conversation.last_message_at = db.func.current_timestamp()
        db.session.commit()

        flash('Message sent successfully!', 'success')
        return redirect(url_for('conversation', other_user_id=other_user_id))

    # Get all messages in this conversation
    message_list = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).order_by(Message.sent_at.asc()).all()

    # Mark messages as read
    Message.query.filter_by(sender_id=other_user_id, receiver_id=user_id, is_read=False).update({'is_read': True})
    db.session.commit()

    return render_template('conversation.html', conversation=conversation, messages=message_list, other_user=other_user)

@app.route('/send-message/<int:receiver_id>', methods=['GET', 'POST'])
def send_message(receiver_id):
    if 'user_id' not in session:
        flash('Please login to send messages', 'error')
        return redirect(url_for('login'))

    sender_id = session['user_id']
    receiver = User.query.get_or_404(receiver_id)

    if request.method == 'POST':
        subject = request.form.get('subject')
        content = request.form.get('content')

        if not content:
            flash('Message content is required', 'error')
            return redirect(url_for('send_message', receiver_id=receiver_id))

        # Create message
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            subject=subject,
            content=content
        )
        db.session.add(message)

        # Find or create conversation
        conversation = Conversation.query.filter(
            db.or_(
                db.and_(Conversation.user1_id == sender_id, Conversation.user2_id == receiver_id),
                db.and_(Conversation.user1_id == receiver_id, Conversation.user2_id == sender_id)
            )
        ).first()

        if not conversation:
            conversation = Conversation(user1_id=sender_id, user2_id=receiver_id)
            db.session.add(conversation)

        # Update conversation timestamp
        conversation.last_message_at = db.func.current_timestamp()
        db.session.commit()

        flash('Message sent successfully!', 'success')
        return redirect(url_for('conversation', other_user_id=receiver_id))

    return render_template('send_message.html', receiver=receiver)

# Company routes
@app.route('/company/<int:company_id>')
def company_profile(company_id):
    company = Company.query.get_or_404(company_id)
    reviews = CompanyReview.query.filter_by(company_id=company_id).order_by(CompanyReview.created_at.desc()).all()

    # Calculate average rating
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        avg_rating = 0

    return render_template('company.html', company=company, reviews=reviews, avg_rating=avg_rating)

@app.route('/review-company/<int:company_id>', methods=['GET', 'POST'])
def review_company(company_id):
    if 'user_id' not in session:
        flash('Please login to leave a review', 'error')
        return redirect(url_for('login'))

    company = Company.query.get_or_404(company_id)
    user_id = session['user_id']

    # Check if user already reviewed
    existing_review = CompanyReview.query.filter_by(user_id=user_id, company_id=company_id).first()
    if existing_review:
        flash('You have already reviewed this company', 'info')
        return redirect(url_for('company_profile', company_id=company_id))

    if request.method == 'POST':
        rating = int(request.form.get('rating'))
        review_text = request.form.get('review_text')

        if not (1 <= rating <= 5):
            flash('Invalid rating', 'error')
            return redirect(url_for('review_company', company_id=company_id))

        review = CompanyReview(
            user_id=user_id,
            company_id=company_id,
            rating=rating,
            review_text=review_text
        )
        db.session.add(review)
        db.session.commit()

        flash('Review submitted successfully!', 'success')
        return redirect(url_for('company_profile', company_id=company_id))

    return render_template('review_company.html', company=company)

@app.route('/employer-dashboard')
def employer_dashboard():
    if 'user_id' not in session:
        flash('Please login to access dashboard', 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    # Get jobs posted by user
    jobs = Job.query.filter_by(posted_by=user_id).order_by(Job.created_at.desc()).all()

    # Get applications for user's jobs
    job_ids = [job.id for job in jobs]
    applications = JobApplication.query.filter(JobApplication.job_id.in_(job_ids)).order_by(JobApplication.applied_at.desc()).all()

    # Analytics
    total_jobs = len(jobs)
    total_applications = len(applications)
    pending_applications = len([app for app in applications if app.status == 'pending'])
    accepted_applications = len([app for app in applications if app.status == 'accepted'])

    return render_template('employer_dashboard.html', user=user, jobs=jobs, applications=applications,
                         total_jobs=total_jobs, total_applications=total_applications,
                         pending_applications=pending_applications, accepted_applications=accepted_applications)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
