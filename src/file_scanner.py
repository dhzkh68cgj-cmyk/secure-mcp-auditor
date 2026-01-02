#!/usr/bin/env python3
"""
File Scanner Script
Scans the current directory and displays file names with their sizes.
"""

import os
from pathlib import Path


def format_size(size_bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def scan_directory(directory_path='.'):
    """Scan directory and print file names with sizes."""
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Error: Directory '{directory_path}' does not exist.")
        return
    
    if not directory.is_dir():
        print(f"Error: '{directory_path}' is not a directory.")
        return
    
    print(f"\n{'='*60}")
    print(f"Scanning: {directory.absolute()}")
    print(f"{'='*60}\n")
    
    # Get all files in the directory
    files = [f for f in directory.iterdir() if f.is_file()]
    
    if not files:
        print("No files found in this directory.")
        return
    
    # Sort files by name
    files.sort(key=lambda x: x.name.lower())
    
    # Print header
    print(f"{'File Name':<40} {'Size':>15}")
    print(f"{'-'*40} {'-'*15}")
    
    total_size = 0
    
    # Print each file with its size
    for file in files:
        try:
            size = file.stat().st_size
            total_size += size
            print(f"{file.name:<40} {format_size(size):>15}")
        except Exception as e:
            print(f"{file.name:<40} {'Error':>15}")
    
    print(f"{'-'*40} {'-'*15}")
    print(f"{'Total:':<40} {format_size(total_size):>15}")
    print(f"\nTotal files: {len(files)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    scan_directory()
