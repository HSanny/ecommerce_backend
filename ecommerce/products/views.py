from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from collections import defaultdict
from mongo_utils.mongo import get_db_handle
import json

class PromotedProductView(APIView):
    def post(self, request):
        db_handle, _ = get_db_handle()
        collection = db_handle.amazon_product

        # retrieve user input (search and browse history)

        user_data = json.loads(request.body).get('user_data', {})
        user_id = user_data('user_id')
        search_history = user_data.get('search_history', [])
        browse_history = user_data.get('browse_history', [])

        # check if user has any search/browse history
        if search_history or browse_history:
            # generate recommendations based on the model
            # //TODO
            recommended_products = self.get_recommendations(user_id, search_history, browse_history)

            if len(recommended_products) < 5:
                highest_rated_products = self.get_highest_rated_products(collection, 5 - len(recommended_products))
                promoted_products = recommended_products + highest_rated_products
            else:
                promoted_products = recommended_products[:5]
        else:
            promoted_products = self.get_highest_rated_products(collection, 5)

        return JsonResponse({'promoted_products': promoted_products}, status=200)
    
    def get_recommendations(self, user_id, search_history, browse_history):
        # Use your recommender model to generate product recommendations
        # For now, just a placeholder
        recommendations = recommender_model.predict(user_id, search_history, browse_history)
        return recommendations

    def get_highest_rated_products(self, collection, limit):
        # Query MongoDB to find the top N highest-rated products
        products = collection.find().sort('rating', -1).limit(limit)
        product_list = [
            {
                'id': str(product['_id']),
                'product_name': product['product_name'][:50] + '...' if len(product['product_name']) > 50 else product['product_name'],
                'rating': product['rating'],
                'discounted_price': product['discounted_price'],
                'actual_price': product['actual_price'],
                'image': product['img_link']
            } for product in products
        ]
        return product_list
class ProductListView(APIView):
    @csrf_exempt
    def post(self, request):
        db_handle, _ = get_db_handle()
        collection = db_handle.amazon_product

        data = json.loads(request.body)
        filters = data.get('filters', {})
        query = {}

        filter_params = [
            'category',
            'rating_gte', 'rating_lte'
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

        # handle the search parameter
        search = filters.get('search', '')
        if search:
            query['product_name'] = {'$regex': search, '$options': 'i'}

        print("Constructed MongoDB query: ", query)

        page_number = int(data.get('page', 1))
        items_per_page = 10
        skip_items = (page_number - 1) * items_per_page

        total_documents = collection.count_documents(query)
        documents = collection.find(query).skip(skip_items).limit(items_per_page)
        total_pages = (total_documents + items_per_page - 1) // items_per_page

        product_list = [
            {
                'id': str(doc['_id']),
                'product_name': doc['product_name'][:50] + '...' if len(doc['product_name']) > 50 else doc['product_name']
                **{key: value for key,value in doc.items() if key != '_id'}
            } for doc in documents
        ]

        print("Returned products: ", product_list) 

        response_data = {
            'products': product_list,
            'total_pages': total_pages,
        }

        return JsonResponse(response_data, status=200)

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
        collection = db_handle.amazon_product

        try:
            product = collection.find_one({'_id': ObjectId(product_id)})
            if product:
                product['id'] = str(product['_id'])
                del product['_id']

                # clean price field
                if 'actual_price' in product:
                    product['actual_price'] = clean_price(product['actual_price'])
                if 'discounted_price' in product:
                    product['discounted_price'] = clean_price(product['discounted_price'])
                
                # handle complex fields (lists)
                product['user_id'] = product.get('user_id', '').split(',') if 'user_id' in product else []
                product['user_name'] = product.get('user_name', '').split(',') if 'user_name' in product else []
                product['review_id'] = product.get('review_id', '').split(',') if 'review_id' in product else []
                product['review_title'] = product.get('review_title', '').split(',') if 'review_title' in product else []
                product['review_content'] = product.get('review_content', '').split(',') if 'review_content' in product else []

                # serialise the product data
                serialiser = ProductSerializer(product)
                return Response(serialiser.data, status=status.HTTP_200_OK)
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DataSummaryView(APIView):
    def get(self, request):
        db_handle, _ = get_db_handle()
        collection = db_handle.amazon_product

        pipeline = [
            {
                '$addFields': {
                    'split_categories': {
                        '$split': ['$category', '|']
                    },

                    'discount_price_clean': {
                        '$cond': {
                            'if': {'$eq': ['$discounted_price', '']},
                            'then': None,
                            'else': {
                                '$toDouble': {
                                    '$replaceAll': {
                                        'input': {'$replaceAll': {'input': '$discounted_price', 'find': '₹', 'replacement': ''}},
                                        'find': ',',
                                        'replacement': ''
                                    }
                                }
                            }
                        }
                    },
                    'actual_price_clean': {
                        '$cond': {
                            'if': {'$eq': ['$discounted_price', '']},
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
                '$unwind': '$split_categories'
            },
            {
                '$group': {
                    '_id': None,
                    'categories': {'$addToSet': '$split_categories'},
                    'all_ratings': {'$addToSet': '$rating'},
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