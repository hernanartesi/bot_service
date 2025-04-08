CREATE TABLE IF NOT EXISTS users (
  "id" SERIAL PRIMARY KEY,
  "telegram_id" text UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
  "id" SERIAL PRIMARY KEY,
  "user_id" integer NOT NULL REFERENCES users("id"),
  "description" text NOT NULL,
  "amount" money NOT NULL,
  "category" text NOT NULL,
  "added_at" timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS expense_categories (
  "id" SERIAL PRIMARY KEY,
  "name" text UNIQUE NOT NULL
); 