from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (ChatPromptTemplate, MessagesPlaceholder)

llm = ChatOpenAI()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

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
response2 = chain.run({"input": input2})
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

