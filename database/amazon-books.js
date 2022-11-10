db.reviews.aggregate([
    {
        $project: {
            "rating": "$overall",
            "unix_datetime": "$unixReviewTime",
            "user_id": "$reviewerID",
            "item_id": "$asin"
        }
    },
    { $out: "interactions" }
]);

db.interactions.aggregate([
    { $group  : { "_id": "$user_id", count: {$sum:1} } },
    { $sort   : { count: -1 } },
    { $out    : "user_interactions_count" }
]);

// Filter interactions

db.user_interactions_count.aggregate([
    { $match: { 
        $and: [ 
            {count: {$gt:500}},
            {count: {$lt:1500}}
    ] } },
    { $out: "user_500_1500_interactions_count" }
]);

db.user_interactions_count.aggregate([
    { $match: { count: { $gt: 1000 } } },
    { $out: "user_more_1000_interactions_count" }
]);

db.user_interactions_count.aggregate([
    { $match: { count: { $gt: 500 } } },
    { $out: "user_more_500_interactions_count" }
]);

db.user_interactions_count.aggregate([
    { $match: { count: { $gt: 200 } } },
    { $out: "user_more_200_interactions_count" }
]);

db.user_interactions_count.aggregate([
    { $match: { count: { $gt: 150 } } },
    { $out: "user_more_150_interactions_count" }
]);

db.user_interactions_count.aggregate([
    { $match: { count: { $gt: 100 } } },
    { $out: "user_more_100_interactions_count" }
]);

db.user_500_1500_interactions_count.count({})
db.user_more_1000_interactions_count.count({})
db.user_more_500_interactions_count.count({})
db.user_more_200_interactions_count.count({})
db.user_more_150_interactions_count.count({})
db.user_more_100_interactions_count.count({})


// From 500 interactions

db.interactions.aggregate([
    {
        $lookup: {
            from: "user_more_500_interactions_count",
            foreignField: "_id",
            localField: "user_id", 
            as: "result"
        }
    },
    { $match  : { result: { $exists: true, $not: {$size: 0} } } },
    { $project: { _id: 0, user_id: 1, item_id: 1, rating: 1 }   },
    { $out    : "user_more_500_interactions" }
]);


// 500 to 1500 interactions

db.interactions.aggregate([
    {
        $lookup: {
            from: "user_500_1500_interactions_count",
            foreignField: "_id",
            localField: "user_id", 
            as: "result"
        }
    },
    { $match  : { result: { $exists: true, $not: {$size: 0} } } },
    { $project: { _id: 0, user_id: 1, item_id: 1, rating: 1 }   },
    { $out    : "user_500_1500_interactions" }
]);


// Filter books

db.user_more_500_interactions.createIndex({"item_id":1}, { unique: false })
db.books.aggregate([
    {
        $lookup: {
            from: "user_more_500_interactions",
            foreignField: "item_id",
            localField: "asin", 
            as: "result"
        }
   },
   { $match: { result: { $exists: true, $not: {$size: 0} } } },
   {
        $project: {
            item_id: "$asin",
            title: 1,
            description: { "$arrayElemAt": ["$description", 0] },
            main_category: "$main_cat",
            category: 1,
            brand: 1,
            price: 1,
            imageURL: 1,
            also_buy: 1,
            also_view: 1,
            rank: 1
        }
    },
    { $out: "user_more_500_books" }
]);


db.user_more_1000_interactions.createIndex({"item_id":1}, { unique: false })
db.books.aggregate([
    {
        $lookup: {
            from: "user_more_1000_interactions",
            foreignField: "item_id",
            localField: "asin", 
            as: "result"
        }
   },
   { $match: { result: { $exists: true, $not: {$size: 0} } } },
   {
        $project: {
            item_id: "$asin",
            title: 1,
            description: { "$arrayElemAt": ["$description", 0] },
            main_category: "$main_cat",
            category: 1,
            brand: 1,
            price: 1,
            imageURL: 1,
            also_buy: 1,
            also_view: 1,
            rank: 1
        }
    },
    { $out: "user_more_1000_books" }
]);


db.user_500_1500_interactions.createIndex({"item_id":1}, { unique: false })
db.books.aggregate([
    {
        $lookup: {
            from: "user_500_1500_interactions",
            foreignField: "item_id",
            localField: "asin", 
            as: "result"
        }
   },
   { $match: { result: { $exists: true, $not: {$size: 0} } } },
   {
        $project: {
            item_id: "$asin",
            title: 1,
            description: { "$arrayElemAt": ["$description", 0] },
            main_category: "$main_cat",
            category: 1,
            brand: 1,
            price: 1,
            imageURL: 1,
            also_buy: 1,
            also_view: 1,
            rank: 1
        }
    },
    { $out: "user_500_1500_books" }
]);
