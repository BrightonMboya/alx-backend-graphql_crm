import graphene
from graphene_django import DjangoObjectType
from crm.models import Product  # Adjust if your Product model is in another app

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No arguments needed

    success = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated = []
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated.append(product)
        return UpdateLowStockProducts(
            success=f"{len(updated)} product(s) restocked.",
            updated_products=updated
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# If not already defined, add:
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello from GraphQL!")

schema = graphene.Schema(query=Query, mutation=Mutation)
