from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (ChatPromptTemplate, MessagesPlaceholder)

llm = ChatOpenAI()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

#
# First Question: Create star schema
#
# template = """Given the following SQL tables, your job is to write queries or programs given a user’s request.

# CREATE TABLE Orders (
#   OrderID int,
#   CustomerID int,
#   OrderDate datetime,
#   OrderTime varchar(8),
#   PRIMARY KEY (OrderID)
# );

# CREATE TABLE OrderDetails (
#   OrderDetailID int,
#   OrderID int,
#   ProductID int,
#   Quantity int,
#   PRIMARY KEY (OrderDetailID)
# );

# CREATE TABLE Products (
#   ProductID int,
#   ProductName varchar(50),
#   Category varchar(50),
#   UnitPrice decimal(10, 2),
#   Stock int,
#   PRIMARY KEY (ProductID)
# );

# CREATE TABLE Customers (
#   CustomerID int,
#   FirstName varchar(50),
#   LastName varchar(50),
#   Email varchar(100),
#   Phone varchar(20),
#   PRIMARY KEY (CustomerID)
# );
# """
template = """
-- create schemas
CREATE SCHEMA production;
go

CREATE SCHEMA sales;
go

-- create tables
CREATE TABLE production.categories (
	category_id INT IDENTITY (1, 1) PRIMARY KEY,
	category_name VARCHAR (255) NOT NULL
);

CREATE TABLE production.brands (
	brand_id INT IDENTITY (1, 1) PRIMARY KEY,
	brand_name VARCHAR (255) NOT NULL
);

CREATE TABLE production.products (
	product_id INT IDENTITY (1, 1) PRIMARY KEY,
	product_name VARCHAR (255) NOT NULL,
	brand_id INT NOT NULL,
	category_id INT NOT NULL,
	model_year SMALLINT NOT NULL,
	list_price DECIMAL (10, 2) NOT NULL,
	FOREIGN KEY (category_id) REFERENCES production.categories (category_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (brand_id) REFERENCES production.brands (brand_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE sales.customers (
	customer_id INT IDENTITY (1, 1) PRIMARY KEY,
	first_name VARCHAR (255) NOT NULL,
	last_name VARCHAR (255) NOT NULL,
	phone VARCHAR (25),
	email VARCHAR (255) NOT NULL,
	street VARCHAR (255),
	city VARCHAR (50),
	state VARCHAR (25),
	zip_code VARCHAR (5)
);

CREATE TABLE sales.stores (
	store_id INT IDENTITY (1, 1) PRIMARY KEY,
	store_name VARCHAR (255) NOT NULL,
	phone VARCHAR (25),
	email VARCHAR (255),
	street VARCHAR (255),
	city VARCHAR (255),
	state VARCHAR (10),
	zip_code VARCHAR (5)
);

CREATE TABLE sales.staffs (
	staff_id INT IDENTITY (1, 1) PRIMARY KEY,
	first_name VARCHAR (50) NOT NULL,
	last_name VARCHAR (50) NOT NULL,
	email VARCHAR (255) NOT NULL UNIQUE,
	phone VARCHAR (25),
	active tinyint NOT NULL,
	store_id INT NOT NULL,
	manager_id INT,
	FOREIGN KEY (store_id) REFERENCES sales.stores (store_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (manager_id) REFERENCES sales.staffs (staff_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE sales.orders (
	order_id INT IDENTITY (1, 1) PRIMARY KEY,
	customer_id INT,
	order_status tinyint NOT NULL,
	-- Order status: 1 = Pending; 2 = Processing; 3 = Rejected; 4 = Completed
	order_date DATE NOT NULL,
	required_date DATE NOT NULL,
	shipped_date DATE,
	store_id INT NOT NULL,
	staff_id INT NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES sales.customers (customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (store_id) REFERENCES sales.stores (store_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (staff_id) REFERENCES sales.staffs (staff_id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE sales.order_items (
	order_id INT,
	item_id INT,
	product_id INT NOT NULL,
	quantity INT NOT NULL,
	list_price DECIMAL (10, 2) NOT NULL,
	discount DECIMAL (4, 2) NOT NULL DEFAULT 0,
	PRIMARY KEY (order_id, item_id),
	FOREIGN KEY (order_id) REFERENCES sales.orders (order_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (product_id) REFERENCES production.products (product_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE production.stocks (
	store_id INT,
	product_id INT,
	quantity INT,
	PRIMARY KEY (store_id, product_id),
	FOREIGN KEY (store_id) REFERENCES sales.stores (store_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (product_id) REFERENCES production.products (product_id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", template), 
      MessagesPlaceholder(
          variable_name="chat_history"
      ),  # Where the memory will be stored.
     ("human", "{input}")]
)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory,
)
input = "Write SQL queries which create new tables with star schema."

response = chain.run({"input": input})
#import pdb; pdb.set_trace()

print("\n\nstep1:")
print(response)


#
# Second Question: Add a column in schema.
#
input1 = """The original Customers table now has an additional column dob. \
  Can you add the column in the new tables with star schema? Show me the schema of the star schema tables.
"""
response1 = chain.run({"input": input1})
#import pdb; pdb.set_trace()

print("\n\nstep2:")
print(response1)


#
# Third Question: Write SQLs for transforming data from the original tables to new star schema tables.
#
input2 = """Now, write SQLs that extract and transform records in original tables to tables in star schema.
"""
respons = chain.run({"input": input2})
#import pdb; pdb.set_trace()

print("\n\nstep3:")
print(response2)


#
# Fourth Question: Change SQLs to extract data from the previous hour.
#
input3 = """Now, change the previously created SQLs that extract and transform records in \
  original tables to tables in star schema. They should extract and  transform data in the previous hour.
"""
response3 = chain.run({"input": input3})
#import pdb; pdb.set_trace()

print("\n\nstep4:")
print(response3)


#
# Fifth Question: Write Python code for Airflow to run the previous query.
#
input4 = """Now, write Python code for Airflow that runs the previous SQLs. The previous SQLs should \
  transfer data in the previous hour from the original tables to star schema tables.
"""
response4 = chain.run({"input": input4})
#import pdb; pdb.set_trace()

print("\n\nstep5:")
print(response4)

