from django.db import models

# Create your models here.

#1. مدل کاربر (User)

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    MEMBERSHIP_CHOICES = [
        ('basic', 'Basic'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]
    
    # فیلدهای شخصی‌سازی شده
    membership_plan = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='basic')
    membership_expiry = models.DateField(null=True, blank=True)
    deposit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reading_score = models.IntegerField(default=0)
    level = models.CharField(max_length=20, default='تازه کار')
    
    # رفع خطای related_name برای groups و user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="library_user_set",
        related_query_name="library_user",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="library_user_permissions_set",
        related_query_name="library_user_permission",
    )

    def __str__(self):
        return self.username

    class Meta:
        # برای جلوگیری از conflicts بیشتر
        swappable = 'AUTH_USER_MODEL'

#2. مدل دسته‌بندی (Category)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

#3. مدل کتاب (Book)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, blank=True)
    summary_ai = models.TextField(blank=True)  # خلاصه تولید شده توسط هوش مصنوعی
    stock = models.IntegerField(default=1)
    deposit_value = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50, default='good')  # وضعیت فیزیکی کتاب
    # اضافه کردن فیلد عکس
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
   
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

#4. مدل امانت کتاب (Borrow)

class Borrow(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    delivery_rating = models.IntegerField(null=True, blank=True)  # امتیاز تحویل
    delivery_comment = models.TextField(blank=True)  # نظر درباره تحویل
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

#5. مدل نظر و امتیاز (Review)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'book']  # هر کاربر فقط یک نظر per book
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

#6. مدل علاقه‌مندی (Wishlist)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'book']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

#7. مدل پلن‌های عضویت (MembershipPlan)
class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    duration_days = models.IntegerField()  # مدت به روز
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_borrows = models.IntegerField()  # حداکثر تعداد امانت همزمان
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

#8. مدل تراکنش‌های مالی (Transaction)

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('membership', 'Membership'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type}"

