from mongoengine import connect

connect(
    db="events_db",
    host="mongodb+srv://groupe9:groupe%409@cluster0.y8zgs6y.mongodb.net/events_db?retryWrites=true&w=majority"
)