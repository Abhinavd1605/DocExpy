"""
SQLite fix for ChromaDB deployment compatibility
This module ensures the correct SQLite version is used before ChromaDB imports
"""

import sys

def fix_sqlite():
    """Fix SQLite3 version compatibility for ChromaDB"""
    try:
        # Try to import pysqlite3 as sqlite3
        import pysqlite3
        sys.modules['sqlite3'] = pysqlite3
        print("✅ SQLite3 fixed using pysqlite3-binary")
        return True
    except ImportError:
        try:
            # Check if system sqlite3 is sufficient
            import sqlite3
            if hasattr(sqlite3, 'sqlite_version_info') and sqlite3.sqlite_version_info >= (3, 35, 0):
                print("✅ System SQLite3 version is sufficient")
                return True
            else:
                print(f"⚠️ System SQLite3 version {sqlite3.sqlite_version} is too old")
                return False
        except ImportError:
            print("❌ No SQLite3 available")
            return False

# Apply the fix when this module is imported
if __name__ != "__main__":
    fix_sqlite() 
