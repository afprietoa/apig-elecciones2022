import requests

security_url = "http://127.0.0.1:8080"
headers = {"Content-Type": "application/json; charset=utf-8"}

# Create Roles
roles = [
    {"name": "Administrador", "description": "El que gestiona los roles en la plaforma."},
    {"name": "Jurado", "description": "El que gestiona los resultados de los sufragantes."},
    {"name": "Ciudadano", "description": "El que emite su voto durante la elección."}
]
url = f'{security_url}/rol/insert'
for rol in roles:
    response = requests.post(url, headers=headers, json=rol)
    print(response.json())
    if rol.get('name') == "Administrador":
        admin = response.json()
print("="*30)

# Create Permission
modules = ['table', 'political_party', 'candidate', 'vote', 'user', 'rol']
endpoints = [('s', 'GET'), ('/?', 'GET'), ('/insert', 'POST'), ('/update/?', 'PUT'), ('/delete/?', 'DELETE')]
url = f'{security_url}/permission/insert'
for module in modules:
    for endpoint, method in endpoints:
        permission_url = f'/{module}{endpoint}'
        body = {
            "url": permission_url,
            "method": method
        }
        response = requests.post(url, headers=headers, json=body)
        print(response.json())
        permission = response.json()
        url_relation = f'{security_url}/rol/update/{admin.get("idRol")}/add_permission/{permission.get("idPermission")}'
        print(url_relation)
        response = requests.put(url_relation, headers=headers)
