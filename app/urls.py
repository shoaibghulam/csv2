from django.urls import path
from app.views import *
urlpatterns = [
    # class View
    path('', homePage.as_view(),name="Homepage"),
    path('login', Login.as_view(),name="login"),
    path('upload', csvUpload.as_view(),name="upload"),
    path('insertsubcat', subCategoryView.as_view(),name="insertsubcat"),
    path('subcatupdate', subCatUpdate.as_view(),name="subcatupdate"),
    path('category', categoryView.as_view(),name="category"),
    path('categoryupdate', categoryUpdate.as_view(),name="categoryupdate"),
    path('addCategory', addCategory.as_view(),name="addCategory"),
    path('setting', setting.as_view(),name="setting"),
    path('chartview', chartView.as_view(),name="chartview"),
    path('items', itemsView.as_view(),name="items"),
    path('homedata', HomeData.as_view(),name="homedata"),
    path('refunddata', refundData.as_view(),name="refunddata"),
    path('customitem', refundData.as_view(),name="refunddata"),
    path('datasaver', datasaver,name="datasaver"),
    path('insertsubcatdata', insertsubcatdata,name="insertsubcatdata"),

    # def view
    path('subcatdelete/<int:id>',subcatdelete,name="subcatdelete"),
    path('categorydelete/<int:id>',categorydelete,name="categorydelete"),
    path('logout',logout,name="logout"),
    path('additem',additem,name="additem"),
    path('itemdelete/<int:id>',itemdelete,name="itemdelete"),
    path('deleteallcat',deleteallcat,name="deleteallcat"),
    path('deleteallsubcat',deleteallsubcat,name="deleteallsubcat"),
    path('deleteallitem',deleteallitem,name="deleteallitem"),
   
]
