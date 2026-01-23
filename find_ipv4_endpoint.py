#!/usr/bin/env python
import os
import sys

# Add PostgreSQL DLL directory on Windows
if os.name == 'nt':
    pg_bin = r"C:\Program Files\PostgreSQL\18\bin"
    if os.path.exists(pg_bin):
        os.add_dll_directory(pg_bin)
        os.environ["PATH"] = pg_bin + os.pathsep + os.environ["PATH"]

import psycopg
import socket

# Configuration
PROJECT_REF = 'bqyujhcttkvulrnmhmxn'
PASSWORD = '1986@olA12=1'
DB_USER = f'postgres.{PROJECT_REF}'
DB_NAME = 'postgres'

# List of potential regions to check
REGIONS = [
    'eu-central-1',
    'eu-west-1',
    'eu-west-2',
    'eu-west-3',
    'us-east-1',
    'us-east-2',
    'us-west-1',
    'us-west-2',
    'ap-southeast-1',
    'ap-northeast-1',
    'ap-south-1',
    'sa-east-1',
    'ca-central-1',
]

def check_endpoint(region):
    host = f'aws-0-{region}.pooler.supabase.com'
    
    try:
        ip = socket.gethostbyname(host)
        print(f"Checking {region} ({host} -> {ip})...")
    except socket.gaierror:
        print(f"Skipping {region} - DNS resolution failed")
        return False

    for port in [6543, 5432]:
        try:
            conn = psycopg.connect(
                host=host,
                port=port,
                user=DB_USER,
                password=PASSWORD,
                dbname=DB_NAME,
                sslmode='require',
                connect_timeout=5
            )
            print(f"[OK] Connected to {region} on port {port}")
            conn.close()
            return host, port
        except psycopg.OperationalError as e:
            error_msg = str(e)
            if "tenant or user not found" in error_msg.lower():
                print(f"  [FAIL] Port {port}: Tenant not found")
            elif "password authentication failed" in error_msg.lower():
                print(f"  [AUTH FAIL] Port {port}: Password failed")
            else:
                print(f"  [FAIL] Port {port}: {error_msg.splitlines()[0]}")
        except Exception as e:
            print(f"  [ERROR] Port {port}: {e}")
            
    return False

def main():
    print(f"Searching for IPv4 endpoint for project {PROJECT_REF}...")
    print("-" * 60)
    
    for region in REGIONS:
        result = check_endpoint(region)
        if result:
            host, port = result
            print("-" * 60)
            print(f"FOUND! Your IPv4-compatible connection string is:")
            print(f"DB_HOST={host}")
            print(f"DB_PORT={port}")
            print(f"DATABASE_URL=postgresql://{DB_USER}:{PASSWORD}@{host}:{port}/{DB_NAME}?sslmode=require")
            return
            
    print("-" * 60)
    print("Could not find a working endpoint. Please check your password or project status.")

if __name__ == "__main__":
    main()
