import ast

async def validate_patch(files: list) -> dict:
    """
    files: [{"path": "...", "content": "..."}]
    """
    status = "PASS"
    notes = []
    checked_files = []
    
    for f in files:
        path = f.get("path", "")
        content = f.get("content", "")
        
        if path.endswith(".py"):
            checked_files.append(path)
            try:
                ast.parse(content)
            except SyntaxError as e:
                status = "FAIL"
                notes.append(f"Syntax error in {path}: {e}")
            except Exception as e:
                status = "FAIL"
                notes.append(f"Error parsing {path}: {e}")
                
    if not checked_files:
        notes.append("No Python files found to validate.")
        
    return {
        "status": status,
        "checked_files": checked_files,
        "notes": notes
    }
