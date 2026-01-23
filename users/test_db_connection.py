# test_db_connection.py
import socket
import psycopg2

print("Testing database connection...")

# 1. First, test DNS resolution
print("\n1. Testing DNS resolution:")
try:
    # Force IPv4
    original_getaddrinfo = socket.getaddrinfo
    def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
        return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    socket.getaddrinfo = getaddrinfo_ipv4
    
    addresses = socket.getaddrinfo("db.bqyujhcttkvulrnmhmxn.supabase.co", 5432)
    print(f"   Resolved to: {addresses[0][4][0] if addresses else 'No addresses'}")
except Exception as e:
    print(f"   DNS Error: {e}")

# 2. Test database connection
print("\n2. Testing database connection:")
try:
    # Replace with your actual credentials
    conn = psycopg2.connect(
        host="db.bqyujhcttkvulrnmhmxn.supabase.co",
        port=5432,
        database="postgres",  # Default Supabase database
        user="postgres",      # Your Supabase username
        password="YOUR_PASSWORD_HERE",  # Your Supabase password
        connect_timeout=10,
        sslmode="require"
    )
    print("   ✅ SUCCESS: Connected to database!")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"   Database version: {version[0]}")
    
    cursor.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"   ❌ FAILED: {e}")
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print("\nTest complete!")