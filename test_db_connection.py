#!/usr/bin/env python
"""
Test database connection with DNS workaround for Windows.
This script manually resolves the Supabase hostname using Google DNS
and then connects using the resolved IP address.
"""
import os
import psycopg
from urllib.parse import urlparse, urlunparse

# Add PostgreSQL DLL directory on Windows
if os.name == 'nt':
    pg_bin = r"C:\Program Files\PostgreSQL\18\bin"
    if os.path.exists(pg_bin):
        os.add_dll_directory(pg_bin)
        os.environ["PATH"] = pg_bin + os.pathsep + os.environ["PATH"]

def resolve_with_google_dns(hostname):
    """
    Manually resolve hostname using Google DNS (8.8.8.8).
    Returns the resolved IP address.
    """
    import dns.resolver
    
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    
    try:
        # Try IPv4 first
        answers = resolver.resolve(hostname, 'A')
        return str(answers[0])
    except:
        # Fall back to IPv6
        try:
            answers = resolver.resolve(hostname, 'AAAA')
            return f"[{str(answers[0])}]"  # IPv6 needs brackets in connection string
        except Exception as e:
            print(f"DNS resolution failed: {e}")
            raise

def test_connection_with_url(db_url, description):
    """Test a specific database connection URL."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{'='*60}")
    
    try:
        # Parse the URL
        parsed = urlparse(db_url)
        hostname = parsed.hostname
        port = parsed.port
        
        print(f"Hostname: {hostname}")
        print(f"Port: {port}")
        
        # Resolve using Google DNS
        print(f"\nResolving hostname using Google DNS (8.8.8.8)...")
        ip_address = resolve_with_google_dns(hostname)
        print(f"✓ Resolved to: {ip_address}")
        
        # Replace hostname with IP in the connection string
        netloc_with_ip = parsed.netloc.replace(hostname, ip_address)
        modified_url = urlunparse((
            parsed.scheme,
            netloc_with_ip,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
        
        print(f"\nConnecting to database...")
        
        # Connect using the modified URL
        conn = psycopg.connect(modified_url, connect_timeout=30)
        
        print("✓ Connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✓ PostgreSQL version: {version[:80]}...")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {type(e).__name__}: {e}")
        return False

def main():
    """Test multiple connection configurations."""
    print("Database Connection Test")
    print("=" * 60)
    
    # Test configurations
    configs = [
        {
            'url': 'postgresql://postgres:1986%40olA12=1@db.bqyujhcttkvulrnmhmxn.supabase.co:6543/postgres?sslmode=require',
            'description': 'Connection Pooler (port 6543) with SSL'
        },
        {
            'url': 'postgresql://postgres:1986%40olA12=1@db.bqyujhcttkvulrnmhmxn.supabase.co:5432/postgres?sslmode=require',
            'description': 'Direct Connection (port 5432) with SSL'
        },
    ]
    
    results = []
    for config in configs:
        success = test_connection_with_url(config['url'], config['description'])
        results.append((config['description'], success))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for desc, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {desc}")
    
    # Overall result
    if any(success for _, success in results):
        print(f"\n✓ At least one configuration works!")
        return 0
    else:
        print(f"\n✗ All configurations failed!")
        return 1

if __name__ == "__main__":
    exit(main())
