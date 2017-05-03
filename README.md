# Facturation.pro client library

Just a basic client library allowing to query Facturation.pro quite simply.

Used for my personal activity and to ease integration with other tools like an EDM
or accounting software.

Example use:

```python
from facturation.pro.api.helpers import ClientFactory
from facturation.pro.api.customers import Customers

# create a ClientFactory. Using it we will instantiate for all types with the same parameters.
cf = ClientFactory(username=54321, password='abcdef1234abcdef1234', firm_id=12345, identifier='foobar@mycompany.net')

# generate a Client object for the Customers type
cus_client = cf.get(Customers)

cus_client.list()  # list all current customers
# create a new customer
cus_client.post(dict(first_name="John", last_name="Doe", individual=True, company=False, country="FR", city="Paris", street="2 rue des Lapins Bleus", zip_code=75019))

cus_client.list()  # list all current customers... again. John Doe is in there

does = cus_client.list(last_name="Doe")

john_doe = [c for c in does if (c['first_name'], c['last_name']) == ('John', 'Doe')][0]
print(john_doe)

# delete John Doe
cus_client.delete(john_doe)
```
