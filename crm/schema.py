import graphene
from crm.models import Product


class ProductType(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    stock = graphene.Int()


class UpdateLowStockProducts(graphene.Mutation):
    class Output(graphene.ObjectType):
        message = graphene.String()
        updated_products = graphene.List(ProductType)

    def mutate(self, info):
        # Query products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        # Update (restock) each product
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)

        message = f"{len(updated_products)} product(s) restocked."

        return UpdateLowStockProducts.Output(
            message=message,
            updated_products=updated_products
        )


class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, CRM!")


schema = graphene.Schema(query=Query, mutation=Mutation)