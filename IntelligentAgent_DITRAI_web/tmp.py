from main import app,db,bcrypt

password=bcrypt.generate_password_hash('jennie',10).decode('utf-8')
print(password)
