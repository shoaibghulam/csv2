from django.db import models
from rest_framework import serializers
DEFAULT_KEY=1

# Create your models here.
# Create user accounts
class Users(models.Model):
    uId=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=100)
    lastName=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    contactNo=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.firstName


class category(models.Model):
    catid=models.AutoField(primary_key=True)
    catName=models.CharField(max_length=150)
    # uid=models.ForeignKey(Users, on_delete=models.SET_NULL , blank=True,null=True)
    def __str__(self):
        return str(self.catName)

class subCategory(models.Model):
    sid=models.AutoField(primary_key=True)
    SName=models.CharField(max_length=200)
    catid=models.ForeignKey(category,  on_delete=models.SET_NULL , null=True)
    # uid=models.ForeignKey(Users,  on_delete=models.SET_NULL , blank=True,null=True)
    
    def __str__(self):
        return str(self.SName)



# items 
class items(models.Model):
    id=models.AutoField(primary_key=True)
    Date=models.DateField()
    Amount=models.FloatField()
    Description=models.TextField(max_length=400)
    DoingBusinessAs=models.TextField(max_length=200)
    StreetAddress=models.TextField(max_length=400)
 
    City=models.TextField(max_length=400)
    uid=models.ForeignKey(Users, on_delete=models.CASCADE)
    subcatid=models.ForeignKey(subCategory,  on_delete=models.SET_NULL , blank=True,null=True, default=DEFAULT_KEY)


    #Temp items 
class itemsTemp(models.Model):
    id=models.AutoField(primary_key=True)
    Date=models.DateField()
    Amount=models.FloatField()
    Description=models.TextField(max_length=400)
    DoingBusinessAs=models.TextField(max_length=200)
    StreetAddress=models.TextField(max_length=400)
   
    City=models.TextField(max_length=400)
    uid=models.ForeignKey(Users, on_delete=models.CASCADE)
    subcatid=models.ForeignKey(subCategory,  on_delete=models.SET_NULL , blank=True,null=True, default=DEFAULT_KEY)
    def __str__(self):
        return str(self.Amount)

    def __str__(self):
        return str(self.Amount)




class serSubCat(serializers.ModelSerializer):
    class Meta:
        model = subCategory
        fields='__all__'


class serCat(serializers.ModelSerializer):
    class Meta:
        model = category
        fields='__all__'


class serItems(serializers.ModelSerializer):
    class Meta:
        model = items
        fields='__all__'