E-Library – Book Recommendation System (BRS)
🔍 Project Overview:
The Book Recommendation System is a personalized E-Library web application that enhances the reading experience by offering intelligent book suggestions. Built using Flask, Machine Learning, and SQLite, it supports secure user access, efficient data handling, and dynamic content delivery. The system combines popularity-based and collaborative filtering algorithms to provide accurate and relevant book recommendations.

💻 Key Features:
✅ User Authentication: Secure user registration and login system using Flask.
✅ Book Recommendation Engine:
 🔸 Collaborative Filtering – Recommends books based on user ratings and preferences.
 🔸 Popularity-Based Filtering – Displays top 50 most popular books based on aggregate user ratings.
✅ Book Ratings System: Users can rate books from 1 to 5 stars, which influences recommendations.
✅ Search & Browse: Search books by title, author, or genre.
✅ Dynamic Book Display: Real-time display of book covers, titles, genres, and ratings.
✅ Admin Functions: Add or manage book entries and monitor user activity.

🔧 Technologies Used:
🔹 Backend: Python (Flask) for server-side logic and routing
🔹 Frontend: HTML and CSS for responsive and interactive UI
🔹 Database: SQLite for storing user data, book records, and ratings
🔹 Machine Learning:
 ▪ Scikit-learn for implementing collaborative filtering
 ▪ Popularity-based logic for listing top 50 books by rating count and score

📜 Data Validations:
✅ User Inputs: Validations for email, password, and secure login
✅ Book Entries: Prevents duplicate or incomplete book data
✅ Ratings: Accepts only valid numerical ratings (1–5)

📜 How It Works:
🔹 Register/Login: Users authenticate to access recommendations
🔹 Browse Books: Search or scroll through books by popularity or category
🔹 Top 50 Books: Lists books with highest ratings and review counts
🔹 Personalized Suggestions: Uses collaborative filtering based on past user behavior
🔹 Rate Books: User feedback improves future recommendation accuracy
🔹 Admin Panel: Manage book inventory and oversee system performance
