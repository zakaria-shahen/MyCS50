from helpers import validations

data = {"name": ["1", "2", "3", "4"]}

output = validations(data, {"name": int})
print(output)

