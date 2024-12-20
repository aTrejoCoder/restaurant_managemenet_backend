from rest_framework.decorators import api_view
from rest_framework.viewsets import ViewSet

from restaurant.services.stock_service import StockService
from restaurant.services.ingredient_service import IngredientService

from restaurant.utils.result import Result
from restaurant.utils.response import ApiResponse
from restaurant.mappers.stock_mappers import StockTransactionMappers
from restaurant.serializers import IngredientSerializer, StockInsertSerializer, StockSerializer, StockTransactionInsertSerializer

stock_service = StockService()
ingredient_service = IngredientService()

class StockViewSet(ViewSet):
    def list(self, request):
        stock_list = stock_service.get_all_stocks_sort_by_last_transaction()
        stock_list_serialized = StockSerializer(stock_list, many=True).data
        return ApiResponse.ok(stock_list_serialized, 'Stock List Successfully Fetched')

    def get(self, request, pk):
        stock = stock_service.get_stock_by_id(pk)
        if stock is None:
            return ApiResponse.not_found('Stock', 'ID', pk)

        stock_serialized = StockSerializer(stock).data
        return ApiResponse.found(stock_serialized, 'Stock', 'ingredient_id', pk)


    def get_by_ingredient(self, request, ingredient_id):
        ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            return ApiResponse.not_found('Ingredient', 'ID', ingredient_id )

        stock = stock_service.get_stock_by_ingredient(ingredient)
        if stock is None:
            return ApiResponse.ok(None, f'Stock with ingredient Id [{ingredient_id}] has not been init')

        stock_serialized = StockSerializer(stock).data
        return ApiResponse.found(stock_serialized, 'Stock', 'ingredient_id', ingredient_id)


    def create(self, request):
        serializer = StockInsertSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)
        
        ingredient_id = serializer.validated_data.get('ingredient_id')
        ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
        if ingredient is None:
            return ApiResponse.not_found('Ingredient', 'ID', ingredient_id)

        is_stock_unique = stock_service.validate_unique_stock_per_product(ingredient)
        if not is_stock_unique:
            return ApiResponse.ok(None, f'Ingredient Id [{ingredient_id}] already has stock')

        stock = stock_service.init_stock(ingredient, serializer.validated_data)
        stock_serialized = StockSerializer(stock).data
        
        return ApiResponse.ok(stock_serialized, f'Stock with ingredient Id {ingredient_id} successfully init')


    def add_transaction(self, request):
        serializer = StockTransactionInsertSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.bad_request(serializer.errors)

        stock_id = serializer.validated_data.get('stock_id')
        stock = stock_service.get_stock_by_id(stock_id)
        if stock is None:
            return ApiResponse.not_found('Stock', 'ID', stock_id)

        trasaction = StockTransactionMappers.serializerToDomain(serializer.validated_data)
        trasaction.stock = stock

        validation_result = stock_service.validate_transaction(stock, trasaction)
        if (validation_result.is_failure()):
            return ApiResponse.bad_request(validation_result.get_error_msg())

        stock = stock_service.add_transaction(stock, trasaction)
        stock_serialized = StockSerializer(stock).data
        
        return ApiResponse.ok(stock_serialized, 'Transaction succesfully added')


    def delete(self, request, pk):
        is_deleted = stock_service.delete_stock_by_id(pk)
        if not is_deleted:
            return ApiResponse.not_found('Stock', 'ID', pk)

        return ApiResponse.deleted('Stock Item')