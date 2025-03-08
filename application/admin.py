from django.contrib import admin

# Register your models here.
from .models import Product,Cart,Saree,FeaturedSaree,SilkSaree,CottonSaree,TrendingSarees

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price']
    search_fields=['name',]
    list_filter=['price',]
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity']
    list_filter= ['user',]
admin.site.register(Cart,CartAdmin)

class SareeAdmin(admin.ModelAdmin):
    list_display=['product_id','title','description','image','color','saree_model','about_item']
admin.site.register(Saree,SareeAdmin)

class FeaturedSareeAdmin(admin.ModelAdmin):
    list_display=['product_id','title','description','image','color','saree_model','about_item']
admin.site.register(FeaturedSaree,FeaturedSareeAdmin)

class SilkSareeAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
admin.site.register(SilkSaree,SilkSareeAdmin)

class CottonSareeAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
admin.site.register(CottonSaree,CottonSareeAdmin)

class TrendingAdmin(admin.ModelAdmin):
    list_display=['title','image']
admin.site.register(TrendingSarees,TrendingAdmin)