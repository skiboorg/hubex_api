from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta

from order.models import Order

class WeeklyStats(APIView):
    def get(self, request):
        current_date = datetime.now().date()
        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        date_range = [start_of_week + timedelta(days=i) for i in range(7)]
        dates = []
        total_done = 0
        print(date_range)
        for date in date_range:

            orders = Order.objects.filter(date_done=date)
            print(orders)
            dates.append({
                str(date):{
                    'done_orders':orders.filter(is_done=True).count(),
                    'total_orders':orders.count(),
                }

            })
            total_done += orders.filter(is_done=True).count()
        # result.append({
        #     'total_done':total_done
        # })

        return Response([dates,{
            'total_done':total_done
        }], status=200)