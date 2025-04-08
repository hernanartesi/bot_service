import sys
import os

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")

print("\nTrying to import app modules...")
try:
    import app
    print("✅ Successfully imported app")
    
    import app.main
    print("✅ Successfully imported app.main")
    
    import app.api
    print("✅ Successfully imported app.api")
    
    import app.api.api
    print("✅ Successfully imported app.api.api")
    
    import app.api.routes
    print("✅ Successfully imported app.api.routes")
    
    import app.core
    print("✅ Successfully imported app.core")
    
    import app.core.config
    print("✅ Successfully imported app.core.config")
    
    import app.services
    print("✅ Successfully imported app.services")
    
    import app.schemas
    print("✅ Successfully imported app.schemas")
    
except Exception as e:
    print(f"❌ Import error: {e}") 