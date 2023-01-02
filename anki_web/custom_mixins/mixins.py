from supermemo2 import SMTwo

review = SMTwo.first_review(5)
review = SMTwo(review.easiness, review.interval, review.repetitions).review(5)
review = SMTwo(review.easiness, review.interval, review.repetitions).review(5)
review = SMTwo(review.easiness, review.interval, review.repetitions).review(3)
review = SMTwo(review.easiness, review.interval, review.repetitions).review(5)
review = SMTwo(review.easiness, review.interval, review.repetitions).review(5)
print(review.easiness)
print(review.interval)
print(review.repetitions)
print(review.review_date)
