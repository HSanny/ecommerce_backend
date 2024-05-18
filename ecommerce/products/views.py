from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from collections import defaultdict
from mongo_utils.mongo import get_db_handle
import json

class ProductListView(APIView):
    @csrf_exempt
    def post(self, request):
        db_handle, _ = get_db_handle()
        collection = db_handle.amazon_products

        data = json.loads(request.body)
        filters = data.get('filters', {})
        query = {}

        filter_params = [
            'main_category', 'sub_category',
            'ratings_gte', 'ratings_lte'
        ]

        for param in filter_params:
            value = filters.get(param)
            if value:
                if 'gte' in param or 'lte' in param:
                    field, operator = param.rsplit('_', 1)
                    if field not in query:
                        query[field] = {}
                    query[field]['$' + operator] = float(value)
                else:
                    query[param] = value

        # Handle the search parameter
        search = filters.get('search', '')
        if search:
            query['name'] = {'$regex': search, '$options': 'i'}

        print("Constructed MongoDB query:", query)  # Debugging statement

        page_number = int(data.get('page', 1))
        items_per_page = 10
        skip_items = (page_number - 1) * items_per_page

        total_documents = collection.count_documents(query)
        documents = collection.find(query).skip(skip_items).limit(items_per_page)
        total_pages = (total_documents + items_per_page - 1) // items_per_page

        product_list = [
            {
                'id': str(doc['_id']),
                **{key: value for key, value in doc.items() if key != '_id'}
            } for doc in documents
        ]

        print("Returned products:", product_list)  # Debugging statement

        response_data = {
            'products': product_list,
            'total_pages': total_pages,
        }

        return JsonResponse(response_data, status=200)

    def get(self, request):
        return JsonResponse({'error': 'This endpoint only supports POST requests'}, status=405)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson.objectid import ObjectId
from .serializers import ProductSerializer
from mongo_utils.mongo import get_db_handle
from mongo_utils.util import clean_product_name  # Import the clean_product_name function if needed

def clean_price(price_str):
    if price_str:
        return float(price_str.replace('₹', '').replace(',', ''))
    return None

class SingleProductView(APIView):
    def get(self, request, product_id):
        db_handle, _ = get_db_handle()
        collection = db_handle.amazon_products

        try:
            product = collection.find_one({'_id': ObjectId(product_id)})
            if product:
                product['id'] = str(product['_id'])
                del product['_id']
                
                # Clean price fields
                if 'actual_price' in product:
                    product['actual_price'] = clean_price(product['actual_price'])
                if 'discount_price' in product:
                    product['discount_price'] = clean_price(product['discount_price'])
                
                # Clean product name if needed
                if 'name' in product:
                    product['name'] = clean_product_name(product['name'])

                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DataSummaryView(APIView):
    def get(self, request):
        db_handle, _ = get_db_handle()
        collection = db_handle.amazon_products

        pipeline = [
            {
                '$addFields': {
                    'discount_price_clean': {
                        '$cond': {
                            'if': {'$eq': ['$discount_price', '']},
                            'then': None,
                            'else': {
                                '$toDouble': {
                                    '$replaceAll': {
                                        'input': {'$replaceAll': {'input': '$discount_price', 'find': '₹', 'replacement': ''}},
                                        'find': ',',
                                        'replacement': ''
                                    }
                                }
                            }
                        }
                    },
                    'actual_price_clean': {
                        '$cond': {
                            'if': {'$eq': ['$discount_price', '']},
                            'then': None,
                            'else': {
                                '$toDouble': {
                                    '$replaceAll': {
                                        'input': {'$replaceAll': {'input': '$actual_price', 'find': '₹', 'replacement': ''}},
                                        'find': ',',
                                        'replacement': ''
                                    }
                                }
                            }
                        }
                    },
                }
            },
            {
                '$group': {
                    '_id': None,
                    'main_categories': {'$addToSet': '$main_category'},
                    'sub_categories': {'$addToSet': '$sub_category'},
                    'all_ratings': {'$addToSet': '$ratings'},
                    'max_discount_price': {'$max': '$discount_price_clean'},
                    'min_discount_price': {'$min': '$discount_price_clean'},
                    'max_actual_price': {'$max': '$actual_price_clean'},
                    'min_actual_price': {'$min': '$actual_price_clean'},
                }
            }
        ]

        summary = collection.aggregate(pipeline)
        summary_list = list(summary)

        return JsonResponse(summary_list, safe=False)