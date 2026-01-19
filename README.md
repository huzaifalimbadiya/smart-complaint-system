# Smart Complaint Management System - README

## 🎯 Project Overview

A production-ready web application for managing public complaints and service requests with **AI-powered automatic classification**.

### Key Highlights
- ✅ **AI Classification** using TF-IDF + Naive Bayes
- ✅ **User & Admin Dashboards** with role-based access
- ✅ **Real-time Status Tracking**
- ✅ **Analytics & Reporting** (Excel, PDF exports)
- ✅ **Professional UI** with Bootstrap 5
- ✅ **Complete Django MVT Architecture**

## 🚀 Quick Start

```powershell
# 1. Navigate to project
cd "e:\AI-web app\Smart_Complaint_Management_System"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create categories
python manage.py populate_categories

# 5. Create admin user
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

## 📖 Full Documentation

See **SETUP_GUIDE.md** for:
- Detailed installation steps
- Testing scenarios
- AI classifier testing
- Project structure
- Interview talking points
- Troubleshooting

## 🧠 AI Classification

The system automatically categorizes complaints into:
1. **Electricity** - Power outages, street lights, transformers
2. **Water Supply** - Pipeline leaks, sewage, water quality
3. **Road & Transport** - Potholes, traffic signals, footpaths
4. **Cleanliness** - Garbage collection, sanitation
5. **Noise** - Loud music, construction noise
6. **Other** - General complaints

**Technology:** TF-IDF Vectorization + Multinomial Naive Bayes

## 👥 User Roles

### Normal User
- Register & Login
- Submit complaints with optional images
- AI auto-categorizes complaint
- Track complaint status
- View admin responses

### Admin
- Dashboard with statistics & charts
- Manage all complaints
- Filter, search, sort complaints
- Update status & category
- Add responses to users
- Export reports (Excel/PDF)

## 📊 Features

### User Features
- ✅ Secure authentication
- ✅ Complaint submission with image upload
- ✅ AI category prediction
- ✅ Personal complaint history
- ✅ Status tracking (Pending → In Progress → Resolved/Rejected)

### Admin Features
- ✅ Analytics dashboard with Chart.js
- ✅ Category distribution pie chart
- ✅ Monthly trend line chart
- ✅ Advanced search & filters
- ✅ Status management
- ✅ AI category correction
- ✅ Admin responses (visible to users)
- ✅ Internal notes (admin only)
- ✅ Excel/PDF export with filters

## 🛠️ Technology Stack

- **Backend:** Django 4.2.7
- **Database:** SQLite (easily upgradable to PostgreSQL)
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **AI/ML:** scikit-learn, pandas, nltk
- **Charts:** Chart.js
- **Reports:** openpyxl, reportlab
- **Icons:** Bootstrap Icons

## 📁 Project Structure

```
Smart_Complaint_Management_System/
├── config/          # Django settings
├── accounts/        # User authentication
├── complaints/      # Complaint management
├── dashboard/       # Admin interface
├── ml_module/       # AI classifier
├── templates/       # HTML templates
├── static/          # CSS, JS, images
└── media/           # User uploads
```

## 🎓 For Interviews

**Key Points:**
- **Problem:** Traditional complaint systems lack tracking, analytics, and automation
- **Solution:** Web-based platform with AI classification and comprehensive dashboards
- **AI/ML:** Real-world NLP using TF-IDF and Naive Bayes with 60 training samples
- **Architecture:** Clean MVT pattern, modular apps, role-based access
- **Scalability:** Can add REST API, mobile app, email notifications, advanced ML
- **Security:** CSRF, login_required decorators, password validation
- **Data Viz:** Chart.js pie and line charts for actionable insights

## 📝 Access URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Register | http://127.0.0.1:8000/accounts/register/ |
| Login | http://127.0.0.1:8000/accounts/login/ |
| Submit Complaint | http://127.0.0.1:8000/complaints/submit/ |
| My Complaints | http://127.0.0.1:8000/complaints/my-complaints/ |
| Admin Dashboard | http://127.0.0.1:8000/dashboard/ |
| Manage Complaints | http://127.0.0.1:8000/dashboard/complaints/ |

## 🧪 Test the AI

```python
python manage.py shell

from ml_module.classifier import predict_category

# Test
category, confidence = predict_category("No electricity in our area")
print(f"Category: {category}, Confidence: {confidence:.0%}")
```

## 🔮 Future Enhancements

- Email notifications
- REST API for mobile apps
- Geolocation with maps
- Advanced ML (BERT, transformers)
- Multi-language support
- Sentiment analysis
- Real-time notifications

## 📧 Contact

**Developer:** [Your Name]
**Email:** [your.email@example.com]
**GitHub:** [your-github]

---

**⭐ If you find this project helpful for learning, please star it!**
