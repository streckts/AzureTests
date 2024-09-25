from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential

import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv('DI_ENDPOINT')
credential = AzureKeyCredential(os.getenv('DI_API_KEY'))
di_client = DocumentIntelligenceClient(endpoint, credential)

test_image = 'https://www.receiptfont.com/wp-content/uploads/template-aldi-1-screenshot-1.png' # Receipt from ALDI

poller = di_client.begin_analyze_document(
    "prebuilt-receipt",
    AnalyzeDocumentRequest(url_source=test_image)
)

receipts: AnalyzeResult = poller.result()

if receipts.documents:
    for idx, receipt in enumerate(receipts.documents):
        print("--------Analysis of receipt #{idx + 1}--------")
        if receipt.fields:
            merchant_name = receipt.fields.get("MerchantName")
            if merchant_name:
                print(
                    f"Merchant Name: {merchant_name.get('valueString')} has confidence: "
                    f"{merchant_name.confidence}"
                )
            transaction_date = receipt.fields.get("TransactionDate")
            if transaction_date:
                print(
                    f"Transaction Date: {transaction_date.get('valueDate')} has confidence: "
                    f"{transaction_date.confidence}"
                )
            items = receipt.fields.get("Items")
            if items:
                print("Receipt items:")
                for idx, item in enumerate(items.get("valueArray")):
                    print(f"...Item #{idx + 1}")
                    item_description = item.get("valueObject").get("Description")
                    if item_description:
                        print(
                            f"......Item Description: {item_description.get('valueString')} has confidence: "
                            f"{item_description.confidence}"
                        )
                    item_quantity = item.get("valueObject").get("Quantity")
                    if item_quantity:
                        print(
                            f"......Item Quantity: {item_quantity.get('valueString')} has confidence: "
                            f"{item_quantity.confidence}"
                        )
                    item_total_price = item.get("valueObject").get("TotalPrice")
                    if item_total_price:
                        print(
                            f"......Total Item Price: {item_total_price.get('valueCurrency')} has confidence: "
                            f"{item_total_price.confidence}"
                        )
            subtotal = receipt.fields.get("Subtotal")
            if subtotal:
                print(
                    f"Subtotal: {subtotal.get('valueCurrency')} has confidence: {subtotal.confidence}"
                )
            tax = receipt.fields.get("TotalTax")
            if tax:
                print(f"Total tax: {tax.get('valueCurrency')} has confidence: {tax.confidence}")
            tip = receipt.fields.get("Tip")
            if tip:
                print(f"Tip: {tip.get('valueCurrency')} has confidence: {tip.confidence}")
            total = receipt.fields.get("Total")
            if total:
                print(f"Total: {total.get('valueCurrency')} has confidence: {total.confidence}")
        print("--------------------------------------")