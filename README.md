### 🩸 DonorLink – Smart Blood Donation Network
In many real-world scenarios, during critical blood emergencies, hospitals rely on traditional methods such as contacting other hospitals or blood banks. This process is slow and can reduce a patient’s chances of survival.

To solve this problem, we developed ML Project **DonorLink**, a smart hospital-to-donor connectivity platform.

---

### 🚨 Problem Statement

* Hospitals take time to find matching blood groups
* Communication between hospitals is slow
* Delays in emergencies reduce survival chances

For example, in many hospitals today, if blood is unavailable, they must manually contact multiple sources, which wastes critical time.

---

### 💡 Our Solution

DonorLink connects hospitals directly with registered donors:

* Donors register with their details and blood group
* Hospitals send requests when blood is needed
* The system notifies donors instantly via email

---
### Our Prototype
<img width="1885" height="872" alt="Screenshot (87)" src="https://github.com/user-attachments/assets/82deb16f-6046-48d8-9213-a202e63ee5b8" />



### ⚙️ Smart Matching Algorithm

Our system filters donors intelligently:

* From 100 donors → selects top 5 best matches
* Based on:

  * Blood group
  * Location
  * Availability

---

### 🚑 Fast Response

* Selected donors are notified immediately
* Ambulance support can be triggered
* Faster response increases survival probability

---

### 📈 Impact

* Reduces response time
* Improves emergency handling
* Increases patient survival chances

---

## 🛠️ Tech Stack

* Backend: Django
* Frontend: React (running on localhost:3000)
* Database: SQLite (default)

---

## ▶️ How to Run the Project

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/danushkaviti-tech/Donor-link.git
cd Donor-link
```

---

### 🔹 2. Backend Setup (Django)

Make sure Python is installed.

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start Django server:

```bash
python manage.py runserver
```

👉 Backend will run at:

```
http://127.0.0.1:8000/
```

---

### 🔹 3. Frontend Setup (React – localhost:3000)

Go to frontend folder (if separate):

```bash
cd frontend
npm install
npm start
```

👉 Frontend will run at:

```
http://localhost:3000/
```

---

### 🔹 4. Connect Frontend & Backend

Make sure:

* Django API is running on port 8000
* React app calls backend APIs correctly

---

## 📌 Features

* Donor registration
* Hospital request system
* Email notifications
* Smart donor filtering
* Fast emergency response

---

## 🎯 Future Improvements

* Real-time notifications (SMS / App alerts)
* GPS-based donor tracking
* Mobile application
* Integration with hospitals nationwide

---

## 🤝 Contributing

Feel free to fork and contribute to improve the system.

---

## 📢 Conclusion

DonorLink aims to save lives by reducing delays in blood availability through smart technology and efficient donor-hospital communication.

---
