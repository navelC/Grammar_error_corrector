import pandas as pd

with open('cleaned_text.txt') as f:
  correct_data = f.read()

with open('incorrect.txt') as f:
  error_data = f.read()

final_data = pd.DataFrame(columns = ['error', 'correct'])

final_data['correct'] = correct_data.split('\n')
final_data['error'] = error_data.split('\n')[:len(final_data['correct'])]

final_data = final_data.drop_duplicates()

final_data = final_data.dropna()

print(final_data.describe())

final_data = final_data.loc[final_data["correct"].str.count(" ") > 2]

print(final_data.describe())
final_data.to_csv("data.csv", index = False)

