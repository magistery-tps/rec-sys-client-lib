# Export collections as json files:

mongoexport -d amazon-books -c user_500_1500_interactions --out user_500_1500_interactions.json --jsonArray
mongoexport -d amazon-books -c user_500_1500_books --out user_500_1500_books.json --jsonArray


# Format:

cat user_500_1500_interactions.json | json_pp  > user_500_1500_interactions2.json 
cat user_500_1500_books.json | json_pp  > user_500_1500_books2.json 