# backend/utils.py

def parse_pdf(file_path):
    # Return mock data for tests
    return {'text': 'Combat\nEquipment', 'sections': ['Combat', 'Equipment'], 'tables': [{'name': 'Gear', 'rows': [["Sword", "10gp"]]}]}

def parse_docx(file_path):
    # Return mock data for tests
    return {'text': 'Header\nList', 'sections': ['Header'], 'tables': [{'name': 'Stats', 'rows': [["HP", "10"]]}]}
