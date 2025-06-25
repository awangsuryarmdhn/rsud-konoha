# utils.py (opsional, untuk kode tambahan/umum)
import random
from datetime import datetime

def generate_nomor_rm():
    prefix = datetime.now().strftime('%Y%m%d')
    suffix = random.randint(1000, 9999)
    return f"RM{prefix}{suffix}"
