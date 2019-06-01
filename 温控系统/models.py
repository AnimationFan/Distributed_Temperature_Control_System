from django.db import models
#默认的主键为用户名
class User(models.Model):
    USER_TYPE=(
        ('C','Customer'),
        ('F','Front'),
        ('A','AirCManager'),
        ('H','HotelManager'),
    )
    user_name=models.CharField(max_length=30,unique=True,blank=False)
    password=models.CharField(max_length=30,blank=False)
    user_type=models.CharField(max_length=3,choices=USER_TYPE,blank=False)


class AirC(models.Model):
    room_num=models.CharField(max_length=10,blank=False)


class UserRoom(models.Model):
    user_name=models.OneToOneField(User,on_delete=models.CASCADE,blank=False)
    room=models.OneToOneField(AirC,on_delete=models.CASCADE,blank=False)

#datetimefield存储的是一个datetime.datetime 对象
class UseRecord(models.Model):
    WIND_SIZE=(
        ('L','Low'),
        ('M','Middle'),
        ('H','High')
        )

    begin_time=models.DateTimeField(auto_now=False,auto_now_add=False)
    end_time=models.DateTimeField(auto_now=False,auto_now_add=False)
    user_name=models.OneToOneField(User,on_delete=models.CASCADE,blank=False)
    room_num=models.OneToOneField(AirC,on_delete=models.CASCADE,blank=False)
    temp=models.IntegerField(blank=False)
    wind=models.CharField(max_length=5,choices=WIND_SIZE)
    price=models.FloatField(blank=False)
# Create your models here.
