CREATE TABLE users (
  -- pk
  pk BIGSERIAL PRIMARY KEY,
-- - id
  id VARCHAR(100) UNIQUE NOT NULL,
-- - password_hash
  password_hash VARCHAR(255) NOT NULL,
-- - role
  role VARCHAR(30) NOT NULL DEFAULT 'USER' CHECK (role IN ('ADMIN', 'USER')),
-- - name
  name VARCHAR(30) NOT NULL,
-- - email
  email VARCHAR(255) NOT NULL UNIQUE,
-- - address
  address VARCHAR(255) NOT NULL,
-- - created_at
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
-- - updated_at
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
-- - deleted_at
  deleted_at TIMESTAMPTZ NULL
);

CREATE TABLE items (
-- - pk
  pk BIGSERIAL PRIMARY KEY,
-- - name
  name VARCHAR(50) NOT NULL,
-- - stock
  stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
-- - price
  price INT NOT NULL DEFAULT 0 CHECK (price >= 0),
-- - image_link
  image_link TEXT,
-- - created_at
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
-- - pk
  pk BIGSERIAL PRIMARY KEY,
-- - user_pk
  user_pk BIGINT NOT NULL REFERENCES users(pk),
-- - status
  status VARCHAR(100) NOT NULL CHECK 
              (status IN ('PENDING_PAYMENT', 'PAID', 'SHIPPING', 
                'SUCCESS', 'FAILED', 'CANCELED', 'EXPIRED')),
-- - recipient_name
  recipient_name VARCHAR(50) NOT NULL,
-- - recipient_email
  recipient_email VARCHAR(255) NOT NULL,
-- - shipping_address
  shipping_address VARCHAR(255) NOT NULL,
-- - total_price
  total_price INTEGER NOT NULL DEFAULT 0 CHECK (total_price >= 0),
-- - created_at
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
-- - updated_at
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
-- - pk
  pk BIGSERIAL PRIMARY KEY,
-- - order_pk
  order_pk BIGINT NOT NULL REFERENCES orders(pk) ON DELETE CASCADE,
-- - item_pk
  item_pk BIGINT NOT NULL REFERENCES items(pk) ON DELETE RESTRICT,
-- - item_name
  item_name VARCHAR(50) NOT NULL,
-- - item_price
  item_price INT NOT NULL DEFAULT 0 CHECK (item_price >= 0),
-- - quantity
  quantity INT NOT NULL CHECK (quantity >= 1),
  -- - total_price
  total_price INT NOT NULL DEFAULT 0 CHECK (total_price >= 0)
);

CREATE TABLE payments (
-- - pk
  pk BIGSERIAL PRIMARY KEY,
-- - order_pk
  order_pk BIGINT NOT NULL REFERENCES orders(pk),
-- - status
  status VARCHAR(50) NOT NULL CHECK (status IN 
      ('IN_PROGRESS', 'PAID', 'FAILED', 'EXPIRED')),
-- - method
  method VARCHAR(255) NOT NULL,
-- - amount
  amount INTEGER NOT NULL DEFAULT 0 CHECK (amount >= 0),
-- - payment_key
  payment_key VARCHAR(255),
-- - paid_at
  paid_at TIMESTAMPTZ NULL,
-- - created_at
  created_at TIMESTAMPTZ DEFAULT NOW()
);