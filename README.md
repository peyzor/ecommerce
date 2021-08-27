# Django web crawler

gathers data from [mobit](https://www.mobit.ir/) website
and then creates category based products in the database

## Command

$ python manage.py product_crawler category_name page_number_limit

### Available categories

- all
- phones
- laptops
- tablets
- tvs
- printers

### Pages retrieved

page_number_limit specifies gathering data from page 1 upto this page number
defaults to 1
