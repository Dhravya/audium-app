import random

gradients = [
    "bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500",
    "bg-gradient-to-r from-green-300 via-blue-500 to-purple-600",
    "bg-gradient-to-r from-pink-300 via-purple-300 to-indigo-400",
    "bg-gradient-to-r from-gray-700 via-gray-900 to-black",
    "bg-gradient-to-r from-indigo-200 via-red-200 to-yellow-100",
    "bg-gradient-to-r from-yellow-100 via-yellow-300 to-yellow-500",
]

hashtags = ['story', 'music', 'coding', 'funny']



#! TEMP CONSTANTS


comments = [
    {
        "author": "Lorem ipsum",
        "date": "2020-01-01",
        "comment": "Mazim ea eos diam duo molestie eum et et sadipscing",
        "image": f"https://picsum.photos/id/{random.randint(1, 100)}/200/300",
    }
    for _ in range(10)
]
