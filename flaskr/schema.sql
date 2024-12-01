-- Drop existing tables
DROP TABLE IF EXISTS postsauthors;
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
    published_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the postsauthors table
CREATE TABLE postsauthors(
    author_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    role TEXT CHECK(role IN ('author', 'co-author')) DEFAULT 'author',
    PRIMARY KEY (author_id, post_id),
    FOREIGN KEY (author_id) REFERENCES authors(user_id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
);

-- Insert 10 sample posts
INSERT INTO posts (title, content, status, published_date)
VALUES
("Welcome Post", "This is the first post on the blog!", "published", CURRENT_TIMESTAMP),
("Upcoming Features", "Here's a sneak peek at upcoming features.", "draft", NULL),
("How to Use This Blog", "A guide on how to navigate and use the blog.", "published", CURRENT_TIMESTAMP),
("Development Updates", "Weekly updates from the development team.", "draft", NULL),
("Meet the Admin", "An introduction to the admin of this blog.", "published", CURRENT_TIMESTAMP),
("Community Guidelines", "Please follow these guidelines when engaging with others.", "published", CURRENT_TIMESTAMP),
("Feature Requests", "Submit your feature requests here!", "draft", NULL),
("Bug Reports", "Found a bug? Let us know!", "draft", NULL),
("Blog Customization", "Learn how to customize your blog appearance.", "published", CURRENT_TIMESTAMP),
("Thank You", "A message of appreciation to all users.", "published", CURRENT_TIMESTAMP);

-- Associate all posts with the admin user
INSERT INTO postsauthors (author_id, post_id, role)
SELECT 1, post_id, 'author' FROM posts;
