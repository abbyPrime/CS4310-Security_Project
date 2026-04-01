-- Production groups (each movie project)
CREATE TABLE productions (
    production_id   SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL
);

-- Users
CREATE TABLE users (
    user_id         SERIAL PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    salt            VARCHAR(255) NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User to production mapping (many-to-many)
CREATE TABLE user_productions (
    user_id         INT NOT NULL,
    production_id   INT NOT NULL,
    PRIMARY KEY (user_id, production_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (production_id) REFERENCES productions(production_id)
);

-- Roles (actors, directors, writers, etc.)
CREATE TABLE roles (
    role_id         SERIAL PRIMARY KEY,
    production_id   INT NOT NULL,
    role_name       VARCHAR(100) NOT NULL,
    FOREIGN KEY (production_id) REFERENCES productions(production_id)
);

-- Assign roles to users (many-to-many)
CREATE TABLE user_roles (
    user_id         INT NOT NULL,
    role_id         INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- Screenplay documents (versioned)
CREATE TABLE screenplays (
    screenplay_id   SERIAL PRIMARY KEY,
    production_id   INT NOT NULL,
    version_number  INT NOT NULL,
    uploaded_by     INT NOT NULL,
    uploaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_revoked      BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (production_id) REFERENCES productions(production_id),
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);

-- Individual lines of a screenplay
CREATE TABLE screenplay_lines (
    line_id             SERIAL PRIMARY KEY,
    screenplay_id       INT NOT NULL,
    line_number         INT NOT NULL,
    encrypted_content   TEXT NOT NULL,
    FOREIGN KEY (screenplay_id) REFERENCES screenplays(screenplay_id)
);

-- Which roles can see which lines
CREATE TABLE line_permissions (
    line_id         INT NOT NULL,
    role_id         INT NOT NULL,
    PRIMARY KEY (line_id, role_id),
    FOREIGN KEY (line_id) REFERENCES screenplay_lines(line_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

-- Comments/annotations on lines
CREATE TABLE comments (
    comment_id      SERIAL PRIMARY KEY,
    line_id         INT NOT NULL,
    user_id         INT NOT NULL,
    content         TEXT NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (line_id) REFERENCES screenplay_lines(line_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Internal messaging system
CREATE TABLE messages (
    message_id      SERIAL PRIMARY KEY,
    sender_id       INT NOT NULL,
    recipient_id    INT NOT NULL,
    content         TEXT NOT NULL,
    sent_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read         BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (recipient_id) REFERENCES users(user_id)
);