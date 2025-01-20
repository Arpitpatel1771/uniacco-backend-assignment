from django.db import models


# Create your models here.
class RepaymentPlan(models.Model):
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    repayment_period = models.IntegerField()  # in months

    penalty_daily_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    penalty_grace_period = models.IntegerField()  # in days


"""
payment_type of user
amount spent by user
credits remaining of user

transactions made by user
active repaymentPlans of user, for amounts

due_date of the emi


"""


class UserPayment(models.Model):
    user = models.ForeignKey("usermanagement.User", on_delete=models.CASCADE)
    payment_type = models.IntegerField()  # 1 for upfront, 2 for emi
    payment_date = models.DateTimeField(auto_now_add=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.IntegerField()  # 1: pending, 2: paid
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    repayment_plan = models.ForeignKey(
        to=RepaymentPlan, on_delete=models.CASCADE, null=True
    )
    emi_day = models.IntegerField(null=True) # out of 31

    def update_paid_amount(self):
        self.paid_amount = UserTransaction.objects.filter(user_payment=self).aggregate(
            paid_amount=models.Sum("amount")
        )
        self.save()

    def save(self, *args, **kwargs):
        if self.amount:
            self.balance = self.amount + self.penalty_amount - self.paid_amount
            if self.balance > 0:
                self.state = 1
            else:
                self.state = 2

        return super().save(*args, **kwargs)


class UserTransaction(models.Model):
    user_payment = models.ForeignKey(to=UserPayment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
