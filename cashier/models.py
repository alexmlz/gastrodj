from django.db import models

# Create your models here.


# for testing only
class Product(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'product'


class Status(models.Model):
    description = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'status'


class Pair(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    pairnr = models.BigIntegerField(null=True)
    namevorname = models.CharField(max_length=100, blank=True, null=True)
    strassenr = models.CharField(max_length=150, blank=True, null=True)
    plzstadt = models.CharField(max_length=100, blank=True, null=True)
    telefonnr = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pair'


class Pp(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    ext_datum = models.DateField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pp'


class Method(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'method'


class PaymentDetail(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    method = models.ForeignKey(Method, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'paymentdetail'


class Paypal(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    paymentdetail = models.ForeignKey(PaymentDetail, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'paypal'


class Cash(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    paymentdetail = models.ForeignKey(PaymentDetail, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cash'


class Cat(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    catnr = models.BigIntegerField(null=True)
    cat0 = models.CharField(max_length=25, blank=True, null=True)
    cat1 = models.CharField(max_length=25, blank=True, null=True)
    cat2 = models.CharField(max_length=25, blank=True, null=True)
    cat3 = models.CharField(max_length=25, blank=True, null=True)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cat'


class Nugget(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    description_long = models.CharField(max_length=200, blank=True, null=True)
    nuggetnr = models.BigIntegerField(null=True)
    pic_url = models.CharField(max_length=100, blank=True, null=True)
    # cat = models.ForeignKey(Cat, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nugget'


class NuggetCat(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True)
    nugget = models.ForeignKey(Nugget, on_delete=models.CASCADE, null=True)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nugget_cat'


class Folg(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    pp = models.ForeignKey(Pp, on_delete=models.PROTECT, null=True)
    pair = models.ForeignKey(Pair, on_delete=models.PROTECT, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    method = models.ForeignKey(Method, on_delete=models.PROTECT, null=True)
    paymentdetails = models.ForeignKey(PaymentDetail, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'folg'


class Basket(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    nugget = models.ForeignKey(Nugget, on_delete=models.PROTECT, null=True)
    method = models.ForeignKey(Method, on_delete=models.PROTECT, null=True)
    folg = models.ForeignKey(Folg, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'basket'


class ShoppingCart(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    nugget = models.ForeignKey(Nugget, on_delete=models.PROTECT, null=True)
    method = models.ForeignKey(Method, on_delete=models.PROTECT, null=True)
    folg = models.ForeignKey(Folg, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    lastchanged = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shopping_cart'
