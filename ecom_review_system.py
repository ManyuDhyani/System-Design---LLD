"""
✅ User adds review text + overall rating
✅ User rates specific features
✅ User sees rating summary
✅ Filters supported:

My Reviews

By Product

Top Rated Reviews
"""

# ---------- User CLASSES ----------
class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name

class FeatureRating:
    def __init__(self, feature, rating):
        self.feature = feature  # e.g., "Battery"
        self.rating = rating    # e.g., 4

# ---------- REVIEW ----------
class Review:
    def __init__(self, user, rating, text, feature_ratings=[]):
        self.user = user
        self.rating = rating        # Overall rating
        self.text = text
        self.feature_ratings = feature_ratings  # List of FeatureRating

# ---------- PRODUCT ----------
class Product:
    def __init__(self, product_id, name):
        self.id = product_id
        self.name = name
        self.reviews = []  # List of Review

    def add_review(self, review):
        self.reviews.append(review)
    
    def show_summary(self):
        if not self.reviews:
            print("No reviews yet.")
            return

        total_rating = 0
        feature_map = {}

        for r in self.reviews:
            total_rating += r.rating
            for fr in r.feature_ratings:
                if fr.feature not in feature_map:
                    feature_map[fr.feature] = []
                feature_map[fr.feature].append(fr.rating)

        print(f"Average Rating: {total_rating / len(self.reviews):.1f}")
        for feature, ratings in feature_map.items():
            avg = sum(ratings) / len(ratings)
            print(f"  {feature} Rating: {avg:.1f}")

# ---------- REVIEW MANAGER ----------
class ReviewManager:
    def __init__(self):
        self.all_reviews = []  # Stores (product, review) tuples

    def add_review(self, product, review):
        product.add_review(review)
        self.all_reviews.append((product, review))

    def get_reviews_by_user(self, user_id):
        return [r for _, r in self.all_reviews if r.user.id == user_id]

    def get_reviews_by_product(self, product_id):
        return [r for p, r in self.all_reviews if p.id == product_id]

    def get_top_reviews(self, top_n=3):
        sorted_reviews = sorted(self.all_reviews, key=lambda x: x[1].rating, reverse=True)
        return [r for _, r in sorted_reviews[:top_n]]


# Setup
user1 = User(1, "Alice")
user2 = User(2, "Bob")
product = Product(101, "Smartphone X")
manager = ReviewManager()

# Add reviews
r1 = Review(user1, 5, "Excellent phone!", [FeatureRating("Camera", 5), FeatureRating("Battery", 4)])
r2 = Review(user2, 3, "Decent, but battery drains", [FeatureRating("Battery", 3)])
manager.add_review(product, r1)
manager.add_review(product, r2)

# Show product summary
product.show_summary()

# Filter examples
print("\nMy Reviews (Alice):")
for r in manager.get_reviews_by_user(1):
    print(f"- {r.text} (Rating: {r.rating})")

print("\nReviews for Product 101:")
for r in manager.get_reviews_by_product(101):
    print(f"- {r.text} by {r.user.name}")

print("\nTop Rated Reviews:")
for r in manager.get_top_reviews(1):
    print(f"- {r.text} (Rating: {r.rating}) by {r.user.name}")
