from django.db import models

# Create your models here.


# for testing only
class Product(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'product'


class User(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    intnr = models.BigIntegerField(null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'user'


class Mt(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    intnr = models.BigIntegerField(null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'mt'


class Domain(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'domain'


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
    email = models.CharField(max_length=50, blank=True, null=True)
    addzusatz = models.CharField(max_length=50, blank=True, null=True)
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lastchanged = models.DateTimeField(auto_now=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'pair'


class Pp(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    ext_datum = models.DateField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

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
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'paymentdetail'


class Paypal(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    paymentdetail = models.ForeignKey(PaymentDetail, on_delete=models.PROTECT, null=True)
    given_name = models.CharField(max_length=20, blank=True, null=True)
    surname = models.CharField(max_length=20, blank=True, null=True)
    payer_id = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.CharField(max_length=40, blank=True, null=True)
    address_line_1 = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    admin_area_1 = models.CharField(max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(null=True)
    update_time = models.DateTimeField(null=True)
    lastchanged = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=25, blank=True, null=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'paypal'


class Cash(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    paymentdetail = models.ForeignKey(PaymentDetail, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'cash'


class OptionCat(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'option_cat'


class Cat(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    catnr = models.BigIntegerField(null=True)
    cat0 = models.CharField(max_length=25, blank=True, null=True)
    cat1 = models.CharField(max_length=25, blank=True, null=True)
    cat2 = models.CharField(max_length=25, blank=True, null=True)
    cat3 = models.CharField(max_length=25, blank=True, null=True)
    lastchanged = models.DateTimeField(auto_now=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'cat'


class Nugget(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    menge = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    einzelpreis = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    einheit = models.CharField(max_length=10, blank=True, null=True)
    addonflag = models.BooleanField(default=False)
    description_long = models.CharField(max_length=200, blank=True, null=True)
    nuggetnr = models.BigIntegerField(null=True)
    pic_url = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)
    # cat = models.ForeignKey(Cat, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)
    optioncat = models.ForeignKey(OptionCat, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'nugget'


class NuggetCat(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True)
    nugget = models.ForeignKey(Nugget, on_delete=models.CASCADE, null=True)
    lastchanged = models.DateTimeField(auto_now=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'nugget_cat'


class Folg(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    pp = models.ForeignKey(Pp, on_delete=models.PROTECT, null=True)
    pair = models.ForeignKey(Pair, on_delete=models.PROTECT, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    method = models.ForeignKey(Method, on_delete=models.PROTECT, null=True)
    paymentdetails = models.ForeignKey(PaymentDetail, on_delete=models.PROTECT, null=True)
    paypaldetails = models.ForeignKey(Paypal, on_delete=models.PROTECT, null=True)
    lastchanged = models.DateTimeField(auto_now=True)
    counter = models.IntegerField(null=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'folg'


class Basket(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    nugget = models.ForeignKey(Nugget, on_delete=models.PROTECT, null=True)
    menge = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    einzelpreis = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    value = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    einheit = models.CharField(max_length=10, blank=True, null=True)
    # indeicates if a nugget has addon nuggets
    group = models.IntegerField(null=True)
    addonCount = models.IntegerField(null=True)
    addonflag = models.BooleanField(default=False)
    folg = models.ForeignKey(Folg, on_delete=models.PROTECT, null=True)
    # user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    lastchanged = models.DateTimeField(auto_now=True)
    mt = models.ForeignKey(Mt, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'basket'

