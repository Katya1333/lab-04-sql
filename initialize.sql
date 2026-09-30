CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    posted_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users (user_id, username, email, created_at) VALUES
(1, 'kpribram', 'katya@example.com', '2024-01-10 09:15:00'),
(2, 'jsmith', 'jsmith@example.com', '2024-01-12 14:22:00'),
(3, 'mariah', 'mariah@example.com', '2024-01-15 08:05:00'),
(4, 'tchang', 'tchang@example.com', '2024-01-18 11:47:00'),
(5, 'rpatel', 'rpatel@example.com', '2024-01-20 16:30:00'),
(6, 'lgreen', 'lgreen@example.com', '2024-01-22 10:10:00'),
(7, 'bwayne', 'bwayne@example.com', '2024-01-25 13:55:00'),
(8, 'cliu', 'cliu@example.com', '2024-01-27 09:40:00'),
(9, 'sanders', 'sanders@example.com', '2024-01-29 17:20:00'),
(10, 'nkim', 'nkim@example.com', '2024-02-01 12:00:00');

INSERT INTO posts (post_id, user_id, title, content, posted_at) VALUES
(101, 1, 'First Day of Spring Semester', 'Classes started today and everything feels new.', '2024-02-05 08:30:00'),
(102, 2, 'SQL Tips', 'Remember to always format your queries.', '2024-02-06 10:15:00'),
(103, 3, 'Coffee Review', 'Tried a new café near campus. Amazing espresso.', '2024-02-06 11:00:00'),
(104, 4, 'Gym Routine', 'Started a new workout plan.', '2024-02-07 07:45:00'),
(105, 5, 'Book Recommendation', 'Highly recommend reading “The Pragmatic Programmer”.', '2024-02-07 15:10:00'),
(106, 6, 'Weekend Trip', 'Visited Shenandoah National Park.', '2024-02-08 09:25:00'),
(107, 7, 'Movie Night', 'Watched a classic film yesterday.', '2024-02-08 20:00:00'),
(108, 8, 'Study Tips', 'Pomodoro technique works wonders.', '2024-02-09 14:40:00'),
(109, 9, 'New Coding Project', 'Started building a small Flask app.', '2024-02-10 18:05:00'),
(110, 10, 'Favorite Restaurants', 'Charlottesville has great food spots.', '2024-02-11 12:30:00');