# Chrystian's Tavern
---


Geek shop system with product sales, client registration, orders saving and  mounth signatures for bonus points and products.

**URL= https://chrystians-tarvern.herokuapp.com**

## Features
- Create/Update/Delete/Search Products
- Register/Update/Delete/Search Clients
- Generate/Search product orders
- Signature services for clients


📌 Routes and Endpoints


- Route Products **(/products)**
    - **POST** - () → Create new Product(s)
    - **GET** - () → Search for  all Products
    - **GET** - (/product_id) → Search for one Product
    - **PATCH** - (/product_id) →  Update Product
    - **DELETE** - (/product_id) → Delete Product
    

- Route Clients **(/clients)**
    - **POST** - () → Create/Register Clients
    - **POST** - (client_id>/checkout) → Register sale for one Client
    - **GET** - () → Search for all clients
    - **GET** - (/client_id) → Search for one Client
    - **PATCH** - (/client_id) → Update Client
    - **DELETE** - (/client_id) → Delete Client


- Rota para a Box **(/boxes)**
    - **POST** - () → Create box(es)
    - **GET** - () → Search boxes
    - **GET** - (/box_flag) → Search for one box
    - **PATCH** - (/box_flag) → Update box
    - **DELETE** - (box_flag) → Delete box


# Product Route

- **POST - 201** - (https://chrystians-tarvern.herokuapp.com/products)

**REQUEST**
```json

{
	"name": "Varinha do Harry Potter",
	"price": 1050, #MUST BE INTEGER
	"category": "Filme",
	"available_amount": 5 
}
```
**RESPONSE**
```json

{
	"id": 2
	"name": "Varinha do Harry Potter",
	"price": 1050, 
	"category": "Filme",
	"available_amount": 5,
	"flag": "Gold" 
}
```

- **GET - 200** - (https://chrystians-tarvern.herokuapp.com/products)

**RESPONSE**
```json
[
	{
		"id": 2
		"name": "Varinha do Harry Potter",
		"price": 1050
		"category": "Filme"
		"available_amount": 5 
		"flag": "Gold" 
	},
	{
		"id": 8
		"name": "Capa de invisibilidade",
		"price": 2050
		"category": "Filme"
		"available_amount": 2
		"flag": "Gold"
	},
	{
		"id": 3
		"name": "Chapéu do Harry Potter",
		"price": 3050, 
		"category": "Filme",
		"available_amount": 10 
		"flag": "Gold"
	}
]
```

- **GET - 200** - (https://chrystians-tarvern.herokuapp.com/products/<product_id>) 

**RESPONSE**
```json
{
	"id": 2
	"name": "Varinha do Harry Potter",
	"price": 1050, 
	"category": "Filme", 
	"available_amount": 5
	"flag": "Gold"
}

```

- **PATCH 200** - (https://chrystians-tarvern.herokuapp.com/products/<product_id>)

**REQUEST**
```json
{
	"name": "Varinha do Harry Potter",
	"price": 1050, 
	"category": "Filme",
	"available_amount": 5
}
```
**CAN UPDATE ONE OR MORE ATRIBUTES**
CAN **NOT** UPDATE A FLAG

**RESPONSE**
```json
{
	"id": 2,
	"name": "Varinha do Rony",
	"price": 1050, 
	"category": "Filme", 
	"available_amount": 2 
}
```

- **DELETE - 200** - (https://chrystians-tarvern.herokuapp.com/products/<product_id>) 
```json
No content
```
___

# Route Clients

- **POST - 201** - (https://chrystians-tarvern.herokuapp.com/clients) 

**REQUEST**
```json
{
	"name": "Rodriguinho",
	"email": "rodrigo@mail.com",
	"cpf": "39567513254", "234.543.678-12"
	"box_flag": "Silver", #OPTIONAL
}
```
- box_flag is optional


**RESPONSE**
```json
{
	"id": 23,
	"name": "Rodriguinho",
	"email": "rodrigo@mail.com",
	"total_points": 0,
	"cpf": "39567513254", "234.543.678-12"
	"box_flag": "Silver", (OPCIONAL, nullable=True)
}
```

- **POST - 201** - (https://chrystians-tarvern.herokuapp.com/<client_id>/checkout)

**REQUEST**
```json
{
	"products":
		[
			{
				"id_produto":23,
				 "quantity": 2
			},
			{
				"id_produto":420,
				 "quantity": 9
			}
		]	
}
```
**RESPOSTA**
```json
{
"products":
	[
		{
			"id_produto":23,
			"name": "Capa do Harry Potter",
			"quantity": 2,
			"unity_price": 2800
		},
		{
			"id_produto":420,
			"name": "Varinha do Harry Potter",
			"quantity": 9,
			"unity_price": 25000
		}
	]
	"total_price": 27800
	"client_id": cliente_id
}
```

- **GET** - (https://chrystians-tarvern.herokuapp.com/clients) 

**RESPONSE**
```json
[
	{
		"id": 23,
		"name": "Rodriguinho",
		"email": "rodrigo@mail.com",
		"total_points": 0,
		"cpf": "23454367812", "234.543.678-12"
		"box_flag": "Bronze"
	},
	{
		"id": 245,
		"name": "Guilherme",
		"email": "guilherminho@mail.com",
		"total_points": 0,
		"cpf": "39567513254", "395.675.132-54"
		"box_flag": "Silver",
	},
	{
		"id": 33,
		"name": "Micael",
		"email": "mickey@mail.com",
		"total_points": 0,
		"cpf": "23245617554", "232.456.175-54"
		"box_flag": null,
	},
	{
		"id": 23,
		"name": "Isabella",
		"email": "bebella@mail.com",
		"total_points": 0,
		"cpf": "25315678945", "253.156.789-45"
		"box_flag": "Bronze", 
	},
	{
		"id": 23,
		"name": "Yasmin",
		"email": "yaya@mail.com",
		"total_points": 0,
		"cpf": "42186234567", "421.862.345-67"
		"box_flag": "Gold", 
	},
	{
		"id": 23,
		"name": "Marcos",
		"email": "marcoveio@mail.com",
		"total_points": 0,
		"cpf": "12363478454", "123.634.784-54"
		"box_flag": "Gold", 
	}
]
```

- **GET - 200** - (https://chrystians-tarvern.herokuapp.com/clients/<client_id>)

**RESPONSE**
```json
{
		"id": 33,
		"name": "Micael",
		"email": "mickey@mail.com",
		"total_points": 0,
		"cpf": "23245617554", "232.456.175-54"
		"box_flag": null
	}
```

- **PATCH - 200** - (https://chrystians-tarvern.herokuapp.com/clients/<client_id>)

**REQUEST**
```json
{
		"name": "Mickey",
		"email": "mickeymouse@mail.com",
		"total_points": 0,
		"cpf": "23245617554", "232.456.175-54"
		"box_flag": "Gold"
}
```

**RESPOSTA**

```json
{
		"id": 33,
		"name": "Mickey",
		"email": "mickeymouse@mail.com",
		"total_points": 0,
		"cpf": "23245617554", "232.456.175-54"
		"box_flag": "Gold"
	}
```

- **DELETE - 200** - (https://chrystians-tarvern.herokuapp.com/clients/<client_id>) 
```
    No content
```
____

# Route Boxes

- **POST - 201** - (https://chrystians-tarvern.herokuapp.com/boxes)

**REQUEST**
```json
{
	"name": "Box Gold",
	"description": "Box para clientes leais e destemidos",
	"flag": "Gold"
	"monthly_price": 50000
}
```

**RESPONSE**
```json
{
	"name": "Box Gold",
	"description": "Box para clientes leais e destemidos",
	"flag": "Gold"
	"monthly_price": 50000
}
```

- **GET - 200** - (https://chrystians-tarvern.herokuapp.com/boxes) 

**RESPONSE**
```json
[
	{
		"name": "Box Gold",
		"description": "Box para clientes leais e destemidos",
		"flag": "Gold"
		"monthly_price": 50000
	},
	{
		"name": "Box Silver",
		"description": "Box para guerreiros experientes",
		"flag": "Silver"
		"monthly_price": 25000
	},
	{
		"name": "Box Bronze",
		"description": "Box para novos aventureiros",
		"flag": "Bronze"
		"monthly_price": 10000
	}
]
```

- **GET - 201** - (https://chrystians-tarvern.herokuapp.com/boxes/<box_flag>) 

**RESPONSE**
```json
{
	"name": "Box Bronze",
	"description": "Box para novos aventureiros",
	"flag": "Bronze",
	"monthly_price": 10000,
	"month_products": [4, 35, 12]
}
```

- **PATCH** - (https://chrystians-tarvern.herokuapp.com/boxes/<box_flag>) 

**REQUEST** 
```json
{
	"name": "Box Gold",
	"description": "Box para clientes malucos",
	"monthly_price": 15000
}
```
CAN **NOT** A FLAG

**RESPONSE**
```json
{
	"name": "Box Gold",
	"description": "Box para clientes malucos",
	"monthly_price": 1500000,
	"flag": "Gold"
}
```

- **DELETE** - (https://chrystians-tarvern.herokuapp.com/boxes/<box_flag>)
```
    No content
```

```json
**No Content**
```

____

#  Possible Errors

# IntegrityError - 409

- Client, Product or Box already exist in database

```
{
    "error": "Cliente já registrado!"
}
```

# WrongKeys - 400

- Missing a key
- Misstype in a key
- Extra keys

```
{
    "error": "Confira as chaves usadas. Chaves esperadas: ['cpf', 'name', 'email', 'box_flag', 'total_points']
}
```

# UnavailableProduct - 422

- Trying to buy more of one or more products that have in stock
```
{
    "error": "Produto não disponível ou demanda excedente ao estoque"
 }
```

# NotFound - 404

- Not find a Client, Product or Box
```
{
    "error": "Cliente não encontrado, verifique o id"
    
}
```

# DuplicateProduct - 400

- Already have product in database
```
{
    "error": "Produto pedido mais de uma vez na mesma compra, considere incrementar a quantidade"
}
```
