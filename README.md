# JU Exam Office Management System
---
## Team Name: JU_Hexagon
*Batch 49, Department of Computer Science & Engineering, Jahangirnagar University, Bangladesh*

## Team Members:
- **Mohammed Tamjid Islam** 
- **Mahfuz Anam** 
- **Kamrul Hasan Nahid** 
- **Farhan Ahmed Onu** 
- **Suraiya Mahmuda** 
- **Abdullah Al Mamun**
## Intoduction

Our Project is Exam Office Management System. We iniitially made the project predominantly for Jahangirnagar University.The primary purpose of the product is to improve the accuracy, efficiency, and transparency of examrelated processes. The software serves as a centralized platform for the exam office to manage multiple tasks,

## Features
#### Exam Office
- Creating and Publishing Exam Schedules,
- Publish Result,
- Manage Exam Materials,
- Manage Answer Scripts,
- Manage Teacher Remuneration,
- Approving special accommodations,
Additionally, it provides students with a seamless interface to:
- Access their results
#### Students
- Register for Upcoming Exams,
- View Results,
- Apply for Marksheets and Certificates

  


## Installation
Following should be installed correctly. They are written in requirements.txt file

-Django==5.0.6
-pytest==7.2.0
-Sphinx==8.0.2


### Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone https://github.com/TamjidIslam99/Ju-Exam-Office-Management-System.git
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run database migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Create a superuser** (optional, for accessing the Django admin panel):
    ```bash
    python manage.py createsuperuser
    ```

5. **Start the server**:
    ```bash
    python manage.py runserver
    ```

6. Open your web browser and go to `http://127.0.0.1:8000/`.


