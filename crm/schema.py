import graphene
from graphene_django import DjangoObjectType
from .models import Product
from datetime import datetime

# --- Define Product Type ---
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

# --- Define Mutation ---
class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No input arguments needed

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10  # simulate restock
            product.save()
            updated_products.append(product)

        msg = f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} — {len(updated_products)} products restocked."
        return UpdateLowStockProducts(updated_products=updated_products, message=msg)


# --- Root Mutation ---
class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()