import os
import tempfile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.csv_parser import load_transactions
from .services.normalizer import normalize_merchant
from .services.recurrence import detect_recurring
from .services.analyzer import analyze_subscriptions


class AnalyzeCSVView(APIView):

    def post(self, request):

        uploaded_file = request.FILES.get("file")

        if not uploaded_file:

            return Response(
                {
                    "success": False,
                    "error": "Please upload a CSV file."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        temp_path = None

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".csv"
            ) as temp_file:

                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

                temp_path = temp_file.name

            # Parse statement
            df = load_transactions(temp_path)

            # Normalize merchants
            df["merchant"] = df["description"].apply(
                normalize_merchant
            )

            # Detect recurring payments
            recurring = detect_recurring(df)

            # Analyze subscriptions
            subscriptions = analyze_subscriptions(
                recurring
            )

            # Convert transactions for React
            transactions = []

            for _, row in df.iterrows():

                transactions.append({
                    "date": row["date"].strftime(
                        "%Y-%m-%d"
                    ),

                    "description": row["description"],

                    "merchant": row["merchant"],

                    "amount": float(row["amount"]),
                })

            return Response({

                "success": True,

                "transaction_count": len(transactions),

                "subscription_count": len(
                    subscriptions
                ),

                "transactions": transactions,

                "subscriptions": subscriptions,
            })

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        finally:

            if (
                temp_path
                and os.path.exists(temp_path)
            ):
                os.remove(temp_path)