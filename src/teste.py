from datetime import datetime 

timestamp = datetime.now().timestamp()         

"""
No código adicionei esse timestamp() mas deu erro 
por problema de compatibilidade de dados
"""

timestamp2 = datetime.now()


print(f"Timestamp atual: {timestamp}")
print(f"Timestamp atual: {timestamp2}")

print(type(timestamp))  
print(type(timestamp2))  

