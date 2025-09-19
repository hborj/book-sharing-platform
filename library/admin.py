from django.contrib import admin
from .models import User, Category, Book, Borrow, Review, Wishlist, MembershipPlan, Transaction

# مدل User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'membership_plan', 'deposit_balance', 'is_staff']
    list_filter = ['membership_plan', 'level', 'is_staff']
    search_fields = ['username', 'email']
    list_editable = ['membership_plan', 'deposit_balance']  # امکان ویرایش مستقیم در لیست

    def has_delete_permission(self, request, obj=None):
        return True  # اجازه حذف

# مدل Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    
    def has_delete_permission(self, request, obj=None):
        return True

# مدل Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'stock', 'deposit_value', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['title', 'author']
    list_editable = ['stock', 'deposit_value', 'is_available']  # ویرایش سریع

    def has_delete_permission(self, request, obj=None):
        return True

# مدل Borrow
@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'return_date', 'status']
    list_filter = ['status', 'borrow_date']
    list_editable = ['status']  # تغییر وضعیت امانت

    def has_delete_permission(self, request, obj=None):
        return True

# مدل Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    
    def has_delete_permission(self, request, obj=None):
        return True

# مدل Wishlist
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'added_date']
    
    def has_delete_permission(self, request, obj=None):
        return True

# مدل MembershipPlan
@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_days', 'price', 'max_borrows']
    list_editable = ['price', 'max_borrows']  # ویرایش قیمت و تعداد امانت
    
    def has_delete_permission(self, request, obj=None):
        return True

# مدل Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'transaction_type', 'timestamp']
    list_filter = ['transaction_type', 'timestamp']
    
    def has_delete_permission(self, request, obj=None):
        return True