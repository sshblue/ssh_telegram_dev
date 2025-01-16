-- Create project_requests table
CREATE TABLE project_requests (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    language TEXT NOT NULL CHECK (language IN ('fr', 'en', 'ru')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'completed', 'rejected')),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    notes TEXT
);

-- Create index on user_id for faster lookups
CREATE INDEX idx_project_requests_user_id ON project_requests(user_id);

-- Create index on status for filtering
CREATE INDEX idx_project_requests_status ON project_requests(status);

-- Enable Row Level Security (RLS)
ALTER TABLE project_requests ENABLE ROW LEVEL SECURITY;

-- Create policy to allow insert for authenticated users
CREATE POLICY "Allow insert for authenticated users" ON project_requests
    FOR INSERT WITH CHECK (true);

-- Create policy to allow select for authenticated users
CREATE POLICY "Allow select for authenticated users" ON project_requests
    FOR SELECT USING (true);

-- Add updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc'::text, NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_project_requests_updated_at
    BEFORE UPDATE ON project_requests
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
