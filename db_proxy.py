#!/usr/bin/env python
"""
Local PostgreSQL Proxy Server for IPv6 to IPv4 bridging.

This proxy listens on localhost (IPv4) and forwards connections to the
Supabase PostgreSQL database (IPv6). This allows applications that can't
make IPv6 connections to connect to IPv6-only databases.

Usage:
    python db_proxy.py

The proxy will listen on localhost:5433 and forward to Supabase.
Update your DATABASE_URL to: postgresql://postgres:PASSWORD@localhost:5433/postgres
"""

import os
import socket
import threading
import select
import dns.resolver

# Add PostgreSQL DLL directory on Windows
if os.name == 'nt':
    pg_bin = r"C:\Program Files\PostgreSQL\18\bin"
    if os.path.exists(pg_bin):
        os.add_dll_directory(pg_bin)
        os.environ["PATH"] = pg_bin + os.pathsep + os.environ["PATH"]

# Configuration
LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 5433
REMOTE_HOST = 'db.bqyujhcttkvulrnmhmxn.supabase.co'
REMOTE_PORT = 6543
BUFFER_SIZE = 4096

def resolve_ipv6(hostname):
    """Resolve hostname to IPv6 address using Google DNS."""
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    
    try:
        answers = resolver.resolve(hostname, 'AAAA')
        return str(answers[0])
    except Exception as e:
        print(f"Failed to resolve {hostname}: {e}")
        return None

def forward_data(source, destination, direction):
    """Forward data between source and destination sockets."""
    try:
        while True:
            # Use select to check if data is available
            ready = select.select([source], [], [], 1.0)
            if ready[0]:
                data = source.recv(BUFFER_SIZE)
                if not data:
                    break
                destination.sendall(data)
    except Exception as e:
        print(f"Error forwarding {direction}: {e}")
    finally:
        try:
            source.close()
        except:
            pass
        try:
            destination.close()
        except:
            pass

def handle_client(client_socket, client_address):
    """Handle a client connection by proxying to the remote server."""
    print(f"New connection from {client_address}")
    
    remote_socket = None
    try:
        # Resolve the remote hostname to IPv6
        remote_ip = resolve_ipv6(REMOTE_HOST)
        if not remote_ip:
            print(f"Failed to resolve {REMOTE_HOST}")
            client_socket.close()
            return
        
        print(f"Connecting to {REMOTE_HOST} ({remote_ip}):{REMOTE_PORT}")
        
        # Create IPv6 socket for remote connection
        remote_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        remote_socket.settimeout(30)
        
        # Connect to remote server
        remote_socket.connect((remote_ip, REMOTE_PORT))
        print(f"Connected to remote server")
        
        # Set sockets to non-blocking mode for better performance
        client_socket.setblocking(False)
        remote_socket.setblocking(False)
        
        # Create threads to forward data in both directions
        client_to_remote = threading.Thread(
            target=forward_data,
            args=(client_socket, remote_socket, "client->remote"),
            daemon=True
        )
        remote_to_client = threading.Thread(
            target=forward_data,
            args=(remote_socket, client_socket, "remote->client"),
            daemon=True
        )
        
        client_to_remote.start()
        remote_to_client.start()
        
        # Wait for both threads to complete
        client_to_remote.join()
        remote_to_client.join()
        
        print(f"Connection from {client_address} closed")
        
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        if remote_socket:
            try:
                remote_socket.close()
            except:
                pass
        try:
            client_socket.close()
        except:
            pass

def start_proxy():
    """Start the proxy server."""
    # Create IPv4 socket for local listening
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((LOCAL_HOST, LOCAL_PORT))
        server_socket.listen(5)
        
        print("=" * 60)
        print("PostgreSQL IPv6 Proxy Server")
        print("=" * 60)
        print(f"Listening on: {LOCAL_HOST}:{LOCAL_PORT}")
        print(f"Forwarding to: {REMOTE_HOST}:{REMOTE_PORT}")
        print()
        print("Update your DATABASE_URL to:")
        print(f"postgresql://postgres:PASSWORD@{LOCAL_HOST}:{LOCAL_PORT}/postgres?sslmode=require")
        print()
        print("Press Ctrl+C to stop the proxy")
        print("=" * 60)
        
        while True:
            client_socket, client_address = server_socket.accept()
            
            # Handle each client in a separate thread
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nShutting down proxy server...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()
        print("Proxy server stopped")

if __name__ == "__main__":
    start_proxy()
