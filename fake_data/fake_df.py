from faker import Faker
import pandas as pd

fake = Faker()
product_list = ['Apple', 'Banana', 'Cherry', 'Date', 'Fig', 'Grape']
category_list = ['Fruit', 'Vegetable', 'Dairy', 'Meat', 'Beverage', 'Snack']
df = pd.DataFrame({
    'Product': [fake.word(ext_word_list=product_list) for _ in range(100)],
    'Category': [fake.word(ext_word_list=category_list) for _ in range(100)],
    'Costs': [fake.pydecimal(left_digits=2, right_digits=2, positive=True) for _ in range(100)],
})

fake_df = df