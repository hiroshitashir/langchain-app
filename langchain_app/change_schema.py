from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

model = ChatOpenAI()

#
# First Question
#
template = """Given the following SQL tables, your job is to write queries given a user’s request.

CREATE TABLE Orders (
  OrderID int,
  CustomerID int,
  OrderDate datetime,
  OrderTime varchar(8),
  PRIMARY KEY (OrderID)
);

CREATE TABLE OrderDetails (
  OrderDetailID int,
  OrderID int,
  ProductID int,
  Quantity int,
  PRIMARY KEY (OrderDetailID)
);

CREATE TABLE Products (
  ProductID int,
  ProductName varchar(50),
  Category varchar(50),
  UnitPrice decimal(10, 2),
  Stock int,
  PRIMARY KEY (ProductID)
);

CREATE TABLE Customers (
  CustomerID int,
  FirstName varchar(50),
  LastName varchar(50),
  Email varchar(100),
  Phone varchar(20),
  PRIMARY KEY (CustomerID)
);
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", template), 
     ("human", "{input}")]
)

chain = prompt | model
input = "Write SQL queries which create new tables with star schema."
response = chain.invoke({"input": input})
import pdb; pdb.set_trace()

print("step1:")
print(response.content)


#
# Second Question
#
prompt1 = ChatPromptTemplate.from_messages(
    [("system", template), 
     ("human", input),
     ("ai", response.content),
     ("human", "{input}"),
     ]
)
chain1 = prompt1 | model
input1 = """The original Customers table now has an additional column dob. \
  Can you add the column in the new tables with star schema? Show me the schema of the star schema tables.
"""
response = chain.invoke({"input": input1})
import pdb; pdb.set_trace()

print("step2:")
print(response.content)
