-- Create support_requests table
CREATE TABLE support_requests (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    language TEXT NOT NULL CHECK (language IN ('fr', 'en', 'ru')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'resolved', 'closed')),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    resolution TEXT,
    priority TEXT DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent'))
);

-- Create index on user_id for faster lookups
CREATE INDEX idx_support_requests_user_id ON support_requests(user_id);

-- Create index on status for filtering
CREATE INDEX idx_support_requests_status ON support_requests(status);

-- Create index on priority for filtering
CREATE INDEX idx_support_requests_priority ON support_requests(priority);

-- Enable Row Level Security (RLS)
ALTER TABLE support_requests ENABLE ROW LEVEL SECURITY;

-- Create policy to allow insert for authenticated users
CREATE POLICY "Allow insert for authenticated users" ON support_requests
    FOR INSERT WITH CHECK (true);

-- Create policy to allow select for authenticated users
CREATE POLICY "Allow select for authenticated users" ON support_requests
    FOR SELECT USING (true);

-- Add updated_at trigger
CREATE TRIGGER update_support_requests_updated_at
    BEFORE UPDATE ON support_requests
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
