-- Drop existing tables
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS authors;

-- Create the authors table
CREATE TABLE authors(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_lname TEXT NOT NULL,
    user_fname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert an admin user
INSERT INTO authors (user_lname, user_fname, email, password_hash)
VALUES (
    "admin",
    "admin",
    "admin",
    "admin"
);

-- Create the posts table
CREATE TABLE posts(
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    status TEXT CHECK(status IN ('draft', 'published')) DEFAULT 'draft',
    published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES authors(user_id)
);



-- Insert 10 sample posts
INSERT INTO posts (title, content, status, published_date, user_id)
VALUES
("Welcome Post", "This is the first post on the blog!", "published", CURRENT_TIMESTAMP, 1),
("Upcoming Features", "Here's a sneak peek at upcoming features.", "draft", CURRENT_TIMESTAMP, 1),
("How to Use This Blog", "A guide on how to navigate and use the blog.", "published", CURRENT_TIMESTAMP, 1),
("Development Updates", "Weekly updates from the development team.", "draft", CURRENT_TIMESTAMP, 1),
("Meet the Admin", "An introduction to the admin of this blog.", "published", CURRENT_TIMESTAMP, 1),
("Community Guidelines", "Please follow these guidelines when engaging with others.", "published", CURRENT_TIMESTAMP, 1),
("Feature Requests", "Submit your feature requests here!", "draft", CURRENT_TIMESTAMP, 1),
("Bug Reports", "Found a bug? Let us know!", "draft", CURRENT_TIMESTAMP, 1),
("Blog Customization", "Learn how to customize your blog appearance.", "published", CURRENT_TIMESTAMP, 1),
("Thank You", "A message of appreciation to all users.", "published", CURRENT_TIMESTAMP, 1);

