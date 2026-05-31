CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS roles (
    id          SERIAL PRIMARY KEY
    name        VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
) ;

CREATE TABLE IF NOT EXISTS users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid()
    username      VARCHAR(100) UNIQUE NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id       INTEGER NOT NULL REFERENCES roles(id),
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPZ NOT NULL DEFAULT NOW()
    updated_at    TIMESTAMPZ NOT NULL DEFAULT NOW()
    last_login_at  TIMESTAMPZ 
) ;

-- TARGETS
CREATE TABLE IF NOT EXISTS targets (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id      UUID NOT NULL REFERENCES users(id),
    name          VARCHAR(200) NOT NULL,
    endpoint_url  TEXT NOT NULL,
    auth_type     VARCHAR(50) NOT NULL DEFAULT 'none',
    auth_secret   BYTEA,
    headers       JSONB NOT NULL DEFAULT '{}',
    timeout_sec   INTEGER NOT NULL DEFAULT 30,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- SCANS
CREATE TABLE IF NOT EXISTS scans (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_id       UUID NOT NULL REFERENCES targets(id),
    initiated_by    UUID NOT NULL REFERENCES users(id),
    status          VARCHAR(20) NOT NULL DEFAULT 'pending',
    overall_score   NUMERIC(5,2),
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- SCAN RESULTS
CREATE TABLE IF NOT EXISTS scan_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id         UUID NOT NULL REFERENCES scans(id),
    verdict         VARCHAR(20) NOT NULL,
    severity        VARCHAR(20),
    risk_score      NUMERIC(5,2),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- REPORTS
CREATE TABLE IF NOT EXISTS reports (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id      UUID NOT NULL REFERENCES scans(id),
    generated_by UUID NOT NULL REFERENCES users(id),
    format       VARCHAR(10) NOT NULL,
    file_path    TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- SEED DEFAULT ROLES
INSERT INTO roles (name, description) VALUES
    ('admin',   'Full system access'),
    ('analyst', 'Can run scans and view reports'),
    ('viewer',  'Read-only access to results')
ON CONFLICT (name) DO NOTHING;