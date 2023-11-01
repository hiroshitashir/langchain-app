from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

model = ChatOpenAI()

#
# First Question: Create star schema
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
#import pdb; pdb.set_trace()

print("step1:")
print(response.content)


#
# Second Question: Add a column in schema.
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
response1 = chain.invoke({"input": input1})
#import pdb; pdb.set_trace()

print("step2:")
print(response1.content)


#
# Third Question: Write SQLs for transforming data from the original tables to new star schema tables.
#
prompt2 = ChatPromptTemplate.from_messages(
    [("system", template), 
     ("human", input),
     ("ai", response.content),
     ("human", input1),
     ("ai", response1.content),
     ("human", "{input}"),
     ]
)
chain2 = prompt2 | model
input2 = """Now, write SQLs that extract and transform records in original tables to tables in star schema.
"""
response2 = chain.invoke({"input": input2})
#import pdb; pdb.set_trace()

print("step3:")
print(response2.content)


#
# Fourth Question: Change SQLs to extract data from the previous hour.
#
prompt3 = ChatPromptTemplate.from_messages(
    [("system", template), 
     ("human", input),
     ("ai", response.content),
     ("human", input1),
     ("ai", response1.content),
     ("human", input2),
     ("ai", response2.content),
     ("human", "{input}"),
     ]
)
chain3 = prompt3 | model
input3 = """Now, change the previously created SQLs that extract and transform records in \
  original tables to tables in star schema. They should extract and  transform data in the previous hour.
"""
response3 = chain.invoke({"input": input3})
#import pdb; pdb.set_trace()

print("step4:")
print(response3.content)


#
# Fifth Question: Write Python code for Airflow to run the previous query.
#
prompt4 = ChatPromptTemplate.from_messages(
    [("system", template), 
     ("human", input),
     ("ai", response.content),
     ("human", input1),
     ("ai", response1.content),
     ("human", input2),
     ("ai", response2.content),
     ("human", input3),
     ("ai", response3.content),
     ("human", "{input}"),
     ]
)
chain4 = prompt4 | model
input4 = """Now, write Python code for Airflow that runs the previous SQLs. The previous SQLs should \
  transfer data in the previous hour from the original tables to star schema tables.
"""
response4 = chain.invoke({"input": input4})
#import pdb; pdb.set_trace()

print("step5:")
print(response4.content)

